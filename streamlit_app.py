import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

df = pd.read_csv('merged_train_mini.csv')

# Use HTML with inline CSS to style your title
st.markdown("""
    <h1 style='text-align: center; color: red; font-size: 34px;'>
        Emergency Vehicle Response Time Analysis
    </h1>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

avg_deltas = df.groupby('emergency vehicle type')['delta selection-presentation'].mean()
top_10_types = df['emergency vehicle type'].value_counts().head(10).index
top_10_avg_deltas = avg_deltas.loc[top_10_types]
norm = mcolors.Normalize(vmin=top_10_avg_deltas.min(), vmax=top_10_avg_deltas.max())
cmap = plt.cm.Reds
colors = [cmap(norm(value)) for value in top_10_avg_deltas] #assign color 
fig1, ax1 = plt.subplots()
fig1, ax1 = plt.subplots(figsize=(15, 10))
explode = [0.05] * 10
custom_labels = list(top_10_types[:5]) + [None] * (10 - 5)

patches, texts, autotexts = ax1.pie(
    df['emergency vehicle type'].value_counts().head(10),
    labels=custom_labels,
    autopct='%1.1f%%',  # Percentage formatting
    startangle=90,
    colors=colors,
    explode=explode,
    textprops={'fontsize': 10},  # Smaller font size
    pctdistance=0.85,  # Adjust this value as needed to move percentage labels out
    labeldistance=1.1  # Adjust this value to move labels out
)

for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_horizontalalignment('center')

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax1)
cbar.set_label('Average Response Time (seconds)')
ax1.set_title('Top 10 Emergency Vehicle Types by Average Response Time', fontsize=14)
plt.show()
with col1:
    st.pyplot(fig1)
    
     
#plot the pie chart of alart reason category with color representing the time
avg_deltas_alerts = df.groupby('alert reason category')['delta selection-presentation'].mean()
top_5_alerts = df['alert reason category'].value_counts().nlargest(5).index
top_5_avg_deltas_alerts = avg_deltas_alerts.loc[top_5_alerts]
norm_alerts = mcolors.Normalize(vmin=top_5_avg_deltas_alerts.min(), vmax=top_5_avg_deltas_alerts.max())
cmap_alerts = plt.cm.Blues 
colors_alerts = [cmap_alerts(norm_alerts(value)) for value in top_5_avg_deltas_alerts]

fig2, ax2 = plt.subplots(figsize=(15, 10))
explode1 = [0.05] * 5
patches, texts, autotexts = ax2.pie(
    df['alert reason category'].value_counts().nlargest(5),
    labels=top_5_alerts,
    autopct='%1.1f%%',
    explode=explode1,
    startangle=90,
    colors=colors_alerts,
    pctdistance=0.85,
)

for autotext in autotexts:
    autotext.set_color('black')
ax2.set_title('Top 5 Alert Reason Categories by Average Response Time')

sm_alerts = plt.cm.ScalarMappable(cmap=cmap_alerts, norm=norm_alerts)
sm_alerts.set_array([])
cbar = plt.colorbar(sm_alerts, ax=ax2)
cbar.set_label('Average Response Time (seconds)')

plt.show()
with col2:
    st.pyplot(fig2)
