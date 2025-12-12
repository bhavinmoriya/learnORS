import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Openrouteservice Reverse Geocode",
    page_icon="📍",
    layout="centered"
)

st.title("Openrouteservice Reverse Geocode")

st.markdown("Get your API key from [openrouteservice.org](https://account.heigit.org/login) for unlimited use, or use the demo key (limited to 13 searches per session).")

# Initialize session state for API call count
if 'api_call_count' not in st.session_state:
    st.session_state.api_call_count = 0

api_key_input = st.text_input("Enter your Openrouteservice API Key (optional)", type="password")

col1, col2 = st.columns(2)
with col1:
    lat_input = st.number_input("Latitude", value=48.858268, format="%.6f")
with col2:
    lon_input = st.number_input("Longitude", value=2.294471, format="%.6f")

if st.button("Reverse Geocode"):
    if api_key_input:
        api_key = api_key_input
        st.info("Using your provided API key.")
    else:
        if st.session_state.api_call_count >= 13:
            st.error("You have reached the limit of 13 free uses. Please provide your own API key.")
            st.stop()
        try:
            api_key = st.secrets["OPENROUTE_API_KEY"]
            st.session_state.api_call_count += 1
            st.info(f"Using demo API key. Uses left: {13 - st.session_state.api_call_count}")
        except KeyError:
            st.error("Demo API key not configured. Please provide your own API key.")
            st.stop()
    
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    }
    call = requests.get(f'https://api.openrouteservice.org/geocode/reverse?api_key={api_key}&point.lon={lon_input}&point.lat={lat_input}', headers=headers)
    
    if call.status_code == 200:
        data = call.json()
        st.subheader("API Response")
        st.json(data)
        
        if data.get("features"):
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
            
            st.subheader("Map")
            st_folium(m, width=700, height=500)
        else:
            st.warning("No features found.")
    else:
        st.error(f"API call failed with status {call.status_code}: {call.reason}")