import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import streamlit as st

"""# Functions"""

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

def calculate_road_distance_matrix(longitudes, latitudes):
    """
    Calculate the road distance matrix for a set of points given their longitudes and latitudes.

    Parameters:
    - longitudes: List of longitudes for the points
    - latitudes: List of latitudes for the points

    Returns:
    - A 2D NumPy array representing the road distance matrix, where element (i, j)
      is the shortest road distance from point[i] to point[j].
    """
    # Ensure the graph is downloaded only once
    location_point = (np.mean(latitudes), np.mean(longitudes))
    G = ox.graph_from_point(location_point, dist=5000, network_type='drive')  # Adjust dist as needed

    num_points = len(longitudes)
    distance_matrix = np.zeros((num_points, num_points))

    # Find the nearest node in the network for each point
    nearest_nodes = [ox.distance.nearest_nodes(G, X=lon, Y=lat) for lon, lat in zip(longitudes, latitudes)]

    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                # Calculate the shortest path length between the nearest nodes
                try:
                    length = nx.shortest_path_length(G, nearest_nodes[i], nearest_nodes[j], weight='length')
                    distance_matrix[i, j] = length
                except nx.NetworkXNoPath:
                    distance_matrix[i, j] = np.inf

    return distance_matrix

"""# Process"""

def get_node_indexing_and_road_distance_matrix():
    # Load and parse the KML file

    kml_path = r'C:\Users\HUAWEI\Desktop\WasteCollection-st\smaller.kml'
    tree = ET.parse(kml_path)
    root = tree.getroot()


    # KML namespace
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    # Lists to hold parsed coordinates
    longitudes = []
    latitudes = []
    node_indexing = []

    # Extract the coordinates from the XML.
    nodeIndex = 1
    st.write("Extracting the coordinates...")
    for placemark in root.findall('.//kml:Placemark', ns):
        for point in placemark.findall('.//kml:Point', ns):
            coordinates = point.find('.//kml:coordinates', ns).text
            longitude, latitude, _ = coordinates.split(',')
            longitudes.append(float(longitude))
            latitudes.append(float(latitude))
            node_indexing.append(nodeIndex)
            nodeIndex += 1


    # Specify the location to download the road network
    location_point = (latitudes[0], longitudes[0])  # Using the first point as reference
    G = ox.graph_from_point(location_point, dist=1500, network_type='drive')

    # Save the graph to an image file
    fig, ax = ox.plot_graph(G, show=False, close=False)
    fig.savefig('graph.png', bbox_inches='tight')
    plt.close(fig)
    road_distance_matrix = calculate_road_distance_matrix(longitudes, latitudes)

    col1, col2 = st.columns([1,2])
    
    with col1:
        # Display the image in Streamlit
        st.subheader("Map")
        st.image('graph.png')

    with col2: 
        st.subheader("Distance Matrix")
        st.write(road_distance_matrix)
    return node_indexing, road_distance_matrix, longitudes, latitudes
