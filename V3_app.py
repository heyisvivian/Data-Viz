import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from sklearn.cluster import KMeans


# Liste des raisons d'accident
accident_reasons = [
    "Vehicle collision",
    "Pedestrian accident",
    "Residential fire",
    "Commercial fire",
    "Chemical spill",
    "Carbon monoxide poisoning",
    "High fall",
    "Drowning",
    "Cardiac arrest"
]


df = pd.read_csv('data.csv', sep=';')
df = df.sample(n=100000, random_state=42)

# Création d'un dictionnaire pour mapper les numéros aux noms des raisons d'accident
reason_mapping = {i+1: reason for i, reason in enumerate(accident_reasons)}

# Remplacement des numéros dans 'alert reason category' par les noms correspondants
df['alert reason category'] = df['alert reason category'].replace(reason_mapping)
# Page configuration
st.set_page_config(page_title="Emergency Response Journey", layout="wide")

# Header section
image_url = 'https://www.immatriculation-autocollant.fr/55223-large_default/sapeurs-pompiers-rf-logo-sticker.jpg'

# HTML content with CSS for styling
st.markdown(f"""
<style>
.header {{
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}}
.header-img {{
    width: 100px;  /* Adjust the size of the image */
    margin-right: 20px; /* Space between the image and the text */
}}
.header-img:last-child {{
    margin-left: 20px; /* Space between the text and the second image */
    margin-right: 0;
}}
</style>
<div class="header">
    <img src="{image_url}" class="header-img">
    <h1 style="text-align: center;">The journey of emergency response of the Paris Fire Brigade vehicles</h1>
    <img src="{image_url}" class="header-img">
</div>
""", unsafe_allow_html=True)


st.markdown("""
Imagine the moment of an emergency—an accident on the bustling streets of Paris, a heart beating to the rhythm of urgency, and a phone call that could mean the difference between despair and hope. This is where our story begins, in the heart of a rescue center, where every second counts, and every decision matters.

The phone rings, and with it, an echo of distress travels through the wires. The operator's voice, calm and reassuring, slices through the panic, collecting precious information. The location of the accident, the nature of the distress, the number of people in need—all puzzle pieces that start to form a picture of the crisis at hand.
""")

# Map Visualization with Filters
st.header("Accident Location Analysis")
# Creating columns for filters and map
col1, col2, col3 = st.columns([1, 3, 2])

with col1:
    st.subheader("Filters")

    # Assuming 'df' already has 'alert reason category' replaced with descriptive text
    accident_reason_options = ['All'] + sorted(df['alert reason category'].unique().tolist())
    accident_reason = st.selectbox("Select Accident Reason", options=accident_reason_options)
    
    time_of_day = st.slider("Select Time of Day", 0, 24, (8, 10))
    
    #rescue_center_options = ['All'] + sorted(df['rescue center'].unique().tolist())
    #selected_rescue_center = st.selectbox("Select Rescue Center", options=rescue_center_options)

paris = 'https://france-geojson.gregoiredavid.fr/repo/departements/75-paris/communes-75-paris.geojson'
paris = alt.topo_feature(url=paris, feature='geometry')
df_filtered = df[(df['hour'] >= time_of_day[0]) & (df['hour'] <= time_of_day[1])]
if accident_reason != 'All':
    df_filtered = df[df['alert reason category'] == accident_reason]
#if selected_rescue_center != 'All':
#    df_filtered = df_filtered[df_filtered['rescue center'] == selected_rescue_center]

