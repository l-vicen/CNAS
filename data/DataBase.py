# 3rdParty Libraries
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect
import re

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

# Name of the columns in the google sheet
GOOGLE_SHEET_COLUMNS = ['Auction_Id', 
                        'Start_Date',
                        'End_Date',
                        'Total_Estimated_Price',
                        'Total_Homologated_Price',
                        'Number_Items_Auctioned',
                        'Items_Auctioned',
                        'Demanded_Quantity_Items',
                        'Estimated_Price_Items',
                        'Winning_Bids',
                        'Winner_Supplier_Id',
                        'Participating_Suppliers',
                        'Items_Bid_History',
                        'Dates_Bid_History']

"""
get_db() uses shillelagh lib to perform a common get
request in SQL & Python. Here, I retrive all Tuples from the
Google Sheet (A Tuple is a single row in the data set). Then,
I convert the tuples to a dataframe.
"""
def get_db():
    query = f'SELECT * FROM "{SHEET_URL}"'
    rows = CURSOR.execute(query)
    df = pd.DataFrame(rows, columns = GOOGLE_SHEET_COLUMNS)
    return df

"""
post_db() uses shillelagh lib to perform a "writing" operation to 
the data set. It inserts, the target data from ComprasNet into the 
Google Sheet. 

One row in the Google Sheet represents one Auction lot, one Auction 
can have multiple lots.

"""
def post_db(auction_id, auction_summary, auction_items, auction_history):

    """ 1st Part: Getting data from auction_items query """

    # Variable to avoid re-accessing the inside of the auction_items json multiple times
    pregoes = auction_items["_embedded"]["pregoes"]
    length_pregoes = len(pregoes)

    # Creating a list with all auctioned items in the auction
    Items_Auctioned = [pregoes[i]["descricao_item"].rstrip() for i in range(length_pregoes)]

    # Creating a list with the demanded quantity for item
    Demanded_Quantity_Items = [int(pregoes[i]["quantidade_item"]) for i in range(length_pregoes)]

    # Creating a list with the estimated price for items
    Estimated_Price_Items = [float(pregoes[i]["valor_estimado_item"]) for i in range(length_pregoes)]

    # Creating a list with all winning bids (smallest) prices
    Winning_Bids = [float(pregoes[i]["menor_lance"]) if pregoes[i]["menor_lance"] != None else -1 for i in range(length_pregoes)]

    """ 2nd Part: Getting data from auction_items query """

    # Variable to avoid re-accessing the inside of the auction_history json multiple times
    auction_history = auction_history["_embedded"]["pregoes"]
    length_auction_history = len(auction_history)

    #  Creating a list with all participating suppliers
    Participating_Suppliers = [auction_history[i]["nu_cpfcnpj_fornecedor"] for i in range(length_auction_history)]
    st.write(Participating_Suppliers)

    item_date_history_2Dlist = [auction_history[i]["vl_global"] for i in range(length_auction_history)]
    st.write(item_date_history_2Dlist)

    query = f'INSERT INTO "{SHEET_URL}" VALUES ("{auction_id}",\
                                                "{auction_summary["dtInicioProposta"]}",\
                                                "{auction_summary["dtFimProposta"]}",\
                                                "{auction_summary["valorEstimadoTotal"]}",\
                                                "{auction_summary["valorHomologadoTotal"]}",\
                                                "{auction_items["count"]}",\
                                                "{Items_Auctioned}",\
                                                "{Demanded_Quantity_Items}",\
                                                "{Estimated_Price_Items}",\
                                                "{Winning_Bids}",\
                                                "{"Testing 1"}",\
                                                "{Participating_Suppliers}",\
                                                "{"Testing 1"}",\
                                                "{"Testing 1"}")'
    CURSOR.execute(query)

def get_item_bid_history():

    # item_date_history_2Dlist = [[int(i) for i in line.split()] for line in data]

    # dict.fromkeys(keys, value)
    pass

def get_dates_bid_history():
    pass

def find_winner_supplier():
    pass
