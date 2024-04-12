import streamlit as st
import pandas as pd
import altair as alt


# Liste des raisons d'accident
accident_reasons = [
    "Vehicle Collision",
    "Pedestrian Accident",
    "Residential Fire",
    "Commercial Fire",
    "Chemical Spill",
    "Carbon Monoxide Poisoning",
    "High Fall",
    "Drowning",
    "Cardiac Arrest"
]


df_full = pd.read_csv('merged_train_mini.csv', sep=';')
df = df_full.sample(n=50000)
df.to_csv('sampled_data.csv', index=False)

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
    <h1>The journey of emergency response of the Paris Fire Brigade vehicles</h1>
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
    
    time_of_day = st.slider("Select Time of Day", 0, 24, (8, 17))
    
    rescue_center_options = ['All'] + sorted(df['rescue center'].unique().tolist())
    selected_rescue_center = st.selectbox("Select Rescue Center", options=rescue_center_options)



with col2:
    st.subheader("Map of Paris")
    # Code to create and display the map goes here
    st.map()  # placeholder for map

# Accident details are in col3
with col3:
    st.subheader("Accident Details")
    st.markdown(f"""
    **Accident Reason:** {accident_reason}
    **Time of Day:** {time_of_day}
    _Here you can include more details about the selected accident and time._
    """)

# Header section for this part of the dashboard
st.header("Response Time and Vehicle Emergency Analysis")

# Calculating the average delta times for each vehicle type
average_delta = df.groupby('emergency vehicle type')['delta selection-departure'].mean().reset_index()

# Bar chart of average delta times by emergency vehicle type
bar_chart = alt.Chart(average_delta).mark_bar().encode(
    x=alt.X('delta selection-departure:Q', title='Average Delta Time (s)'),
    y=alt.Y('emergency vehicle type:N', sort='-x', title='Emergency Vehicle Type'),
    color='emergency vehicle type:N',
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

# Footer
st.markdown("---")
st.markdown("© 2024 Emergency Response Journey Dashboard")
