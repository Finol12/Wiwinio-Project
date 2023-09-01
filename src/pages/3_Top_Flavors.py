from altair import value
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

connection = sqlite3.connect('.././data/vivino.db')
cursor = connection.cursor()

query_5_tastes_clean = """
    SELECT wines.id AS WineID,
           wines.name AS Name,
           wines.ratings_average AS Average_Rating,
           keywords.name || ' (' || keywords_wine.group_name || ')' AS Group_Flavor
    FROM keywords_wine
        JOIN keywords on keywords_wine.keyword_id = keywords.id
        JOIN flavor_groups on keywords_wine.group_name = flavor_groups.name
        JOIN wines on keywords_wine.wine_id = wines.id
    WHERE keywords.name IN ("coffee", "toast", "green apple", "cream", "citrus") AND
          keywords_wine.group_name <> "non_oak" AND
          keywords_wine.count > 10
    ORDER BY WineID ASC, Group_Flavor ASC
    ;
"""
query_result = pd.read_sql_query(query_5_tastes_clean, connection)
flavor_count_per_wine = query_result\
    .groupby(["WineID", "Name", "Average_Rating"])[["Group_Flavor"]]\
    .agg(lambda x: ', '.join(x))
flavor_count_per_wine = flavor_count_per_wine.reset_index()
flavor_count_per_wine = flavor_count_per_wine.set_index("WineID")
flavor_count_per_wine["Flavor_Count"] = flavor_count_per_wine["Group_Flavor"].apply(lambda x: len(x.split(", ")))

wines_per_taste = flavor_count_per_wine.groupby("Group_Flavor")[["Name"]].count()
wines_per_taste = wines_per_taste.reset_index()
wines_per_taste.columns = ["combo", "wine_count"]
wines_per_taste = wines_per_taste.sort_values("wine_count", ascending=False)

wines_per_taste_top5 = wines_per_taste.iloc[0:5,:]

new_row = {'combo': ['others'], 'wine_count': [sum(wines_per_taste.iloc[5:,1])]}
wines_per_taste_others = pd.DataFrame(new_row)
wines_per_taste_top5_rest = pd.concat([wines_per_taste_top5, wines_per_taste_others])

st.set_page_config(layout='wide')
col1,col, col2 = st.columns([2,1,2])
col1.write('# Wines with taste combos')
col2.write('# Top 5 combos')

with col1:
    fig = px.pie(
        wines_per_taste_top5_rest,
        values='wine_count',
        names='combo',
        height=(500),
        width=(800)
        )
    st.dataframe(flavor_count_per_wine.reset_index(), use_container_width=True)
with col2:
    st.plotly_chart(fig, use_container_width=False)
