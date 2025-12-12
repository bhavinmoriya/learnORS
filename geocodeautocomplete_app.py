import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENROUTE_API_KEY")

st.title("Openrouteservice Geocode Autocomplete")

text_input = st.text_input("Enter text to geocode", "Toky")

if st.button("Search"):
    if not api_key:
        st.error("API key not found. Please set OPENROUTE_API_KEY in .env file.")
    elif text_input:
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }
        call = requests.get(f'https://api.openrouteservice.org/geocode/autocomplete?api_key={api_key}&text={text_input}', headers=headers)
        
        if call.status_code == 200:
            data = call.json()
            st.subheader("API Response")
            st.json(data)
            
            if data.get("features"):
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
                
                st.subheader("Map")
                st_folium(m, width=700, height=500)
            else:
                st.warning("No features found.")
        else:
            st.error(f"API call failed with status {call.status_code}: {call.reason}")
    else:
        st.warning("Please enter text to search.")