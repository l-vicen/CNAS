# 3rdParty Libraries
import streamlit as st
import pandas as pd

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

def get_db():   
    sa = gspread.service_account(st.secrets())
    sh = sa.open("CNAS_DataSet")
    worksheet = sh.get_worksheet(1)
    df_read = get_as_dataframe(worksheet)
    st.write(df_read)
    # return df_read

    # # Perform SQL query on the Google Sheet.
    # # Uses st.cache_data to only rerun when the query changes or after 10 min.
    # @st.cache_data(ttl=600)
    # def run_query(query):
    #     rows = conn.execute(query, headers=1)
    #     rows = rows.fetchall()
    #     return rows

    # sheet_url = st.secrets["private_gsheets_url"]
    # rows = run_query(f'SELECT * FROM "{sheet_url}"')

    # # Print results.
    # for row in rows:
    #     st.write(row)