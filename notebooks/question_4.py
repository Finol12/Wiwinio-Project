import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

connection = sqlite3.connect('../data/vivino.db')
cursor = connection.cursor()


query_grapes = """
    SELECT grapes.name, 
           COUNT(most_used_grapes_per_country.country_code) AS total
           -- SUM(most_used_grapes_per_country.wines_count) AS total_wines
           -- AVG(most_used_grapes_per_country.wines_count) AS total_wines
    FROM grapes
        JOIN most_used_grapes_per_country ON grapes.id = most_used_grapes_per_country.grape_id
    GROUP BY most_used_grapes_per_country.grape_id
    ORDER BY total DESC
    LIMIT 10
    ;
"""

df_grapes = pd.read_sql_query(query_grapes, connection)
df_grapes.columns=['Grape Name', 'Total Used/Country']
df_grapes2 = df_grapes.head(3)
st.set_page_config(layout='wide')
col1, col2 = st.columns([1,2])
col1.write('# Query Dataframes')
col2.write('# Graph')

with col1:
    fig = px.bar(
        df_grapes2,
        x=df_grapes2['Grape Name'],
        y=df_grapes2['Total Used/Country'],
        color_discrete_sequence=['red'],
        height=(480)
        )
    fig.update_layout(yaxis_range=[0, 15])
    st.write('## TOP 10 Used Grapes per Country')
    st.dataframe(df_grapes, use_container_width=True)
with col2:
    st.write('## TOP 3 Used Grapes per Country')
    st.plotly_chart(fig, use_container_width=True)
