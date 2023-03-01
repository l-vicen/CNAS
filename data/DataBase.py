# 3rdParty Libraries
import streamlit as st
import pandas as pd
import re

from google.oauth2 import service_account
from gspread_dataframe import get_as_dataframe
from gsheetsdb import connect
import gspread

# Create a connection object and config
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials) # Connection
client = gspread.authorize(credentials)

# Get Request to own built DB -> Data containing <Wallet | Credit Score>
def get_db():
    sa = gspread.service_account()
    sh = sa.open("CNAS_DataSet")
    worksheet = sh.get_worksheet(1)
    df_read = get_as_dataframe(worksheet)
    st.write(df_read)
    return df_read
