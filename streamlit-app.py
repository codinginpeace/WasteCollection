import streamlit as st
from mapProcessor.map import get_node_indexing_and_road_distance_matrix
from functions.funct import all_subsets_except_depot
import pandas as pd
# Function to convert dataframe to CSV for download

# Your existing Streamlit app setup
st.set_page_config(
    page_title="Waste Management Planning",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.header("Waste Management Dasboard")

node_indexing, road_distance_matrix, longitudes, latitudes = get_node_indexing_and_road_distance_matrix()

# Convert the distance matrix into a pandas DataFrame
df = pd.DataFrame(road_distance_matrix, columns=[f"Node {i+1}" for i in range(len(longitudes))], index=[f"Node {i+1}" for i in range(len(latitudes))])

# Display the DataFrame
st.write("Road Distance Matrix (in meters):")
st.write(df)

st.subheader("Enter Parameters")
# Parameters
vehicle_capacity = 8
K = 2  # Number of vehicles; this value should be set based on your specific problem

depot = 0

V = node_indexing  # List of vertices including the depot
V = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
N = len(V)  # Number of vertices
# Data extraction from the dataframe
demands = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
service_times = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


import requests

# Assuming your Flask API is running on localhost port 5000
api_url = 'http://127.0.0.1:5001/optimize'


data = {
    #'road_distance_matrix': road_distance_matrix.tolist(),  # Convert to list
    'vehicle_capacity': vehicle_capacity,
    'depot': depot,
    'V': V,
    'N': N,
    'K': K,
    'demands': demands,
    'service_times': service_times,
}
response = requests.post(api_url, json=data)

if response.status_code == 200:
    results = response.json()
    # Use the results in your Streamlit app
    # For example:
    st.write(results)
else:
    st.error("Failed to optimize route")

