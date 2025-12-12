import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENROUTE_API_KEY")
body = {"format_in":"point","geometry":[13.331273,38.10849]}

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': api_key,
    'Content-Type': 'application/json; charset=utf-8'
}
call = requests.post('https://api.openrouteservice.org/elevation/point', json=body, headers=headers)

print(call.status_code, call.reason)
print(call.text)
