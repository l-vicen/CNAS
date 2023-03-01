# 3rdParty Libraries
import streamlit as st
import pandas as pd

from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
CREDENTIALS = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
CONNECTION = connect(credentials=CREDENTIALS)

def run_get_query(query):
    rows = CONNECTION.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

def run_post_query(query):
    rows = CONNECTION.execute(query, headers=1)

def get_db():
    sheet_url = st.secrets["private_gsheets_url"]
    rows = run_get_query(f'SELECT * FROM "{sheet_url}"')
    dataframe = pd.DataFrame(list(rows))
    return dataframe

def insert_row_db():
    sheet_url = st.secrets["private_gsheets_url"]
    run_post_query(f'INSERT INTO "{sheet_url}" (Auction_Id,\
                                                  Start_Date,\
                                             	  End_Date,\
                                          	      Total_Estimated_Price,\
                                                  Total_Homologated_Price,\
                     	                          Items_Auctioned,\
                                            	  Winning_Bids,\
                                                  Suppliers_Winner_ID,\
                                                  History_Bids_Items,\
                     	                          History_Bids_Date)\
                       VALUES                     ("{10}",\
                                                   "{11}",\
                                             	   "{12}",\
                                          	       "{13}",\
                                                   "{14}",\
                     	                           "{15}",\
                                            	   "{16}",\
                                                   "{17}",\
                                                   "{18}",\
                     	                           "{19}")')