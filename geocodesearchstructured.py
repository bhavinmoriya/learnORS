import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENROUTE_API_KEY")
headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
}
call = requests.get(f'https://api.openrouteservice.org/geocode/search/structured?api_key={api_key}', headers=headers)

print(call.status_code, call.reason)
print(call.text)
