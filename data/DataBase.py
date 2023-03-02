# 3rdParty Libraries
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect

# Credential setting to access the private Google Sheet Data Set
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)

"""

Default way to access the private information on the credentials to access the Google Sheet Data Set.

Via st.secrets["gcp_service_account"] I store private credential info on a file .streamlit/secrets.toml 
that it is used on the hosting side (Streamlit Cloud) to establish communication between app and data set
without disclosing critical information.

"""
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
        "client_x509_cert_url" : st.secrets["gcp_service_account"]["client_x509_cert_url"],
        }
    },
})

# Establishing the connection
CURSOR = connection.cursor()

# URL of private Google Sheet
SHEET_URL = st.secrets["private_gsheets_url"]

"""
get_db() uses shillelagh lib to perform a common get
request in SQL & Python. Here, I retrive all Tuples from the
Google Sheet (A Tuple is a single row in the data set). Then,
I convert the tuples to a dataframe.
"""
def get_db():
    query = f'SELECT * FROM "{SHEET_URL}"'
    rows = CURSOR.execute(query)
    df = pd.DataFrame(rows, columns = ['Auction_Id', 'Start_Date',
                                  'End_Date', 'Total_Estimated_Price',
                                  'Total_Homologated_Price', 'Items_Auctioned',
                                  'Winning_Bids', 'Suppliers_Winner_ID',
                                  'History_Bids_Items', 'History_Bids_Date'])
    return df

"""
post_db() uses shillelagh lib to perform a "writing" operation to 
the data set. It inserts, the target data from ComprasNet into the 
Google Sheet. 

One row in the Google Sheet represents one Auction lot, one Auction 
can have multiple lots.

"""
def post_db():
    # query = f'INSERT INTO "{sheet_url}" VALUES ("{name}", "{email}", "{q1a1}", "{q1a2}", "{q1a3}")'
    query = f'INSERT INTO "{SHEET_URL}" VALUES ("{"Testing 1"}", "{"Testing 1"}", "{"Testing 1"}","{"Testing 1"}", "{"Testing 1"}", "{"Testing 1"}","{"Testing 1"}", "{"Testing 1"}", "{"Testing 1"}", "{"Testing 1"}")'
    CURSOR.execute(query)


