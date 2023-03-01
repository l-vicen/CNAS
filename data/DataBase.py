# 3rdParty Libraries
import streamlit as st
import pandas as pd
import re

from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect

# Create a connection object and config
CREDENTIALS = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets",],)

def post_db():

    connection = connect(":memory:", adapter_kwargs={
        "gsheetsapi" : { 
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
            "client_x509_cert_url" : st.secrets["gcp_service_account"]["client_x509_cert_url"]
            }
        },
    })

    cursor = connection.cursor()
    sheet_url = st.secrets["private_gsheets_url"]
    # query = f'INSERT INTO "{sheet_url}" VALUES ("{name}", "{email}", "{q1a1}", "{q1a2}", "{q1a3}")'
    query = f'INSERT INTO "{sheet_url}" VALUES ("Testing 1", "Testing 1", "Testing 1","Testing 1", "Testing 1", "Testing 1","Testing 1", "Testing 1", "Testing 1", "Testing 1")'
    cursor.execute(query)

