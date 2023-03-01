# 3rdParty Libraries
import streamlit as st
import pandas as pd
import re

from google.oauth2 import service_account
from gsheetsdb import connect
import gspread

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ],
)
conn = connect(credentials=credentials)
client = gspread.authorize(credentials)

def get_db(): 

    @st.cache_data(ttl=600)
    def run_query(query):
        rows = conn.execute(query, headers=1)
        rows = rows.fetchall()
        return rows
    
    sheet_url = st.secrets["private_gsheets_url"]
    rows = run_query(f'SELECT * FROM "{sheet_url}"')
    st.write(pd.DataFrame(rows))

def post_db():
    database_df = database_df.astype(str)
    sheet_url = st.secrets["private_gsheets_url"] #this information should be included in streamlit secret
    sheet = client.open_by_url(sheet_url).sheet1
    sheet.update([database_df.columns.values.tolist()] + database_df.values.tolist())
    st.success('Data has been written to Google Sheets')