import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENROUTE_API_KEY")
body = {"jobs":[{"id":1,"service":300,"delivery":[1],"location":[1.98465,48.70329],"skills":[1],"time_windows":[[32400,36000]]},{"id":2,"service":300,"delivery":[1],"location":[2.03655,48.61128],"skills":[1]},{"id":3,"service":300,"delivery":[1],"location":[2.39719,49.07611],"skills":[2]},{"id":4,"service":300,"delivery":[1],"location":[2.41808,49.22619],"skills":[2]},{"id":5,"service":300,"delivery":[1],"location":[2.28325,48.5958],"skills":[14]},{"id":6,"service":300,"delivery":[1],"location":[2.89357,48.90736],"skills":[14]}],"vehicles":[{"id":1,"profile":"driving-car","start":[2.35044,48.51764],"end":[2.35044,48.51764],"capacity":[4],"skills":[1,14],"time_window":[28800,43200]},{"id":2,"profile":"driving-car","start":[2.35044,48.51764],"end":[2.35044,48.51764],"capacity":[4],"skills":[2,14],"time_window":[28800,43200]}]}

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': api_key,
    'Content-Type': 'application/json; charset=utf-8'
}
call = requests.post('https://api.openrouteservice.org/optimization', json=body, headers=headers)

print(call.status_code, call.reason)
print(call.text)
