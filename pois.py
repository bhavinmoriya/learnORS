import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENROUTE_API_KEY")
body = {"request":"pois","geometry":{"bbox":[[8.8034,53.0756],[8.7834,53.0456]],"geojson":{"type":"Point","coordinates":[8.8034,53.0756]},"buffer":200}}

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': api_key,
    'Content-Type': 'application/json; charset=utf-8'
}
call = requests.post('https://api.openrouteservice.org/pois', json=body, headers=headers)

print(call.status_code, call.reason)
print(call.text)
