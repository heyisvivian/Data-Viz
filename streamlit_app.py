import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

df = pd.read_csv('merged_train_mini.csv')

# Create a Matplotlib figure and axis
fig, ax = plt.subplots()
# Plot data on the axis
df['emergency vehicle type'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
# Set the title
ax.set_title('Emergency Vehicle Type')
# Display the plot in Streamlit
st.pyplot(fig)

