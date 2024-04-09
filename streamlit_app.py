
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

df = pd.read_csv("/Users/vivianwang/Downloads/T2/Data Viz/merged_train.csv")

# Pie chart for alert reason category
df['alert reason category'].value_counts().plot.pie(autopct='%1.1f%%')
plt.axis('equal')
plt.title('Alert Reason Category')
plt.show()

# Pie chart for vehicle type
df['emergency vehicle type'].value_counts().plot.pie(autopct='%1.1f%%')
plt.axis('equal')
plt.title('Emergency Vehicle Type')
plt.show()

