# 3rdParty Libraries
import streamlit as st
import pandas as pd

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write(f"{row.name} has a :{row.pet}:")

def get_auction_summary_values():
    sa = gspread.service_account("credentials.json")
    sh = sa.open("CNAS_DataSet")
    worksheet = sh.get_worksheet(1)
    df_read = get_as_dataframe(worksheet, usecols=[0,1], nrows=20)
    st.write(df_read)
    return df_read

# def set_auction_summary_values(auction_summary_json_dictionary):
#     auction_start = auction_summary_json_dictionary.get("dtInicioProposta")
#     auction_end = auction_summary_json_dictionary.get("dtFimProposta")
#     homologated_value = auction_summary_json_dictionary.get("valorHomologadoTotal")
#     estimated_value = auction_summary_json_dictionary.get("valorEstimadoTotal")

#     pass