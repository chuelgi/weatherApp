from geopy.geocoders import GeoNames

# Initialize GeoNames geocoder
geolocator = GeoNames(username="")

# Specify the place (city name)
place = "Boston England"

# Use geocode method to get location information
location = geolocator.geocode(place)

# Check if location information is available
if location:
    
    print("Place:", location.address)
    print("Latitude:", location.latitude)
    print("Longitude:", location.longitude)
else:
    print("Location not found.")