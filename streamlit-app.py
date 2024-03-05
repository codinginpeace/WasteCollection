import streamlit as st
from mapProcessor.map import get_node_indexing_and_road_distance_matrix
from functions.funct import all_subsets_except_depot
import pandas as pd
import requests
from optimizer import find_optimal_route

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
