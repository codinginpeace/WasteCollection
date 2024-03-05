import streamlit as st
from mapProcessor.map import get_node_indexing_and_road_distance_matrix
from functions.funct import all_subsets_except_depot
import pandas as pd
import requests
from optimizer import find_optimal_route
import xml.etree.ElementTree as ET

# Function to convert dataframe to CSV for download

# Your existing Streamlit app setup
st.set_page_config(
    page_title="Waste Management Planning",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.title("Waste Management Dasboard")

# Parameters
vehicle_capacity = 8
depot = 0

tree = ET.parse('smaller.kml')
root = tree.getroot()

# KML namespace
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

# Lists to hold parsed coordinates
longitudes = []
latitudes = []
node_indexing = []

# Extract the coordinates from the XML.
nodeIndex = 1
for placemark in root.findall('.//kml:Placemark', ns):
    for point in placemark.findall('.//kml:Point', ns):
        coordinates = point.find('.//kml:coordinates', ns).text
        longitude, latitude, _ = coordinates.split(',')
        longitudes.append(float(longitude))
        latitudes.append(float(latitude))
        node_indexing.append(nodeIndex)
        nodeIndex += 1

st.write(nodeIndex)
node_indexing, road_distance_matrix, longitudes, latitudes = get_node_indexing_and_road_distance_matrix()

# Sets and indices
V = node_indexing  # List of vertices including the depot
V = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
N = len(V)  # Number of vertices
K = 2  # Number of vehicles; this value should be set based on your specific problem

st.write("Parameters are inserted")
# Data extraction from the dataframe
demands = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
service_times = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
outputs = find_optimal_route(road_distance_matrix, vehicle_capacity, depot, V, N, K, demands, service_times)
