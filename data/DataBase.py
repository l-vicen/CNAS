# 3rdParty Libraries
import streamlit as st
import pandas as pd

from google.oauth2 import service_account
from gspread_dataframe import get_as_dataframe
from gsheetsdb import connect
import gspread

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

def get_sheet():
    sa = gspread.service_account("credentials.json")
    sh = sa.open("CNAS_DataSet")
    worksheet = sh.get_worksheet(1)
    df_read = get_as_dataframe(worksheet, usecols=[0,1], nrows=20)
    st.write(df_read)
    return df_read

def set_auction_summary_values(auction_summary_json_dictionary):
    auction_start = auction_summary_json_dictionary.get("dtInicioProposta")
    auction_end = auction_summary_json_dictionary.get("dtFimProposta")
    homologated_value = auction_summary_json_dictionary.get("valorHomologadoTotal")
    estimated_value = auction_summary_json_dictionary.get("valorEstimadoTotal")
    pass