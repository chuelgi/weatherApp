from flask import Flask, render_template, request,flash,redirect, url_for
import requests
from datetime import datetime
import json
from dotenv import load_dotenv
import os
from geopy.geocoders import GeoNames

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'
load_dotenv()

meteomatics_username = os.getenv("METEOMATICS_USERNAME")
meteomatics_password = os.getenv("METEOMATICS_PASSWORD")

geolocator = GeoNames(username=os.getenv("GEONAMES_USER"))

def get_current_time():
    current_time = datetime.now()

    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    return formatted_time

def get_coordinates(city):

     try:
        location = geolocator.geocode(city)

        if location:
            lat = location.latitude
            log = location.longitude
            address = location.address
            return lat, log, address, None  #error message is none
        else:
            print("Location not found.")
            return None, None, None, "Location not found."
     except Exception as e:
        return None, None, None, f"GeoName error: {e}"
        

def get_weather(city):

    base_url = 'https://api.meteomatics.com/'
    thetime = get_current_time()

    #get city coordinates
    lat, log, address, error_message = get_coordinates(city)

    if error_message:
        return f"Error: {error_message}"
    
    if lat is not None and log is not None and address is not None:

        
        auth = (meteomatics_username, meteomatics_password)
        
        response = requests.get(f'{base_url}{thetime}/t_2m:F/{lat},{log}/json', auth=auth)

        if response.status_code != 200:
            return f"Could not fetch weather data for {city}. Status code: {response.status_code}"

        try: 
            data = json.loads(response.content)
        except json.JSONDecodeError as e:
            return f"Could not decode: {e}"
            
        if 'data' in data and data['data']:
            temperature = data['data'][0]['coordinates'][0]['dates'][0]['value']
            return {'temperature': temperature, 'address': address}
        else:
            return f"Could not find temperature information in the API response for {city}."
    else:
        return f"Error, try again later."

@app.route('/', methods=['GET', 'POST'])
def home():

    result = None
    alert_message = None
    if request.method == 'POST':
        city = request.form['city']

        state = request.form.get('state', '') 
        country = request.form.get('country', '')  
        location = f"{city} {state} {country}".strip()  
        result = get_weather(location)

        #error message
        if isinstance(result, str):  
            alert_message = result
            result = None
            return render_template('index.html', result=result, alert_message=alert_message)
        return render_template('result.html', result=result, city=location)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
