import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

connection = sqlite3.connect('.././data/vivino.db')
cursor = connection.cursor()

query = """
    SELECT wines.id AS WineID, 
           wines.name AS Name, 
           wines.ratings_average AS Average_Rating, 
           wines.ratings_count AS Popularity, 
           ROUND(AVG(vintages.price_euros), 2) AS Average_Price,
           countries.name AS Country
    FROM wines
        JOIN vintages ON wines.id = vintages.wine_id
        JOIN regions ON wines.region_id = regions.id
        JOIN countries ON regions.country_code = countries.code
    WHERE wines.ratings_count > 10000
    GROUP BY WineID
    ORDER BY Average_Rating DESC, Popularity DESC
    LIMIT 10;
"""
query = pd.read_sql_query(query, connection)

query2 = """
    SELECT wines.id AS WineID, 
           wines.name AS Name, 
           wines.ratings_average Average_Rating, 
           wines.ratings_count Popularity, 
           ROUND(AVG(vintages.price_euros), 2) AS Average_Price,
           countries.name AS Country
    FROM wines
        JOIN vintages ON wines.id = vintages.wine_id
        JOIN regions ON wines.region_id = regions.id
        JOIN countries ON regions.country_code = countries.code
    WHERE vintages.price_euros <= 50 AND
          wines.ratings_count > 10000 
    GROUP BY WineID
    ORDER BY Average_Rating DESC, 
             Popularity DESC,
             Average_Price ASC
    LIMIT 10
    ;
"""

query2 = pd.read_sql_query(query2, connection)

st.set_page_config(layout='wide')
col1, col2 = st.columns([1,2])
with col1:
    st.write(' ')
with col2:
    st.write('# Special Occasion Wines')
    st.dataframe(query)
    st.write('# Everyday Favorite Wines')
    st.dataframe(query2)