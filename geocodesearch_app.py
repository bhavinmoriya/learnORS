import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Openrouteservice Geocode Search",
    page_icon="🔍",
    layout="centered"
)

st.title("Openrouteservice Geocode Search")

st.markdown("Get your API key from [openrouteservice.org](https://account.heigit.org/login) for unlimited use, or use the demo key (limited to 13 searches per session).")

# Initialize session state for API call count
if 'api_call_count' not in st.session_state:
    st.session_state.api_call_count = 0

api_key_input = st.text_input("Enter your Openrouteservice API Key (optional)", type="password")

text_input = st.text_input("Enter text to geocode", "Namibian Brewery")

if st.button("Search"):
    if api_key_input:
        api_key = api_key_input
        st.info("Using your provided API key.")
    else:
        if st.session_state.api_call_count >= 13:
            st.error("You have reached the limit of 13 free uses. Please provide your own API key.")
            st.stop()
        try:
            api_key = st.secrets["openrouteservice"]["OPENROUTE_API_KEY"]
            st.session_state.api_call_count += 1
            st.info(f"Using demo API key. Uses left: {13 - st.session_state.api_call_count}")
        except KeyError:
            st.error("Demo API key not configured. Please provide your own API key.")
            st.stop()
    
    if text_input:
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }
        call = requests.get(f'https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={text_input}', headers=headers)
        
        if call.status_code == 200:
            data = call.json()
            st.subheader("API Response")
            st.json(data)

            st.subheader(f"API Response has {len(data['features'])} features")
            # st.json(len(data["features"]))
            
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
                st_folium(m, width=700, height=500, returned_objects=[])
            else:
                st.warning("No features found.")
        else:
            st.error(f"API call failed with status {call.status_code}: {call.reason}")
    else:
        st.warning("Please enter text to search.")