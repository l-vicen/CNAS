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
    sheet_id = re.search('/d/(.+?)/edit?', st.secrets["private_gsheets_url"]).group(1)
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    st.write(csv_url)
    df =  pd.read_csv(csv_url)
    st.write(df)
    return df

def post_db():
    database_df = database_df.astype(str)
    sheet_url = st.secrets["private_gsheets_url"] #this information should be included in streamlit secret
    sheet = client.open_by_url(sheet_url).sheet1
    sheet.update([database_df.columns.values.tolist()] + database_df.values.tolist())
    st.success('Data has been written to Google Sheets')