X = df_filtered[['longitude intervention', 'latitude intervention']]
n_clusters = 10
kmeans = KMeans(n_clusters=n_clusters, n_init=10)
df_filtered.loc[:, 'cluster_label'] = kmeans.fit_predict(X)
centroids = df_filtered.groupby('cluster_label').agg({'longitude intervention': 'mean', 'latitude intervention': 'mean'}).reset_index()
centroids.rename(columns={'longitude intervention': 'longitude centroid', 'latitude intervention': 'latitude centroid'}, inplace=True)
cluster_counts = df_filtered['cluster_label'].value_counts().reset_index()
cluster_counts.columns = ['cluster_label', 'Number of interventions']
centroids = centroids.merge(cluster_counts, on='cluster_label', how='left')
link_centroid_rc = df_filtered[['longitude intervention', 'latitude intervention', 'cluster_label', 'longitude before departure', 'latitude before departure']].copy()
link_centroid_rc = link_centroid_rc.merge(centroids[['cluster_label', 'longitude centroid', 'latitude centroid']], on='cluster_label', how='left')
link_centroid_rc=link_centroid_rc.drop(['longitude intervention', 'latitude intervention'], axis=1).drop_duplicates()

hour_mapping = {
    0: "midnight",
    1: "1AM", 2: "2AM", 3: "3AM", 4: "4AM", 5: "5AM", 6: "6AM",
    7: "7AM", 8: "8AM", 9: "9AM", 10: "10AM", 11: "11AM",
    12: "noon", 13: "1PM", 14: "2PM", 15: "3PM", 16: "4PM",
    17: "5PM", 18: "6PM", 19: "7PM", 20: "8PM", 21: "9PM",
    22: "10PM", 23: "11PM"
}

hour_1 = hour_mapping[time_of_day[0]]
hour_2 = hour_mapping[time_of_day[1]]

with col2:
    st.markdown(f"<p style='text-align:center; color: 'white'; font-weight: bold;'>Number of Interventions per main zone of intervention, with links to the rescue centers intervening in each zone between {hour_1} and {hour_2} for {accident_reason} reason in Paris</p>", unsafe_allow_html=True)
    paris = alt.Chart(paris).mark_geoshape(
        stroke='white'
    )

    points = alt.Chart(df_filtered).mark_circle().encode(
    longitude='longitude before departure:Q',
    latitude='latitude before departure:Q',
    size=alt.value(20), 
    tooltip=['latitude before departure:Q', 'longitude before departure:Q', 'rescue center:Q'], 
    color=alt.value('orange')
    )
    select_centroid=alt.selection_point(on="mouseover", 
                                    nearest=True,
                                    fields=["longitude centroid"],
                                    empty=False)
    centroid_points = alt.Chart(centroids).mark_point().encode(
    longitude='longitude centroid:Q',
    latitude='latitude centroid:Q',
    size=alt.Size('Number of interventions:Q'),
    color=alt.value('red'),
    ).add_params(
        select_centroid
    ).interactive()

    connections = alt.Chart(link_centroid_rc).mark_rule(opacity=0.8).encode(
        latitude="latitude before departure:Q",
        longitude="longitude before departure:Q",
        latitude2="latitude centroid:Q",
        longitude2="longitude centroid:Q",
        color=alt.value('white')
    ).transform_filter(
        select_centroid
    )
    chart = (paris + points + centroid_points)
    chart = (chart + connections).configure_legend(labelColor='white', titleColor='white')

    map_container = st.altair_chart(chart, use_container_width=True)


total_interventions = centroids['Number of interventions'].sum()
average_interventions = round(total_interventions / 12)
max_interventions = centroids['Number of interventions'].max()

# Accident details are in col3
with col3:
    st.markdown(f"<h4 style='color: 'white';'><span style='font-size: 12px;'>Total number of intervention between {hour_1} and {hour_2} for {accident_reason} reason</span><br><span style='font-size: 24px;'>{total_interventions}</span></h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: 'white';'><span style='font-size: 12px;'>Average number of intervention between {hour_1} and {hour_2} for {accident_reason} reason</span><br><span style='font-size: 24px;'>{average_interventions}</span></h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: 'white';'><span style='font-size: 12px;'>Maximum number of intervention between {hour_1} and {hour_2} for {accident_reason} reason</span><br><span style='font-size: 24px;'>{max_interventions}</span></h4>", unsafe_allow_html=True)

