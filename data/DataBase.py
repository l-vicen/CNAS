# 3rdParty Libraries
import streamlit as st
import pandas as pd

from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
def get_db():

    conn = connect(credentials=credentials)

    @st.cache(ttl=600)
    def run_query(query):
        rows = conn.execute(query, headers=1)
        return rows

    sheet_url = st.secrets["private_gsheets_url"]
    rows = run_query(f'SELECT * FROM "{sheet_url}"')

    tickers = []
    for row in rows:
        tickers.append(f"{row.ticker}")

    return tickers