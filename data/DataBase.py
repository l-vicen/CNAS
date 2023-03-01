# 3rdParty Libraries
import streamlit as st
import pandas as pd

from gspread_dataframe import get_as_dataframe

def get_db(sa):
    sh = sa.open("CNAS_DataSet")
    worksheet = sh.get_worksheet(1)
    df_read = get_as_dataframe(worksheet)
    return df_read