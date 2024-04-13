import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

df = pd.read_csv('merged_train_mini.csv')

# Use HTML with inline CSS to style your title
st.markdown("""
    <h1 style='text-align: center; color: red; font-size: 34px;'>
        Emergency Vehicle Response Time Analysis
    </h1>""", unsafe_allow_html=True)

def get_annotations(index):
    global df, top_10_types
    avg_delta = df[df['emergency vehicle type'] == top_10_types[index]]['delta selection-presentation'].mean()
    return [dict(text=f"{top_10_types[index]}: {avg_delta:.2f} seconds", x=0.5, y=0.5, showarrow=False, font_size=20)]

#plot the two graph 
col1, col2 = st.columns(2)
avg_deltas = df.groupby('emergency vehicle type')['delta selection-presentation'].mean()
top_10_types = df['emergency vehicle type'].value_counts().head(10).index
top_10_avg_deltas = avg_deltas.loc[top_10_types]
norm = mcolors.Normalize(vmin=top_10_avg_deltas.min(), vmax=top_10_avg_deltas.max())
cmap = plt.cm.Reds
colors = [cmap(norm(value)) for value in top_10_avg_deltas] 
hex_colors = [mcolors.rgb2hex(color) for color in colors]


fig = px.pie(
    df.loc[df['emergency vehicle type'].isin(top_10_types)], 
    names='emergency vehicle type',
    values='delta selection-presentation',
    title='Top 10 Emergency Vehicle Types by Average Response Time',
    color='delta selection-presentation',
    color_discrete_sequence=hex_colors
)

fig.update_traces(
    textinfo='percent+label',
    pull=[0.05]*10  
)
fig.update_layout(
    showlegend=False,
    title_font_size=14
)

with col1:
    st.plotly_chart(fig, use_container_width=True)


     
#plot the pie chart of alart reason category with color representing the time
avg_deltas_alerts = df.groupby('alert reason category')['delta selection-presentation'].mean()
top_5_alerts = df['alert reason category'].value_counts().nlargest(5).index
top_5_avg_deltas_alerts = avg_deltas_alerts.loc[top_5_alerts]
norm_alerts = mcolors.Normalize(vmin=top_5_avg_deltas_alerts.min(), vmax=top_5_avg_deltas_alerts.max())
cmap_alerts = plt.cm.Blues 
# Create a list of colors for the pie chart based on the average response time.
colors_alerts = [px.colors.sequential.Blues[int(i)] for i in np.linspace(0, len(px.colors.sequential.Blues) - 1, num=len(top_5_alerts))]

# Create the pie chart with Plotly.
fig2 = px.pie(
    df.loc[df['alert reason category'].isin(top_5_alerts)],
    names='alert reason category',
    values='delta selection-presentation',
    title='Top 5 Alert Reason Categories by Average Response Time',
    color='delta selection-presentation',
    color_discrete_sequence=colors_alerts
)
fig2.update_traces(
    textinfo='percent+label',
    pull=[0.05]*5 
)
fig2.update_layout(
    showlegend=False,
    title_font_size=14
)
# Add annotations to the pie chart for interactivity.
def get_annotations_alerts(category):
    # Get the average delta for the specific alert category.
    avg_delta = top_5_avg_deltas_alerts[category]
    return [dict(text=f"{category}: {avg_delta:.2f} seconds", x=0.5, y=0.5, showarrow=False, font_size=20)]

with col2:
    st.plotly_chart(fig2, use_container_width=True)
