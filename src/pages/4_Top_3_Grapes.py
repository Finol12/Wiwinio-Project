import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

connection = sqlite3.connect('.././data/vivino.db')
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
query_sauvignon = ('''
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
    LIMIT 5;
''')
query_sauvignon = pd.read_sql_query(query_sauvignon, connection)
query_sauvignon.columns=['Wine', 'Rating', 'ID', 'Count', 'Year', 'Price']

query_merlot = ('''
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
        wines.ratings_count > 1 AND wines.name 
    LIKE 
        '%Merlot%' 
    GROUP BY
        wines.id
    ORDER BY
        hra DESC, count DESC
    LIMIT 5;
''')
query_merlot = pd.read_sql_query(query_merlot, connection)
query_merlot.columns=['Wine', 'Rating', 'ID', 'Count', 'Year', 'Price']

query_chardonnay = ('''
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
        wines.ratings_count > 1 AND wines.name 
    LIKE 
        '%Chardonnay%' 
    GROUP BY
        wines.id
    ORDER BY
        hra DESC, count DESC
    LIMIT 5;
''')
query_chardonnay = pd.read_sql_query(query_chardonnay, connection)
query_chardonnay.columns=['Wine', 'Rating', 'ID', 'Count', 'Year', 'Price']


df_grapes = pd.read_sql_query(query_grapes, connection)
df_grapes.columns=['Grape Name', 'Total Used/Country']

grapes_top3 = df_grapes.iloc[0:3,:]

new_row = {'Grape Name': ['others'], 'Total Used/Country': [sum(df_grapes.iloc[3:,1])]}
grapes_others = pd.DataFrame(new_row)
grapes_top3_rest = pd.concat([grapes_top3, grapes_others])

#df_grapes2 = df_grapes.head(3)
st.set_page_config(layout='wide')
col1, col2 = st.columns([1,2])
col1.write('# Query Dataframes')
col2.write('# Graph')

with col1:
    fig = px.pie(
        grapes_top3_rest,
        values=grapes_top3_rest['Total Used/Country'],
        names=grapes_top3_rest['Grape Name'],
        height=(350)
        )
    fig2 = px.scatter(
        query_sauvignon,
        x='Wine',
        y='Rating',
        color_discrete_sequence=['orange'],
        size='Price',
        height=(280)
        )
    fig3 = px.scatter(
        query_merlot,
        x='Wine',
        y='Rating',
        color_discrete_sequence=['pink'],
        size='Price',
        height=(280)
        )
    fig4 = px.scatter(
        query_chardonnay,
        x='Wine',
        y='Rating',
        color_discrete_sequence=['white'],
        size='Price',
        height=(280)
        )
    fig.update_layout(yaxis_range=[0, 15])
    st.write('## TOP 10 Used Grapes per Country')
    st.dataframe(df_grapes, use_container_width=True)
    st.write('Top Wines: Cabernet Sauvignon')
    st.dataframe(query_sauvignon, use_container_width=True)
    st.write('Top Wines: Merlot')
    st.dataframe(query_merlot, use_container_width=True)
    st.write('Top Wines: Chardonnay')
    st.dataframe(query_chardonnay, use_container_width=True)
with col2:
    st.write('## TOP 3 Used Grapes per Country')
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)