# Header section for this part of the dashboard
st.header("Response Time and Vehicle Emergency Analysis")

# Calculating the average delta times for each vehicle type
average_delta = df.groupby('emergency vehicle type')['delta selection-departure'].mean().reset_index()
top_average_delta = average_delta.sort_values(by='delta selection-departure', ascending=False).head(15)

# Bar chart of average delta times by emergency vehicle type
bar_chart = alt.Chart(top_average_delta).mark_bar().encode(
    x=alt.X('delta selection-departure:Q', title='Average Delta Time (s)'),
    y=alt.Y('emergency vehicle type:N', sort='-x', title='Emergency Vehicle Type'),
    color=alt.Color(field='emergency vehicle type', type='nominal', legend=None),
    tooltip=['emergency vehicle type', 'delta selection-departure']
).properties(width=350, height=400)

# Calculating the top 10 most used emergency vehicle types
top_vehicles = df['emergency vehicle type'].value_counts().nlargest(10).reset_index()
top_vehicles.columns = ['emergency vehicle type', 'count']

# Pie chart of the top 10 most used emergency vehicle types
pie_chart = alt.Chart(top_vehicles).mark_arc().encode(
    theta=alt.Theta(field='count', type='quantitative', title='Number of Dispatches'),
    color=alt.Color(field='emergency vehicle type', type='nominal', legend=alt.Legend(title="Vehicle Type")),
    tooltip=['emergency vehicle type', 'count']
).properties(width=350, height=400)

# Create two columns for the bar chart and pie chart
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Average Delta Selection-Departure Time by Vehicle Type")
    st.altair_chart(bar_chart, use_container_width=True)

with col2:
    st.subheader("Top 10 Most Used Emergency Vehicles")
    st.altair_chart(pie_chart, use_container_width=True)

st.header("Travel Time to Accident Spot")

# Conversion et préparation des données
df['selection time'] = pd.to_datetime(df['selection time'])
df['hour of day'] = df['selection time'].dt.hour

# Conversion de 'delta departure-presentation' de secondes en minutes
df['delta departure-presentation'] = df['delta departure-presentation'] / 60

average_delta_overview = df.groupby(['hour of day', 'alert reason category'])['delta departure-presentation'].mean().reset_index()

# Obtenir toutes les catégories uniques et préparer une palette de couleurs
alert_reason_categories = ['All'] + sorted(df['alert reason category'].unique().tolist())
color_palette = alt.Scale(domain=alert_reason_categories[1:],  # Exclude 'All' from the domain
                          range=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])

# Sélection par l'utilisateur
selected_alert_reason = st.selectbox('Select Alert Reason Category:', options=alert_reason_categories, index=0)

# Filtre conditionnel
if selected_alert_reason != 'All':
    filtered_data = average_delta_overview[average_delta_overview['alert reason category'] == selected_alert_reason]
else:
    filtered_data = average_delta_overview

# Création du graphique
global_view_chart = alt.Chart(filtered_data).mark_line(point=True).encode(
    x=alt.X('hour of day:O', title='Hour of Day'),
    y=alt.Y('delta departure-presentation:Q', title='Average Delta Time (minutes)'),
    color=alt.Color('alert reason category:N', scale=color_palette),
    tooltip=['hour of day', 'alert reason category', 'delta departure-presentation']
).properties(width=600, height=400).interactive()

st.altair_chart(global_view_chart, use_container_width=True)

st.markdown("<p style='color: 'white'; text-align: justify;'>Master in Data Sciences and Business Analytics - Centralesupélec & ESSEC</p>", unsafe_allow_html=True)
st.markdown("<p style='color: 'white'; text-align: justify;'>Cupillard Charlotte, Khayat Nathan, Revcolevschi Hannah, Wang Xiaoqing</p>", unsafe_allow_html=True)
