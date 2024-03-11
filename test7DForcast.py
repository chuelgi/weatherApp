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
    
response = requests.get(f'{base_url}{today}T22:00:00ZP7D:PT24H/weather_symbol_1h:idx,t_min_2m_24h:F,t_max_2m_24h:F/42.3315509,-83.0466403/json', auth=auth)
re = response.json()
print(time)
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

weekly_weather = {}

for x in range(8):
    day_data = {
        'icon': re['data'][0]['coordinates'][0]['dates'][x]['value'],
        'min': re['data'][1]['coordinates'][0]['dates'][x]['value'],
        'max': re['data'][2]['coordinates'][0]['dates'][x]['value']
    }
    weekly_weather[f'Day {x + 1}'] = day_data

print(weekly_weather)
