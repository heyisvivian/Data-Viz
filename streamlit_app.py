import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import requests
from io import StringIO

@st.cache
def load_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = pd.read_csv(StringIO(response.text))
        return data
    else:
        return pd.DataFrame()

# URL of your dataset
data_x = "https://challengedata.ens.fr/participants/challenges/21/download/x-train"
data_y = "https://challengedata.ens.fr/participants/challenges/21/download/y-train"

# Load data
data_x = load_data(data_x)
data_y = load_data(data_y)
merged_data = pd.merge(data_x, data_y, on='emergency vehicle selection')

# Use the merged data in your app
st.write(merged_data)

#plot the pie chart of emergency vehicle type
vehicle_type_counts = merged_data['emergency_vehicle_type'].value_counts()

# Create a pie chart
fig, ax = plt.subplots()
ax.pie(vehicle_type_counts, labels=vehicle_type_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the pie chart using Streamlit
st.pyplot(fig)



