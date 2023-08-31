from altair import LayoutAlign
from matplotlib.font_manager import weight_dict
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

connection = sqlite3.connect('../data/vivino.db')
cursor = connection.cursor()

query = """
SELECT wines.name || ' (' || countries.name || ')' AS name, 
       wines.id, 
       AVG(vintages.price_euros) AS price,
       SUM(vintages.ratings_count) AS rating_count,
       AVG(vintages.ratings_average) AS avg_rating
FROM wines
JOIN vintages ON wines.id = vintages.wine_id
JOIN regions ON wines.region_id = regions.id
JOIN countries ON regions.country_code = countries.code
GROUP BY wines.name, wines.id
ORDER BY  rating_count DESC, AVG(vintages.price_euros) ASC, avg_rating DESC
LIMIT 10;
"""
query = pd.read_sql_query(query, connection)

query2 = """
SELECT countries.name AS country_name, 
       AVG(wines.ratings_average) AS avg_rating, 
       COUNT(wines.id) AS wine_count,
       SUM(wines.ratings_count) AS count_rating,
       (AVG(wines.ratings_average) * COUNT(wines.id)) AS impact_score
FROM countries
JOIN regions ON countries.code = regions.country_code
JOIN wines ON regions.id = wines.region_id
GROUP BY countries.name
ORDER BY impact_score DESC;
"""

query2 = pd.read_sql_query(query2, connection)

impact_top3 = query2.iloc[0:3,:]

new_row = {'country_name': ['others'], 'impact_score': [sum(query2.iloc[3:,1])]}
impact_others = pd.DataFrame(new_row)
impact_top3_rest = pd.concat([impact_top3, impact_others])

st.set_page_config(layout='wide')

fig2 = px.pie(
        impact_top3_rest,
        values='impact_score',
        names='country_name',
        height=(700),
        width=(1000)
        )


col1, col2= st.columns([1,1])
col1.write('# Query Dataframes')
col2.write('# Graph')
 

with col1:
    fig = px.scatter(
        query,
        x='name',
        y='rating_count',
        color_discrete_sequence=['yellow'],
        size='price'
        )
    #fig.update_layout(yaxis_range=[0, 15])
    st.dataframe(query, use_container_width=True)
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.plotly_chart(fig2, use_container_width=False)
with col2:
    st.plotly_chart(fig, use_container_width=True)
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write('# Impact Score per Country')
    st.dataframe(query2, use_container_width=True)