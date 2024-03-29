# Libraries
import streamlit as st
import data.DataBase as DataBase

# UI of the Get Data Feature
def get_data_set_view():
    st.title("GET: Data Set")
    st.info("This page displays the ComprasNet's data set constructed during the thesis period.")
    st.markdown("---")
    st.write(DataBase.get_db())
    st.markdown("---")