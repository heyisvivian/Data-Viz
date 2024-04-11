
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

df = pd.read_csv('merged_train_mini.csv')

'''Emergency Vehicle Response Time Analysis'''
col1, col2 = st.columns(2)

#plot the pie chart of emergency vehicle type (top 10) with the color representing the time 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

avg_deltas = df.groupby('emergency vehicle type')['delta selection-presentation'].mean()
top_10_types = df['emergency vehicle type'].value_counts().head(10).index
top_10_avg_deltas = avg_deltas.loc[top_10_types]
norm = mcolors.Normalize(vmin=top_10_avg_deltas.min(), vmax=top_10_avg_deltas.max())
cmap = plt.cm.Reds
colors = [cmap(norm(value)) for value in top_10_avg_deltas]
fig1, ax1 = plt.subplots()
explode = [0.05] * 10  
patches, texts, autotexts = ax1.pie(
    df['emergency vehicle type'].value_counts().head(10),
    labels=top_10_types,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    explode=explode,
    textprops={'fontsize': 9}  
)
for text in texts + autotexts:
    text.set_color('white')  
ax1.legend(patches, top_10_types, title="Vehicle Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
ax1.set_title('Top 10 Emergency Vehicle Types', fontsize=14)
plt.show()
with col1:
    st.pyplot(fig1)
    
#plot the pie chart of alart reason category with color representing the time
fig2, ax = plt.subplots(figsize=(10, 6))
df['alert reason category'].value_counts().nlargest(5).plot.pie(autopct='%1.1f%%', ax=ax)
ax.set_title('Alert Reason Category Top 5')
with col2:
    st.pyplot(fig2)

