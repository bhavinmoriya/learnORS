import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENROUTE_API_KEY")
# print(api_key)
# import requests

import requests
import folium

body = {"locations":[[8.681495,49.41461],[8.686507,49.41943]],"range":[300,200]}
body = {"locations":[[48.73616760900966, 9.29131865414886][::-1],[48.72054146100535, 9.356893298214183][::-1]],"range":[300,200]}

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': api_key,
    'Content-Type': 'application/json; charset=utf-8'
}
call = requests.post('https://api.openrouteservice.org/v2/isochrones/driving-car', json=body, headers=headers)

# print(call.status_code, call.reason)
print(call.json())
print(call.json().keys())

# Your GeoJSON data
geojson_data = call.json()

# Create a Folium map centered on the area
m = folium.Map(location=[49.419, 8.682], zoom_start=14)

# Define a style function for the polygons
def style_function(feature):
    if feature['properties']['value'] == 200:
        return {
            'fillColor': 'blue',
            'color': 'blue',
            'weight': 2,
            'fillOpacity': 0.2,
        }
    else:
        return {
            'fillColor': 'blue',
            'color': 'red',
            'weight': 2,
            'fillOpacity': 0.2,
        }

# Add the GeoJSON data to the map
folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['value', 'group_index'])
).add_to(m)

# Add markers for the centers of the isochrones
folium.Marker(
    location=[49.41459939191395, 8.681494991825476],
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

folium.Marker(
    location=[49.419429892535234, 8.686505661289154],
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Save the map to an HTML file
m.save('isochrones_map.html')
