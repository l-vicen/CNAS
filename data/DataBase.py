# 3rdParty Libraries
import streamlit as st
import pandas as pd
import re

from google.oauth2 import service_account
from gsheetsdb import connect
# from shillelagh.backends.apsw.db import connect

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
connection = connect(credentials=credentials)

def run_query(query):
    rows = connection.execute(query, headers=1)
    rows = rows.fetchall()
    st.write(rows)
    return rows

def get_db():

    sheet_url = st.secrets["private_gsheets_url"]
    rows = run_query(f'SELECT * FROM "{sheet_url}"')

    # Print results.
    for row in rows:
        st.write(row)

# def post_db():
#     cursor = connection.cursor()
#     sheet_url = st.secrets["private_gsheets_url"]
#     # query = f'INSERT INTO "{sheet_url}" VALUES ("{name}", "{email}", "{q1a1}", "{q1a2}", "{q1a3}")'
#     query = f'INSERT INTO "{sheet_url}" VALUES ("{2}", "{5}", "{6}", "{7}", "{8}")'
#     cursor.execute(query)

