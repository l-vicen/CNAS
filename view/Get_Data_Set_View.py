import streamlit as st
import data.DataBase as DataBase

def get_data_set_view():
    st.title("GET: Data Set")
    st.info("This page displays the ComprasNet's data set constructed during the thesis period.")
    # st.write(DataBase.get_db())