from altair import value
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

connection = sqlite3.connect('.././data/vivino.db')
cursor = connection.cursor()

query_5_tastes_clean = """
    SELECT wines.id AS wine_id,
           wines.name AS wine_name,
           wines.ratings_average AS rating,
           keywords.name || ' (' || keywords_wine.group_name || ')' AS group_flavor
    FROM keywords_wine
        JOIN keywords on keywords_wine.keyword_id = keywords.id
        JOIN flavor_groups on keywords_wine.group_name = flavor_groups.name
        JOIN wines on keywords_wine.wine_id = wines.id
    WHERE keywords.name IN ("coffee", "toast", "green apple", "cream", "citrus") AND
          keywords_wine.group_name <> "non_oak" AND
          keywords_wine.count > 10
    ORDER BY wine_id ASC, group_flavor ASC
    ;
"""
query_result = pd.read_sql_query(query_5_tastes_clean, connection)
flavor_count_per_wine = query_result\
    .groupby(["wine_id", "wine_name", "rating"])[["group_flavor"]]\
    .agg(lambda x: ', '.join(x))
flavor_count_per_wine = flavor_count_per_wine.reset_index()
flavor_count_per_wine = flavor_count_per_wine.set_index("wine_id")
flavor_count_per_wine["flavor_count"] = flavor_count_per_wine["group_flavor"].apply(lambda x: len(x.split(", ")))

wines_per_taste = flavor_count_per_wine.groupby("group_flavor")[["wine_name"]].count()
wines_per_taste = wines_per_taste.reset_index()
wines_per_taste.columns = ["combo", "wine_count"]
wines_per_taste = wines_per_taste.sort_values("wine_count", ascending=False)

wines_per_taste_top5 = wines_per_taste.iloc[0:5,:]

new_row = {'combo': ['others'], 'wine_count': [sum(wines_per_taste.iloc[5:,1])]}
wines_per_taste_others = pd.DataFrame(new_row)
wines_per_taste_top5_rest = pd.concat([wines_per_taste_top5, wines_per_taste_others])

st.set_page_config(layout='wide')
col1, col2 = st.columns([1,1])
col1.write('# Query Dataframes')
col2.write('# Graph')

with col1:
    fig = px.pie(
        wines_per_taste_top5_rest,
        values='wine_count',
        names='combo'
        )
    st.dataframe(flavor_count_per_wine.reset_index(), use_container_width=True)
with col2:
    st.plotly_chart(fig, use_container_width=True)
