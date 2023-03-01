# 3rdParty Libraries
import streamlit as st
import pandas as pd

import gspread
from gspread_dataframe import get_as_dataframe
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object and config
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials) # Connection

CONNECTION =  gspread.service_account("credentials.json")
DB = CONNECTION.open("CNAS_DataSet")
WORKSHEET = DB.get_worksheet(1)

# Get Request to own built DB -> Data containing <Wallet | Credit Score>
def get_db():
    df_read = get_as_dataframe(WORKSHEET, usecols=[0,1], nrows=20)
    st.write(df_read)
    return df_read

def post_db():
    l = len(WORKSHEET.col_values(1))+1

    WORKSHEET.update_cell(l, 1, "A1")
    WORKSHEET.update_cell(l, 2,  "A2")
    WORKSHEET.update_cell(l, 3, "A3")
    WORKSHEET.update_cell(l, 4,  "A4")
    WORKSHEET.update_cell(l, 5,  "A5")
    WORKSHEET.update_cell(l, 6,  "A6")
    WORKSHEET.update_cell(l, 7,  "A7")
    WORKSHEET.update_cell(l, 8,  "A8")
    WORKSHEET.update_cell(l, 9,  "A9")
    WORKSHEET.update_cell(l, 10,  "A10")