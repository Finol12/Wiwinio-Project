import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

connection = sqlite3.connect('../data/vivino.db')
cursor = connection.cursor()

cursor.execute ('''
    SELECT
        wines.name AS name,
        ROUND(AVG(wines.ratings_average), 2) AS hra,
        wines.id AS id,
        wines.ratings_count AS count,
        vintages.year,
        vintages.price_euros
    FROM
        countries
        JOIN regions ON countries.code = regions.country_code
        JOIN wines ON regions.id = wines.region_id
        JOIN vintages on wines.id = vintages.wine_id
    WHERE 
        wines.ratings_count > 1000 AND wines.name 
    LIKE 
        '%Sauvignon%' 
    GROUP BY
        wines.id
    ORDER BY
        hra DESC, count DESC
    LIMIT 10;
''')
query_result = cursor.fetchall()

query_result = pd.DataFrame(query_result)
query_result.columns=['Wine', 'Rating', 'ID', 'Count', 'Year', 'Price']

st.set_page_config(layout='wide')
col1, col2 = st.columns([1,2])
col1.write('# Query Dataframes')
col2.write('# Graphs')

with col1:
    fig = px.scatter(
        query_result, 
        x='Wine', 
        y='Rating',
        size=query_result['Price'],
        color_discrete_sequence=['yellow']
        )
    st.write('Vintage Ratings per Country Dataframe')
    st.dataframe(query_result, use_container_width=True)
with col2:
    st.write('Vintage Ratings per Country Graph (Size=Rating Count)')
    st.plotly_chart(fig, use_container_width=True)
