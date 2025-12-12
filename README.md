Openrouteservice offers a variety of Geo-services accessible through a single API. The interactive API documentation lists several of these endpoints, including **directions**, **geocoding results**, **matrices**, **points of interest**, and **isochrones**.

The different endpoints available include:

*   **Directions** This service can be utilized globally to provide rich route instructions for various profiles, such as cars, trucks, different bike profiles, walking, hiking, or wheelchair. It offers many customization options, including different kinds of road restrictions or vehicle dimensions.
*   **Isochrones** This endpoint is used for reachability analysis, helping determine which areas objects can reach in given times or distances. Users can request up to 500 isochrones per day for free.
*   **Time-Distance Matrix (Matrices)** This application computes many-to-many distances and the times of routes. It is significantly faster for these calculations than repeatedly consuming the directions API and is often used by logistics organizations attempting to figure out the most optimal delivery routes.
*   **Optimization** Based on the Vroom project, this service provides optimal routes for solving Traveling Salesmen and other Vehicle Routing Problems (VRPs), while considering specific vehicle and time constraints.
*   **Pelias Geocoding** Geocoding transforms a description of a location (like a place name, street address, or postal code) into a normalized description that includes a point geometry. This service is built on the sophisticated Pelias Stack, which aggregates several data sources.
*   **POIs** (Points of Interest) The Openpoiservice allows you to find places of interest around or within given geographic coordinates. You can search for categories of points of interest around a point, path, or within a polygon.
*   **Elevation** Using the Openelevationservice, this endpoint easily enriches 2D geometries (Point or Line geometries) with height information based on SRTM data, returning the three-dimensional version quickly.
*   **Export endpoint** This endpoint is available for exporting the routing graph, allowing users to incorporate it into their analyses, such as for calculating edge centrality.

## Prerequisites

- Python 3.10 or higher
- An Openrouteservice API key (sign up at [openrouteservice.org](https://openrouteservice.org/))
- Create a `.env` file in the project root with your API key: `OPENROUTE_API_KEY=your_api_key_here`

## Installation

1. Clone or download this repository.
2. Install dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

   Or if using the pyproject.toml:

   ```bash
   pip install .
   ```

   Note: Some scripts require additional packages like `requests`. If not installed, run `pip install requests`.

## Usage

Each Python script demonstrates a specific API endpoint. Run them with:

```bash
python script_name.py
```

Outputs are printed to the console, and some generate HTML files for visualization.

### Streamlit App

#### geocodeautocomplete_app.py
**Purpose:** Interactive Streamlit app for geocoding autocomplete with optional user API key input, demo key (limited to 10 uses per session), and map visualization.

**Usage:**
```bash
streamlit run geocodeautocomplete_app.py
```

Users can enter their own Openrouteservice API key for unlimited use, or use the demo key for up to 10 searches per session. Enter text to geocode and click "Search" to see results and an interactive map.

**Setup for Demo Key:** For deployed apps, set the API key in Streamlit secrets as `OPENROUTE_API_KEY`. For local development, create `.streamlit/secrets.toml` with:

```
OPENROUTE_API_KEY = "your_api_key_here"
```

## Python Scripts

This repository contains Python scripts that demonstrate how to interact with the Openrouteservice API for various endpoints. Most scripts use the `requests` library to make API calls, while `pubCrawl.py` uses the `openrouteservice` Python client library. Scripts requiring mapping generate HTML files using `folium`.

### Geocoding Scripts

#### geocodesearch.py
**Purpose:** Performs a geocoding search to find locations based on a text query.

**Example Input:**
- Text: "Namibian Brewery"

**Example Output:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [17.065, -22.57]
      },
      "properties": {
        "label": "Namibian Brewery, Windhoek, Namibia"
      }
    }
  ]
}
```

#### geocodereverse.py
**Purpose:** Performs reverse geocoding to find addresses or places from coordinates. Generates an interactive map in `eiffel_geocode.html`.

**Example Input:**
- Coordinates: lon=2.294471, lat=48.858268

**Example Output:**
- JSON response with features near the point (e.g., Eiffel Tower details).
- Generates a Folium map with markers for the features.

#### geocodeautocomplete.py
**Purpose:** Provides autocomplete suggestions for geocoding queries. Generates a map in `tokyo_geocode.html`.

**Example Input:**
- Text: "Toky"

**Example Output:**
- JSON with autocomplete features (e.g., Tokyo-related locations).
- Folium map centered on the first result with markers.

#### geocodesearchstructured.py
**Purpose:** Performs structured geocoding search with specific address components (note: the script's URL is incomplete; add parameters like `&address=...&country=...` for full functionality).

**Example Input:**
- Structured query parameters (e.g., address components).

**Example Output:**
- JSON response with structured geocoding results.

### Elevation Scripts

#### elevationpointget.py
**Purpose:** Retrieves elevation data for a single point using GET request.

**Example Input:**
- Geometry: "13.349762,38.11295"

**Example Output:**
```json
{
  "geometry": {
    "coordinates": [13.349762, 38.11295, 123.45],
    "type": "Point"
  },
  "type": "Feature"
}
```

#### elevationpointpost.py
**Purpose:** Retrieves elevation for a point using POST request.

**Example Input:**
- Geometry: [13.331273, 38.10849]

**Example Output:**
- Similar JSON with elevation added.

#### elevationline.py
**Purpose:** Retrieves elevation profile for a line (encoded polyline).

**Example Input:**
- Geometry: "u`rgFswjpAKD" (encoded polyline)

