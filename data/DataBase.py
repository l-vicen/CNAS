# 3rdParty Libraries
import streamlit as st
import pandas as pd
import re

from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect

# Create a connection object and config
CREDENTIALS = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)

connection = connect(":memory:", adapter_kwargs={
    "gsheetaspi" : { 
    "service_account_info" : {
        "type" : st.secrets["gcp_service_account"]["type"],
        "project_id" : st.secrets["gcp_service_account"]["project_id"],
        "private_key_id" : st.secrets["gcp_service_account"]["private_key_id"],
        "private_key" : st.secrets["gcp_service_account"]["private_key"],
        "client_email" : st.secrets["gcp_service_account"]["client_email"],
        "client_id" : st.secrets["gcp_service_account"]["client_id"],
        "auth_uri" : st.secrets["gcp_service_account"]["auth_uri"],
        "token_uri" : st.secrets["gcp_service_account"]["token_uri"],
        "auth_provider_x509_cert_url" : st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url" : st.secrets["gcp_service_account"]["client_x509_cert_url"],
        }
    },
})

def run_query(query):
    rows = connection.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


def get_db():

    sheet_url = st.secrets["private_gsheets_url"]
    rows = run_query(f'SELECT * FROM "{sheet_url}"')

    # Print results.
    for row in rows:
        st.write(f"{row}:")

# def post_db():
#     cursor = connection.cursor()
#     sheet_url = st.secrets["private_gsheets_url"]
#     # query = f'INSERT INTO "{sheet_url}" VALUES ("{name}", "{email}", "{q1a1}", "{q1a2}", "{q1a3}")'
#     query = f'INSERT INTO "{sheet_url}" VALUES ("{2}", "{5}", "{6}", "{7}", "{8}")'
#     cursor.execute(query)

