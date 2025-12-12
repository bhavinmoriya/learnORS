import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENROUTE_API_KEY")
body = {"locations":[[8.669629,49.413025],[8.675841,49.418532],[8.665144,49.415594]],"radius":350}

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': api_key,
    'Content-Type': 'application/json; charset=utf-8'
}
call = requests.post('https://api.openrouteservice.org/v2/snap/driving-car/geojson', json=body, headers=headers)

print(call.status_code, call.reason)
print(call.text)