**Example Output:**
- JSON with LineString geometry including elevation for each point.

### Export Scripts

#### export.py
**Purpose:** Exports the routing graph for a bounding box in default format.

**Example Input:**
- Bbox: [[8.681495,49.41461],[8.686507,49.41943]]

**Example Output:**
- JSON with graph data (nodes, edges, e.g., for Heidelberg area).

#### exportjson.py
**Purpose:** Exports routing graph in JSON format.

**Example Input:**
- Same bbox as above.

**Example Output:**
- JSON graph data.

#### exporttopology.py
**Purpose:** Exports routing graph in TopoJSON format.

**Example Input:**
- Same bbox.

**Example Output:**
- TopoJSON data for topology analysis.

### Isochrones Script

#### isochrones.py
**Purpose:** Generates isochrones (areas reachable within time/distance) and creates an interactive map in `isochrones_map.html`.

**Example Input:**
- Locations: [[48.73616760900966, 9.29131865414886], [48.72054146100535, 9.356893298214183]]
- Range: [300, 200] (seconds)

**Example Output:**
- GeoJSON with polygons for isochrones.
- Folium map with colored polygons (blue for 200s, red for 300s) and markers.

### Matrix Script

#### matrix.py
**Purpose:** Computes time-distance matrix between multiple locations.

**Example Input:**
- Locations: [[9.70093,48.477473], [9.207916,49.153868], [37.573242,55.801281], [115.663757,38.106467]]

**Example Output:**
```json
{
  "durations": [[0, 1234, 5678, 9012], ...],
  "distances": [[0, 12345, 56789, 90123], ...]
}
```

### Optimization Script

#### optimization.py
**Purpose:** Solves vehicle routing problems (VRP) with jobs and vehicles.

**Example Input:**
- Jobs: List of delivery jobs with locations, services, etc.
- Vehicles: List of vehicles with capacities, skills, etc.

**Example Output:**
```json
{
  "routes": [...],
  "unassigned": [],
  "summary": {...}
}
```

### POIs Script

#### pois.py
**Purpose:** Finds points of interest within a geometry or buffer.

**Example Input:**
- Geometry: bbox and point with buffer 200m.

**Example Output:**
- JSON with POI features (e.g., amenities in the area).

### Snapping Scripts

#### snapping.py
**Purpose:** Snaps locations to the nearest road network.

**Example Input:**
- Locations: [[8.669629,49.413025], [8.675841,49.418532], [8.665144,49.415594]]
- Radius: 350m

**Example Output:**
- JSON with snapped locations.

#### snappinggeojson.py
**Purpose:** Snaps locations and returns GeoJSON.

**Example Input:**
- Same as above.

**Example Output:**
- GeoJSON with snapped points.

#### snappingjson.py
**Purpose:** Snaps locations and returns JSON.

**Example Input:**
- Same as above.

**Example Output:**
- JSON with snapped data.

### Pub Crawl Script

#### pubCrawl.py
**Purpose:** Demonstrates a complex workflow: finds pubs in an area, filters them, computes distances, and optimizes a route for visiting them using OR-Tools. Generates a map in `pubCrawl.html`. Uses the `openrouteservice` library.

**Example Input:**
- Area: WKT polygon for Kreuzberg, Berlin.
- Category: Pubs (ID 569).

**Example Output:**
- Console: Number of pubs, filtered pubs, route calculations.
- Folium map with pub markers and optimized path.

### Main Script

#### main.py
**Purpose:** A simple hello world script, likely a placeholder.

**Example Input:**
- None

**Example Output:**
- "Hello from learnors!"