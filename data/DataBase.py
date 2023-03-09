# 3rdParty Libraries
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect

# URL of private Google Sheet
SHEET_URL = st.secrets["private_gsheets_url"]

# Name of the columns in the google sheet
GOOGLE_SHEET_COLUMNS = ['Auction_Id', 
                        'Start_Date',
                        'End_Date',
                        'Total_Estimated_Price',
                        'Total_Homologated_Price',
                        'Number_Items_Auctioned',
                        'Number_Valid_Items_Auctioned',
                        'Items_Auctioned',
                        'Demanded_Quantity_Items',
                        'Estimated_Price_Items',
                        'Winning_Bids',
                        'Auction_Lot_Summary']

"""
Default way to access the private information on the credentials to access the Google Sheet Data Set.

Via st.secrets["gcp_service_account"] I store private credential info on a file .streamlit/secrets.toml 
that it is used on the hosting side (Streamlit Cloud) to establish communication between app and data set
without disclosing critical information.
"""

CONNECTION = connect(":memory:", adapter_kwargs={
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

"""
get_db() uses shillelagh lib to perform a common get
request in SQL & Python. Here, I retrive all Tuples from the
Google Sheet (A Tuple is a single row in the data set). Then,
I convert the tuples to a dataframe.
"""
@st.cache_data(ttl=50)
def get_db():
    # Establishing the connection
    cursor = CONNECTION.cursor()

    query = f'SELECT * FROM "{SHEET_URL}"'
    rows = cursor.execute(query)
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

    # Creating a list with all auction situations (homologated, canceled, etc ....)
    Auction_Situation = [pregoes[i]["situacao_item"] for i in range(length_pregoes)]
    st.write(Auction_Situation)
    
    """ 2nd Part: Getting data from auction_items query """

    # Variable to avoid re-accessing the inside of the auction_history json multiple times
    number_auction_lots = len(auction_history)

    # List with a summary of the auction lot. It calls the helper method: def parse_auction_lot(...)
    Auction_Lot_Summary= [parse_auction_lot(auction_history[i], Items_Auctioned[i], Winning_Bids[i]) for i in range(number_auction_lots)]

    # Removing Auctions whose outcomes are not determined (No winners) <The cause can be different>.
    lots = len(Winning_Bids)
    Invalid_Auction_Lot_Index = [i for i in range(lots) if Winning_Bids[i] == -1]
    number_of_bad_auctions = len(Invalid_Auction_Lot_Index)

    Items_Auctioned = remove_bad_auctions(Items_Auctioned, Invalid_Auction_Lot_Index, number_of_bad_auctions)
    Demanded_Quantity_Items = remove_bad_auctions(Demanded_Quantity_Items, Invalid_Auction_Lot_Index, number_of_bad_auctions)
    Estimated_Price_Items = remove_bad_auctions(Estimated_Price_Items, Invalid_Auction_Lot_Index, number_of_bad_auctions)
    Auction_Lot_Summary = remove_bad_auctions(Auction_Lot_Summary, Invalid_Auction_Lot_Index, number_of_bad_auctions)
    Winning_Bids = remove_bad_auctions(Winning_Bids, Invalid_Auction_Lot_Index, number_of_bad_auctions)

    number_valid_auction_lots = len(Items_Auctioned)

    # Query: Inserting values into data set
    query = f'INSERT INTO "{SHEET_URL}" VALUES ("{auction_id}",\
                                                "{auction_summary["dtInicioProposta"]}",\
                                                "{auction_summary["dtFimProposta"]}",\
                                                "{auction_summary["valorEstimadoTotal"]}",\
                                                "{auction_summary["valorHomologadoTotal"]}",\
                                                "{auction_items["count"]}",\
                                                "{number_valid_auction_lots}",\
                                                "{Items_Auctioned}",\
                                                "{Demanded_Quantity_Items}",\
                                                "{Estimated_Price_Items}",\
                                                "{Winning_Bids}",\
                                                "{Auction_Lot_Summary}")'
    # Establishing the connection
    cursor = CONNECTION.cursor()

    cursor.execute(query)
    st.success("Auction successfully added to data set!")


def parse_auction_lot(auction_lot, auction_lot_item, smallest_bid):

    # Variable to avoid re-accessing the inside of the auction_history json multiple times
    auction_lot_history = auction_lot["_embedded"]["pregoes"]
    number_bids_in_lot = len(auction_lot_history)

    #  Creating a list with all participating suppliers
    Participating_Suppliers = [auction_lot_history[i]["nu_cpfcnpj_fornecedor"] for i in range(number_bids_in_lot)]
    number_suppliers = len(Participating_Suppliers)
    # st.write("Participating Suppliers")
    # st.write(Participating_Suppliers)

    # Creates a list with the history bids of the respective supplier
    item_bid_history_2D_list = [[auction_lot_history[i]["vl_global"] for i in range(number_bids_in_lot) if (auction_lot_history[i]["nu_cpfcnpj_fornecedor"] == Participating_Suppliers[j])] for j in range(number_suppliers)]
    # st.write("Bid History of Every Supplier")
    # st.write(item_bid_history_2D_list)

    # Creates a list with the history dates of the bids of the respective supplier
    item_date_history_2D_list = [[auction_lot_history[i]["dtRegistro"] for i in range(number_bids_in_lot) if (auction_lot_history[i]["nu_cpfcnpj_fornecedor"] == Participating_Suppliers[j])] for j in range(number_suppliers)]
    # st.write("Dates of bids of every Supplier")
    # st.write(item_date_history_2D_list)

    # TODO: Review this part
    winner_supplier = None
    for i in range(len(item_bid_history_2D_list)):
        for j in range(len(item_bid_history_2D_list[i])):
            if (item_bid_history_2D_list[i][j] == smallest_bid):
                winner_supplier = Participating_Suppliers[i]
            else:
                continue

    # Summary Dictionary
    dictionary_lot_summary =  {
        "Lot_Item": auction_lot_item,
        "Participating_Suppliers": Participating_Suppliers,
        "History_Bids_Lot": item_bid_history_2D_list,
        "History_Bid_Dates_Lot": item_date_history_2D_list,
        "Winning_Bid": smallest_bid,
        "Winner_Supplier": winner_supplier
    }
    # st.write(dictionary_lot_summary)

    return dictionary_lot_summary

def remove_bad_auctions(original_list, bad_elements_list, number_bad_elements):
    for i in range(number_bad_elements):
        original_list.pop(bad_elements_list[i])
    return original_list