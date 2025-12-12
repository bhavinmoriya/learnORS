import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENROUTE_API_KEY")
headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
}
call = requests.get(f'https://api.openrouteservice.org/geocode/autocomplete?api_key={api_key}&text=Toky', headers=headers)

# print(call.status_code, call.reason)
# print(call.text)

import folium

data = call.json()

# Center map on first feature
lon0, lat0 = data["features"][0]["geometry"]["coordinates"]
m = folium.Map(location=[lat0, lon0], zoom_start=10)

for f in data["features"]:
    lon, lat = f["geometry"]["coordinates"]
    name = f["properties"].get("label") or f["properties"].get("name")
    folium.Marker(
        [lat, lon],
        popup=name
    ).add_to(m)

m.save("tokyo_geocode.html")
