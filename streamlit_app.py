import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

df = pd.read_csv('merged_train_mini.csv')

fig, ax = plt.subplots()
col1, col2 = st.columns(2)

#plot the pie chart of emergency vehicle type (top 10)
fig1, ax = plt.subplots(figsize=(10, 10)) 
df['emergency vehicle type'].value_counts().nlargest(10).plot.pie(autopct='%1.1f%%', ax=ax)
ax.set_title('Emergency Vehicle Type Top 10')
with col1:
    st.pyplot(fig1)

#plot the pie chart of alart reason category
fig2, ax = plt.subplots(figsize=(10, 6))
df['alert reason category'].value_counts().nlargest(5).plot.pie(autopct='%1.1f%%', ax=ax)
ax.set_title('Alert Reason Category Top 5')
with col2:
    st.pyplot(fig2)
