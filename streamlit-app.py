import streamlit as st
from opt import find_optimal_route
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
vehicle_capacity = 100
depot = 0

V = node_indexing  # List of vertices including the depot
V = [0, 1, 2]
V = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
N = len(V)  # Number of vertices
K = 1  # Number of vehicles; this value should be set based on your specific problem

# Data extraction from the dataframe

demands = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
service_times = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


find_optimal_route(road_distance_matrix, vehicle_capacity, depot, V, N, K, demands, service_times)

