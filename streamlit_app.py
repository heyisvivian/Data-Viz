import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

df = pd.read_csv('merged_train_mini.csv')

#plot the pie chart of emergency vehicle type
df['emergency vehicle type'].value_counts().plot.pie(autopct='%1.1f%%')
plt.title('Emergency Vehicle Type')
plt.show()
st.pyplot()

