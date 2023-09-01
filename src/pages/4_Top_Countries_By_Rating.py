import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

connection = sqlite3.connect('.././data/vivino.db')
cursor = connection.cursor()

cursor.execute ('''
    SELECT
        countries.name AS country,
        ROUND(AVG(wines.ratings_average), 2) AS hra,
        wines.ratings_count AS rating
    FROM
        countries
        JOIN regions ON countries.code = regions.country_code
        --JOIN toplists ON countries.code = toplists.country_code
        --JOIN vintage_toplists_rankings on toplists.id = vintage_toplists_rankings.top_list_id
        JOIN wines ON regions.id = wines.region_id
        JOIN vintages on wines.id = vintages.wine_id
    GROUP BY
        country
    ORDER BY
        rating DESC;
''')
query_result = cursor.fetchall()

query_result = pd.DataFrame(query_result)
query_result = query_result.rename(columns={0: 'Country Name', 1:'Average Rating', 2:'Rating Count'})

cursor.execute ('''
    SELECT
        countries.name as country,
        ROUND(AVG(vintages.ratings_average), 2) AS hra,
        vintages.ratings_count as rating
    FROM
        countries
        JOIN regions ON countries.code = regions.country_code
        --JOIN toplists ON countries.code = toplists.country_code
        --JOIN vintage_toplists_rankings on toplists.id = vintage_toplists_rankings.top_list_id
        JOIN wines ON regions.id = wines.region_id
        JOIN vintages on wines.id = vintages.wine_id
    GROUP BY
        country
    ORDER BY
        rating DESC;
''')
query_result2 = cursor.fetchall()
query_result2 = pd.DataFrame(query_result2)
query_result2 = query_result2.rename(columns={0: 'Country Name', 1:'Average Rating', 2:'Rating Count'})
st.set_page_config(layout='wide')
col1, col2 = st.columns([1,2])
col1.write('# Query Dataframes')
col2.write('# Graphs')

with col1:
    fig = px.scatter(
        query_result2, 
        x='Country Name', 
        y='Average Rating',
        size=query_result2['Rating Count'],
        color_discrete_sequence=['red']
        )
    st.write('Vintage Ratings per Country Dataframe')
    st.dataframe(query_result2, use_container_width=True)
    st.write('Wine Ratings per Country Dataframe')
    st.dataframe(query_result, use_container_width=True)
with col2:    
    fig2 = px.scatter(
        query_result, 
        x='Country Name', 
        y='Average Rating', 
        size=query_result['Rating Count'],
        color_discrete_sequence=['purple'] 
        )
    st.write('Vintage Ratings per Country Graph (Size=Rating Count)')
    st.plotly_chart(fig, use_container_width=True)
    st.write('Wine Ratings per Country Graph (Size=Rating Count)')
    st.plotly_chart(fig2, use_container_width=True)

