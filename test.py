from geopy.geocoders import GeoNames
from dotenv import load_dotenv
import os
from geopy.geocoders import GeoNames

load_dotenv()

# Initialize GeoNames geocoder
geolocator = GeoNames(username=os.getenv("GEONAMES_USER"))

# Specify the place (city name)
place = "toledo usa"

# Use geocode method to get location information
location = geolocator.geocode(place)

# Check if location information is available
if location:
    
    print(location.address)

else:
    print("Location not found.")