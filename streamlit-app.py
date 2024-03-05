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



import requests

# Assuming your Flask API is running on localhost port 5000
api_url = 'http://127.0.0.1:5000/optimize'

data={
  "vehicle_capacity": 100,
  "road_distance_matrix": [[0, 2, 3], [2, 0, 1], [3, 1, 0]],
  "depot": 0,
  "V": [0, 1, 2],
  "N": 3,
  "K": 2,
  "demands": [0, 10, 10],
  "service_times": [0, 5, 5]
}
response = requests.post(api_url, json=data)

if response.status_code == 200:
    results = response.json()
    # Use the results in your Streamlit app
    # For example:
    st.write(results)
else:
    st.write("Failed to optimize route")

