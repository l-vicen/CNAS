# 3rdParty Libraries
import streamlit as st
import pandas as pd

from google.oauth2 import service_account
from gspread_dataframe import get_as_dataframe
from gsheetsdb import connect
import gspread

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

def set_auction_summary_values(auction_summary_json_dictionary):
    auction_start = auction_summary_json_dictionary.get("dtInicioProposta")
    auction_end = auction_summary_json_dictionary.get("dtFimProposta")
    homologated_value = auction_summary_json_dictionary.get("valorHomologadoTotal")
    estimated_value = auction_summary_json_dictionary.get("valorEstimadoTotal")
    pass