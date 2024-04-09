import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

df = pd.read_csv('data/merge_train_mini.csv')
'''
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
'''

