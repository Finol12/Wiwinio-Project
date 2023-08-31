import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

connection = sqlite3.connect('../data/vivino.db')
cursor = connection.cursor()

query = """
    SELECT wines.id AS wine_id, 
           wines.name AS wine_name, 
           wines.ratings_average AS wine_avg_rating, 
           wines.ratings_count AS wine_ratings_count, 
           COUNT(vintages.year) AS vintages_number, 
           ROUND(AVG(vintages.price_euros), 2) AS average_price,
           countries.name AS country_name
    FROM wines
        JOIN vintages ON wines.id = vintages.wine_id
        JOIN regions ON wines.region_id = regions.id
        JOIN countries ON regions.country_code = countries.code
    WHERE wines.ratings_count > 10000
    GROUP BY wines.id
    ORDER BY wine_avg_rating DESC, wine_ratings_count DESC;
"""
query = pd.read_sql_query(query, connection)

query2 = """
    SELECT wines.id AS wine_id, 
           wines.name AS wine_name, 
           wines.ratings_average wine_avg_rating, 
           wines.ratings_count wine_ratings_count, 
           COUNT(vintages.year) AS vintages_number, 
           ROUND(AVG(vintages.price_euros), 2) AS average_price,
           countries.name AS country_name
    FROM wines
        JOIN vintages ON wines.id = vintages.wine_id
        JOIN regions ON wines.region_id = regions.id
        JOIN countries ON regions.country_code = countries.code
    WHERE vintages.price_euros <= 50 AND
          wines.ratings_count > 10000 
    GROUP BY wines.id
    ORDER BY wine_avg_rating DESC, 
             wine_ratings_count DESC,
             vintages.price_euros ASC
    -- LIMIT 10
    ;
"""

query2 = pd.read_sql_query(query2, connection)

st.set_page_config(layout='wide')

col1, col2 = st.columns([1,1])
with col1:
    st.write('# Most expensive')
    st.dataframe(query)
with col2:
    st.write('# Least expensive')
    st.dataframe(query2)