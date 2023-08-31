import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout='wide'
)
col, col1, col2 = st.columns([1,1,1])
with col1:
    st.write("# Welcome to our Vivino Query Page! 👋")


st.sidebar.success("Select a page above.")