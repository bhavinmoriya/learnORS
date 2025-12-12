import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENROUTE_API_KEY")
headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
}
call = requests.get(f'https://api.openrouteservice.org/geocode/search?api_key={api_key}&text=Namibian%20Brewery', headers=headers)

# print(call.status_code, call.reason)
print(call.json().keys())
# for k in list(call.json().keys()):
#     print(k)
#     print(call.json()[k])
#     print()

for f in call.json().get("features", []):
    print(f)
    print()
# print(json.dumps(call.json(), indent=2))

data = call.json() 
print(type(data["features"]))           
            
if data.get("features"):
    # Center map on first feature
    lon0, lat0 = data["features"][0]["geometry"]["coordinates"]
    print(lon0, lat0)
    # m = folium.Map(location=[lat0, lon0], zoom_start=10)
    
    for f in data["features"]:
        lon, lat = f["geometry"]["coordinates"]
        name = f["properties"].get("label") or f["properties"].get("name")
        print(lat, lon, name)