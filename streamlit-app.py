import streamlit as st
from mapProcessor.map import get_node_indexing_and_road_distance_matrix
from functions.funct import all_subsets_except_depot
import pandas as pd
import requests
from optimizer import find_optimal_route
import xml.etree.ElementTree as ET
import os
# Function to convert dataframe to CSV for download

# Your existing Streamlit app setup
st.set_page_config(
    page_title="Waste Management Planning",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.title("Waste Management Dasboard")

st.write("Welcome to the waste management dashboard. Please wait while the mapping of Kadıköy is processed...")

node_indexing, road_distance_matrix, longitudes, latitudes = get_node_indexing_and_road_distance_matrix()
st.write("Mapping is done!")


# Sets and indices
# Parameters
# Define a function to input the vehicle capacity
def input_vehicle_capacity():
    return st.number_input('Vehicle Capacity', min_value=1, value=8)

# Define a function to input the depot index
def input_depot():
    return st.number_input('Depot', min_value=0, value=0)

# Define a function to input the number of vehicles
def input_num_vehicles():
    return st.number_input('Number of Vehicles', min_value=1, value=2)


# Call the functions to get inputs
vehicle_capacity = input_vehicle_capacity()
depot = input_depot()
V = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
N = len(V)  # Number of vertices
K = input_num_vehicles()

st.write("Parameters are inserted")
# Data extraction from the dataframe
demands = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
service_times = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

if st.button("Start Routing"):
    # Run the optimization
    st.write("Optimization starting with the following parameters:")
    st.write(f"Vehicle Capacity: {vehicle_capacity}")
    st.write(f"Depot: {depot}")
    st.write(f"Vertices: {V}")
    st.write(f"Number of vertices: {N}")
    st.write(f"Number of vehicles: {K}")
    outputs = find_optimal_route(road_distance_matrix, vehicle_capacity, depot, V, N, K, demands, service_times)
    
    # Display the raw JSON output for reference
    st.subheader("Raw Optimization Output")
    #st.json(outputs)

    # Extracting the route information for each vehicle
    st.subheader("Optimization Results")
    st.write(f"Objective Value: {outputs['objective_value']}")

    # Display each route in a more readable format
    for route_info in outputs['routes']:
        vehicle = route_info['vehicle']
        route = route_info['route']
        st.write(f"Vehicle {vehicle} route: {' -> '.join(map(str, route))}")

    # Assuming latitudes and longitudes are your vertex coordinates
    coords = list(zip(latitudes, longitudes))
    coords_df = pd.DataFrame(coords, columns=['lat', 'lon'])

    st.map(coords_df)

    # Now for each vehicle, draw its route on the map
    # This is a simplistic example, you may need to adapt it based on your actual coordinate data
    for route_info in outputs['routes']:
        route_coords = [coords[vertex] for vertex in route_info['route']]
        route_df = pd.DataFrame(route_coords, columns=['lat', 'lon'])
        st.map(route_df)