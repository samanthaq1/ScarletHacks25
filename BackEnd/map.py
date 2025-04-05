import requests
maps_key = "Your_map_key"

def searchArea(userAddress, radius):
  #address = "1600+Amphitheatre+Parkway,+Mountain+View,+CA"

  address = userAddress.replace(" ", "+")

  # Set the location (latitude, longitude)
  geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={maps_key}"
  geo_response = requests.get(geo_url)
  geo_data = geo_response.json()

  lat = geo_data['results'][0]['geometry']['location']['lat']
  lng = geo_data['results'][0]['geometry']['location']['lng']

  # Set the radius (1 mile = 1609 meters)
  radius *= 1609  # 1 mile

  #lat, lng = 37.7749, -122.4194
  print(str(lat) + " gfhjkl " + str(lng))

  # Define the type of places you want to search for (stores, shopping centers, etc.)
  place_type = "grocery_or_supermarket"

  # Google Places API URL
  url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={place_type}&key={maps_key}"

  # Send the request
  response = requests.get(url)
  data = response.json()

  # Print the results
  if data['status'] == 'OK':
      print("Stores within the specified radius:")
      for result in data['results']:
          name = result.get('name')
          address = result.get('vicinity')
          print(f"Name: {name}, Address: {address}")
  else:
      print("Error:", data['status'])
      
searchArea("1600 Amphitheatre Parkway, Mountain View, CA", 1)