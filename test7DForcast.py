import requests
from datetime import datetime,date
import json
from dotenv import load_dotenv
import os
from geopy.geocoders import GeoNames

load_dotenv()

meteomatics_username = os.getenv("METEOMATICS_USERNAME")
meteomatics_password = os.getenv("METEOMATICS_PASSWORD")

geolocator = GeoNames(username=os.getenv("GEONAMES_USER"))

base_url = 'https://api.meteomatics.com/'
#time and day
today = date.today()
time = datetime.now()
time = time.strftime("%H:%M:%S")

auth = (meteomatics_username, meteomatics_password)
    
response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=42.3314&longitude=-83.0458&current=temperature_2m&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit&timezone=America%2FNew_York&forecast_days=14")
re = response.json()
print(re)
'''
print(time)
print(today)



#get the days and the corresponding weather information

#weather icon
day1 = re['data'][0]['coordinates'][0]['dates'][0]['value']
print(day1);

#all days
for x in range(9):
    #day 1 returns night icon(data was recorded at night)
    #weather icon
    icon = re['data'][0]['coordinates'][0]['dates'][x]['value']
    #low temp
    min =  data = re['data'][1]['coordinates'][0]['dates'][x]['value']
    #high temp
    max =  data = re['data'][2]['coordinates'][0]['dates'][x]['value']

    print("Day "+ str(x +1)+": "+ str(icon) + " "+ str(min)+ " "+str(max) )

print(re)
'''

#dictionary
print (re['daily']['temperature_2m_max'][0])
weekly_weather = {}

for x in range(8):
    day_data = {
        
        'min': re['daily']['temperature_2m_min'][0],
        'max': re['daily']['temperature_2m_max'][0]
    }
    weekly_weather[f'Day {x + 1}'] = day_data

print(weekly_weather)
