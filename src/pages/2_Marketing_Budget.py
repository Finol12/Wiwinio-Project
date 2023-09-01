from altair import LayoutAlign
from matplotlib.font_manager import weight_dict
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

connection = sqlite3.connect('.././data/vivino.db')
cursor = connection.cursor()

query = """
SELECT wines.name || ' (' || countries.name || ')' AS Name, 
       wines.id AS WineID, 
       AVG(vintages.price_euros) AS Price,
       SUM(vintages.ratings_count) AS Popularity,
       AVG(vintages.ratings_average) AS Average_Rating
FROM wines
JOIN vintages ON wines.id = vintages.wine_id
JOIN regions ON wines.region_id = regions.id
JOIN countries ON regions.country_code = countries.code
GROUP BY wines.name, wines.id
ORDER BY  Popularity DESC, Price ASC, Average_Rating DESC
LIMIT 10;
"""
query = pd.read_sql_query(query, connection)

query2 = """
SELECT countries.name AS Country, 
       AVG(wines.ratings_average) AS Average_Rating, 
       COUNT(wines.id) AS Wine_Count,
       SUM(wines.ratings_count) AS Popularity,
       (AVG(wines.ratings_average) * COUNT(wines.id)) AS Impact_Score
FROM countries
JOIN regions ON countries.code = regions.country_code
JOIN wines ON regions.id = wines.region_id
GROUP BY countries.name
ORDER BY Impact_Score DESC;
"""

query2 = pd.read_sql_query(query2, connection)

impact_top3 = query2.iloc[0:3,:]

new_row = {'Country': ['Others'], 'Impact_Score': [sum(query2.iloc[3:,1])]}
impact_others = pd.DataFrame(new_row)
impact_top3_rest = pd.concat([impact_top3, impact_others])

st.set_page_config(layout='wide')

fig2 = px.bar(
        impact_top3_rest,
        x='Country',
        y='Impact_Score',
        height=(500),
        width=(500)
        )


col1, col2= st.columns([1,1])
col1.write('# Query Dataframes')
col2.write('# Graph')
 

with col1:
    fig = px.scatter(
        query,
        x='Name',
        y='Popularity',
        color_discrete_sequence=['yellow'],
        size='Price',
        width=(900)
        )
    #fig.update_layout(yaxis_range=[0, 15])
    

    st.write('# Impact Score per Country')
    st.dataframe(query2, use_container_width=True)
    st.dataframe(query, use_container_width=True)
with col2:
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.plotly_chart(fig2, use_container_width=True)
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.plotly_chart(fig, use_container_width=False)