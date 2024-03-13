from flask import Flask, render_template, request
import requests
from datetime import datetime
import json
from dotenv import load_dotenv
import os
from geopy.geocoders import GeoNames

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'
load_dotenv()

#meteomatics_username = os.getenv("METEOMATICS_USERNAME")

#meteomatics_password = os.getenv("METEOMATICS_PASSWORD")

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

    base_url = 'https://api.open-meteo.com/v1/forecast?'
    thetime = get_current_time()
    print(thetime)
    #get city coordinates
    lat, log, address, error_message = get_coordinates(city)

    if error_message:
        return f"Error: {error_message}"
    print(log)
    
    if lat is not None and log is not None and address is not None:

        
        #auth = (meteomatics_username, meteomatics_password)
        
        response = requests.get(f'{base_url}latitude={lat}&longitude={log}&current=temperature_2m&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit&timezone=America%2FNew_York&forecast_days=14')

        if response.status_code != 200:
            return f"Could not fetch weather data for {city}. Status code: {response.status_code}"

        try: 
            data = response.json()

            #today info
            today_data = {
                'min': data['daily']['temperature_2m_min'][0],
                'max': data['daily']['temperature_2m_max'][0]

            }

            #put info into dictionary
            weekly_weather = {}

            for x in range(1,8):
                day_data = {
                    'min': data['daily']['temperature_2m_min'][x],
                    'max': data['daily']['temperature_2m_max'][x]
                }
                weekly_weather[f'Day {x}'] = day_data
            return today_data, weekly_weather
                
        except json.JSONDecodeError as e:
            return f"Could not decode: {e}"
    else:
        return f"Error, try again later."

@app.route('/', methods=['GET', 'POST'])
def home():

    result = None
    alert_message = None
    today_data = None
    weekly_weather = None

    if request.method == 'POST':
        city = request.form['city']
        state = request.form.get('state', '') 
        country = request.form.get('country', '')  
        location = f"{city} {state} {country}".strip()  
        result = get_weather(location)

        
        if isinstance(result, tuple):  
            today_data, weekly_weather = result 
        else:
            alert_message = result #error message
            result = None
            return render_template('index.html', result=result, alert_message=alert_message)
            
        return render_template('result.html', result=result, city=location, weekly_weather=weekly_weather, today_data=today_data) 

    return render_template('index.html', result=result, weekly_weather=weekly_weather, today_data=today_data) 

if __name__ == '__main__':
    app.run(debug=True)
