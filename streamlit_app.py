import pandas as pd
import numpy as np
import altair as alt

df = pd.read_csv("/Users/vivianwang/Downloads/T2/Data Viz/merged_train.csv")

# plot the Pie chart for alert reason category using altair
alert_reason = df['alert_reason_category'].value_counts().reset_index()
alert_reason.columns = ['alert_reason_category', 'count']
alert_reason_chart = alt.Chart(alert_reason).mark_bar().encode(
    x='count',
    y=alt.Y('alert_reason_category', sort='-x')
)
alert_reason_chart



