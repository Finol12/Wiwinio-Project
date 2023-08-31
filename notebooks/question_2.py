import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

connection = sqlite3.connect('../data/vivino.db')
cursor = connection.cursor()

query = """
SELECT wines.name, wines.id, AVG(vintages.price_euros) AS price,
       SUM(vintages.ratings_count) AS rating_count,
       AVG(vintages.ratings_average) AS avg_rating,
       countries.name AS country_name
FROM wines
JOIN vintages ON wines.id = vintages.wine_id
JOIN regions ON wines.region_id = regions.id
JOIN countries ON regions.country_code = countries.code
GROUP BY wines.name, wines.id
ORDER BY  rating_count DESC, AVG(vintages.price_euros) ASC, avg_rating DESC
LIMIT 10;
"""
query = pd.read_sql_query(query, connection)


st.set_page_config(layout='wide')
col1, col2 = st.columns([1,2])
col1.write('# Query Dataframes')
col2.write('# Graph')

with col1:
    fig = px.scatter(
        query,
        x='name',
        y='avg_rating',
        color_discrete_sequence=['yellow'],
        size='price'
        )
    fig.update_layout(yaxis_range=[0, 15])
    st.dataframe(query, use_container_width=True)
with col2:
    st.plotly_chart(fig, use_container_width=True)