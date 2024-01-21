from flask import Flask, render_template, request
import requests
from datetime import datetime
import json
from dotenv import load_dotenv
import os
from geopy.geocoders import GeoNames

app = Flask(__name__, static_folder='static')

load_dotenv()

meteomatics_username = os.getenv("METEOMATICS_USERNAME")
meteomatics_password = os.getenv("METEOMATICS_PASSWORD")

geolocator = GeoNames(username=os.getenv("GEONAMES_USER"))

def get_current_time():
    current_time = datetime.now()

    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    return formatted_time

def get_coordinates(city):
    location = geolocator.geocode(city)

    if location:
        lat = location.latitude
        log = location.longitude
        address = location.address
        return lat, log, address
    else:
        print("Location not found.")
        return None

def get_weather(city):
    base_url = 'https://api.meteomatics.com/'
    thetime = get_current_time()

    #get city coordinates
    location = get_coordinates(city)

    
    if location:
        lat, log, address = location
        auth = (meteomatics_username, meteomatics_password)
        print(f"API Request URL: {base_url}{thetime}/t_2m:F/{lat},{log}/json")
        
        response = requests.get(f'{base_url}{thetime}/t_2m:F/{lat},{log}/json', auth=auth)

        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Content: {response.content}")

        if response.status_code != 200:
            return f"Could not fetch weather data for {city}. Status code: {response.status_code}"

        try: 
            data = json.loads(response.content)
        except json.JSONDecodeError as e:
            return "Could not decode"

        if 'data' in data and data['data']:
            temperature = data['data'][0]['coordinates'][0]['dates'][0]['value']
            return {'temperature': temperature, 'address':address}
        else:
            return f"Could not find temperature information in the API response for {city}."
    else:
        return f"Could not fetch coordinates for {city}."

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        location = request.form['city'] 
        result = get_weather(location)
        return render_template('result.html', result=result, city=location)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
