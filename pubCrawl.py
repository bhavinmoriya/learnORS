import folium
from shapely import wkt, geometry
import json
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
key = os.getenv("OPENROUTE_API_KEY")


api_key = key
wkt_str = 'Polygon ((13.43926404 52.48961046, 13.42040115 52.49586382, 13.42541101 52.48808523, 13.42368155 52.48635829, 13.40788599 52.48886084, 13.40852944 52.487142, 13.40745989 52.48614988, 13.40439187 52.48499746, 13.40154731 52.48500125, 13.40038591 52.48373202, 13.39423818 52.4838664, 13.39425346 52.48577149, 13.38629096 52.48582648, 13.38626853 52.48486362, 13.3715694 52.48495055, 13.37402099 52.4851697, 13.37416365 52.48771105, 13.37353615 52.48798191, 13.37539925 52.489432, 13.37643416 52.49167597, 13.36821531 52.49333093, 13.36952826 52.49886974, 13.37360623 52.50416333, 13.37497726 52.50337776, 13.37764916 52.5079675, 13.37893813 52.50693045, 13.39923153 52.50807711, 13.40022883 52.50938108, 13.40443425 52.50777471, 13.4052848 52.50821063, 13.40802944 52.50618019, 13.40997081 52.50692569, 13.41152096 52.50489127, 13.41407284 52.50403794, 13.41490921 52.50491634, 13.41760145 52.50417013, 13.41943091 52.50564912, 13.4230412 52.50498109, 13.42720031 52.50566607, 13.42940229 52.50857222, 13.45335235 52.49752496, 13.45090795 52.49710803, 13.44765912 52.49472124, 13.44497623 52.49442276, 13.43926404 52.48961046))'

aoi_geom = wkt.loads(wkt_str)  # load geometry from WKT string

aoi_coords = list(aoi_geom.exterior.coords)  # get coords from exterior ring
aoi_coords = [(y, x) for x, y in aoi_coords]  # swap (x,y) to (y,x). Really leaflet?!
aoi_centroid = aoi_geom.centroid  # Kreuzberg center for map center



m = folium.Map(location=(aoi_centroid.y, aoi_centroid.x), zoom_start=14)
folium.vector_layers.Polygon(aoi_coords,
                             color='#ffd699',
                             fill_color='#ffd699',
                             fill_opacity=0.4,
                             weight=3).add_to(m)
# m.save("pubCrawl.html")



from openrouteservice import client, places

ors = client.Client(key=api_key)


aoi_json = geometry.mapping(geometry.shape(aoi_geom))
query = {'request': 'pois',
         'geojson': aoi_json,
         'filter_category_ids': [569],
         'sortby': 'distance'}
pubs = ors.places(**query)['features']  # Perform the actual request and get inner json

# Amount of pubs in Kreuzberg
print("\nAmount of pubs: {}".format(len(pubs)))


query['filters_custom'] = {'smoking': ['yes']}  # Filter out smoker bars
pubs_smoker = ors.places(**query)['features']

print("\nAmount of smoker pubs: {}".format(len(pubs_smoker)))


pubs_addresses = []

for feat in pubs_smoker:
    lon, lat = feat['geometry']['coordinates']
    name = ors.pelias_reverse(point=(lon, lat))['features'][0]['properties']['name']
    popup = "<strong>{0}</strong><br>Lat: {1:.3f}<br>Long: {2:.3f}".format(name, lat, lon)
    icon = folium.map.Icon(color='lightgray',
                           icon_color='#b5231a',
                           icon='beer',  # fetches font-awesome.io symbols
                           prefix='fa')
    folium.map.Marker([lat, lon], icon=icon, popup=popup).add_to(m)
    pubs_addresses.append(name)

# folium.map.LayerControl().add_to(m)
# m.save("pubCrawl.html")

from openrouteservice import distance_matrix

pubs_coords = [feat['geometry']['coordinates'] for feat in pubs_smoker]

request = {'locations': pubs_coords,
           'profile': 'driving-car',
           'metrics': ['duration']}

pubs_matrix = ors.distance_matrix(**request)
print("Calculated {}x{} routes.".format(len(pubs_matrix['durations']), len(pubs_matrix['durations'][0])))

from ortools.constraint_solver import pywrapcp

tsp_size = len(pubs_addresses)
num_routes = 1
start = 0  # arbitrary start location
coords_aoi = [(y, x) for x, y in aoi_coords]  # swap (x,y) to (y,x)

optimal_coords = []

if tsp_size > 0:

    # Old Stuff kept for reference
    # routing = pywrapcp.RoutingModel(tsp_size, num_routes, start)

    # New Way according to ortools v7.0 docs (https://developers.google.com/optimization/support/release_notes#announcing-the-release-of-or-tools-v70)
    # manager = pywrapcp.RoutingIndexManager(num_locations, num_vehicles, depot)
    # routing = pywrapcp.RoutingModel(manager)

    # Adaption according to old and new way
    manager = pywrapcp.RoutingIndexManager(tsp_size, num_routes, start)
    routing = pywrapcp.RoutingModel(manager)


    # Create the distance callback, which takes two arguments (the from and to node indices)
    # and returns the distance between these nodes.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(pubs_matrix['durations'][from_node][to_node])


    # Since v7.0, this also needs to be wrapped:
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    # Solve, returns a solution if any.
    assignment = routing.Solve()
    if assignment:
        # Total cost of the 'optimal' solution.
        print("Total duration: " + str(round(assignment.ObjectiveValue(), 3) / 60) + " minutes\n")
        index = routing.Start(start)  # Index of the variable for the starting node.
        route = ''
        # while not routing.IsEnd(index):
        for node in range(routing.nodes()):
            # IndexToNode has been moved from the RoutingModel to the RoutingIndexManager
            optimal_coords.append(pubs_coords[manager.IndexToNode(index)])
            route += str(pubs_addresses[manager.IndexToNode(index)]) + ' -> '
            index = assignment.Value(routing.NextVar(index))
        route += str(pubs_addresses[manager.IndexToNode(index)])
        optimal_coords.append(pubs_coords[manager.IndexToNode(index)])
        print("Route:\n" + route)

def style_function(color):
    return lambda feature: dict(color=color,
                                weight=3,
                                opacity=1)


# See what a 'random' tour would have been
pubs_coords.append(pubs_coords[0])
request = {'coordinates': pubs_coords,
           'profile': 'driving-car',
           'geometry': 'true',
           'format_out': 'geojson',
           #            'instructions': 'false'
           }
random_route = ors.directions(**request)

folium.features.GeoJson(data=random_route,
                        name='Random Bar Crawl',
                        style_function=style_function('#84e184'),
                        overlay=True).add_to(m)

# And now the optimal route
request['coordinates'] = optimal_coords
optimal_route = ors.directions(**request)
folium.features.GeoJson(data=optimal_route,
                        name='Optimal Bar Crawl',
                        style_function=style_function('#6666ff'),
                        overlay=True).add_to(m)

m.add_child(folium.map.LayerControl())
m.save("pubCrawl.html")

optimal_duration = 0
random_duration = 0

optimal_duration = optimal_route['features'][0]['properties']['summary']['duration'] / 60
random_duration = random_route['features'][0]['properties']['summary']['duration'] / 60

print("Duration optimal route: {0:.3f} mins\nDuration random route: {1:.3f} mins".format(optimal_duration,random_duration))
