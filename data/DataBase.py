# 3rdParty Libraries
import streamlit as st
import pandas as pd

from google.oauth2 import service_account
from gsheetsdb import connect

def get_db():

    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    )
    conn = connect(credentials=credentials)
    
    def run_query(query):
        rows = conn.execute(query, headers=1)
        rows = rows.fetchall()
        return rows

    sheet_url = st.secrets["private_gsheets_url"]
    rows = run_query(f'SELECT * FROM "{sheet_url}"')

    dataframe = pd.DataFrame(list(rows))
    st.write(dataframe)
    return dataframe