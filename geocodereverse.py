import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENROUTE_API_KEY")
headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
}
call = requests.get(f'https://api.openrouteservice.org/geocode/reverse?api_key={api_key}&point.lon=2.294471&point.lat=48.858268', headers=headers)

print(call.status_code, call.reason)
# print(call.text)

import folium

data = call.json()
# Center map on first feature
lon0, lat0 = data["features"][0]["geometry"]["coordinates"]
m = folium.Map(location=[lat0, lon0], zoom_start=17)

for f in data["features"]:
    lon, lat = f["geometry"]["coordinates"]  # GeoJSON: [lon, lat]
    props = f.get("properties", {})
    label = props.get("label") or props.get("name") or "No name"

    folium.Marker(
        location=[lat, lon],      # Folium/Leaflet: [lat, lon]
        popup=label
    ).add_to(m)

# Add required attribution
folium.map.LayerControl().add_to(m)
m.get_root().html.add_child(folium.Element(
    '<div style="position: fixed; bottom: 5px; left: 5px; '
    'background: white; padding: 3px; font-size: 11px;">'
    '© openrouteservice.org by HeiGIT | Map data © OpenStreetMap contributors'
    '</div>'
))

m.save("eiffel_geocode.html")
