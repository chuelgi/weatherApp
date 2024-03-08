import requests
from datetime import datetime
import json
from dotenv import load_dotenv
import os
from geopy.geocoders import GeoNames

load_dotenv()

meteomatics_username = os.getenv("METEOMATICS_USERNAME")
meteomatics_password = os.getenv("METEOMATICS_PASSWORD")

geolocator = GeoNames(username=os.getenv("GEONAMES_USER"))

base_url = 'https://api.meteomatics.com/'
#thetime = get_current_time()

auth = (meteomatics_username, meteomatics_password)
    
response = requests.get(f'{base_url}2024-03-02T00:00:00ZP8D:PT24H/weather_symbol_1h:idx,t_min_2m_24h:F,t_max_2m_24h:F/42.3315509,-83.0466403/json', auth=auth)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

print(data)

daily_temperatures = {}
for entry in data['data']:
    parameter = entry['parameter']
    for coordinate in entry['coordinates']:
        for date_entry in coordinate['dates']:
            date = date_entry['date'][:10]  # Extract date portion (YYYY-MM-DD)
            temperature = date_entry['value']
            if date not in daily_temperatures:
                daily_temperatures[date] = {}
            if parameter == 't_min_2m_24h:F':
                daily_temperatures[date]['low'] = temperature
            elif parameter == 't_max_2m_24h:F':
                daily_temperatures[date]['high'] = temperature

# Print the extracted daily high and low temperatures
for date, temperatures in daily_temperatures.items():
    print(f'Date: {date}, High: {temperatures["high"]}, Low: {temperatures["low"]}')