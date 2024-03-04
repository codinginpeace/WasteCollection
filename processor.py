import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
#upds

def visualize_route(G, node_sequence):
    """
    Visualizes a route given a sequence of node IDs.
    
    Parameters:
    - G: The graph object containing the road network.
    - node_sequence: A list or tuple of node IDs indicating the route.
    
    This function plots the route on the graph G.
    """
    # Initialize an empty list to store the routes (as lists of nodes)
    routes = []
    
    # Calculate the route for the sequence of nodes
    for i in range(len(node_sequence) - 1):
        # Find the shortest path between consecutive nodes
        route = nx.shortest_path(G, node_sequence[i], node_sequence[i+1], weight='length')
        routes.append(route)
    
    # Plot the graph with the routes
    fig, ax = ox.plot_graph_routes(G, routes, route_color='blue', route_linewidth=6, node_size=0)
    plt.show()


def calculate_distance_matrix(G, nodes, weight='length'):
    """
    Calculates the distance matrix between the given nodes in the graph G.
    
    Parameters:
    - G: The graph object containing the road network.
    - nodes: A list of node IDs for which to calculate the distance matrix.
    - weight: The edge weight property to use for distance calculations (default is 'length').
    
    Returns:
    - A 2D NumPy array representing the distance matrix, where element (i, j) is the 
      shortest path distance from node[i] to node[j].
    """
    # Initialize an empty matrix
    distance_matrix = np.zeros((len(nodes), len(nodes)))
    
    # Calculate shortest path distances between all pairs of nodes
    for i, node_start in enumerate(nodes):
        for j, node_end in enumerate(nodes):
            if i != j:  # No need to calculate distance from a node to itself
                try:
                    # Calculate the shortest path length
                    path_length = nx.shortest_path_length(G, node_start, node_end, weight=weight)
                    distance_matrix[i, j] = path_length
                except nx.NetworkXNoPath:
                    # If there is no path between node_start and node_end, set distance to a large value
                    distance_matrix[i, j] = np.inf
            else:
                # Distance from a node to itself is 0
                distance_matrix[i, j] = 0
    
    return distance_matrix

# Load and parse the KML file
tree = ET.parse('simplified.kml')
root = tree.getroot()

# KML namespace
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

# Lists to hold parsed coordinates
longitudes = []
latitudes = []

# Extract the coordinates from the XML.
for placemark in root.findall('.//kml:Placemark', ns):
    for point in placemark.findall('.//kml:Point', ns):
        coordinates = point.find('.//kml:coordinates', ns).text
        longitude, latitude, _ = coordinates.split(',')
        longitudes.append(float(longitude))
        latitudes.append(float(latitude))

# Specify the location to download the road network
location_point = (latitudes[0], longitudes[0])  # Using the first point as reference
G = ox.graph_from_point(location_point, dist=3000, network_type='drive')

"""
# For each point, find the nearest node in the network
nearest_nodes = [ox.distance.nearest_nodes(G, X=lon, Y=lat) for lat, lon in zip(latitudes, longitudes)]

# Assuming you want to route between consecutive points in your list
# Calculate the shortest path for each pair of consecutive nodes
routes = []
for i in range(len(nearest_nodes) - 1):
    route = nx.shortest_path(G, nearest_nodes[i], nearest_nodes[i+1], weight='length')
    routes.append(route)

# Plot the routes
fig, ax = ox.plot_graph_routes(G, routes, route_color='blue', route_linewidth=6, node_size=0)

# Example usage
# First, you need to have a graph G loaded. Here's how you might load a graph for a specific area:
location_point = (40.9801, 29.0287)  # Example coordinates for Kadıköy, İstanbul
G = ox.graph_from_point(location_point, dist=3000, network_type='drive')

# Now, you can call the function with your graph G and a sequence of nodes.
# The sequence of nodes should be replaced with actual node IDs from your graph.
# For demonstration, I'll use a hypothetical sequence of node IDs.
node_sequence = [1,2]  # Replace these with actual node IDs from your graph
#visualize_route(G, node_sequence)

calculate_distance_matrix(G, nodes, weight='length')
"""