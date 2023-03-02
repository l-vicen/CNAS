# 3rd party libraries
import streamlit as st
import requests
import re
import json

# Global Variables used to build http request targets
URL_AUCTION =  "http://compras.dados.gov.br/pregoes/id/pregao/"
ITEMS = "/itens"
JSON_TYPE = ".json"

"""

get_auction_summary(auctionId) does http request
to target: https://compras.dados.gov.br/pregoes/doc/pregao/<auctionID>json
and return a .json object with summary data from one auction.

param auctionID Auction Identifier 
"""
def get_auction_summary(auctionID):
    target = URL_AUCTION + auctionID + JSON_TYPE

    try:
        responseAuctionSummary = requests.get(url = target)
    except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
        st.warning("The request took too long!")

    auction_summary_json_dictionary = responseAuctionSummary.json()
    return auction_summary_json_dictionary 
"""

get_auction_itens_information(auction_summary_json_dictionary) does http request
to target: <TODO>
and return a .json object with the information on the items auctioned in a specific auction. 

param auction_summary_json_dictionary <TODO>
"""
def get_auction_itens_information(auction_summary_json_dictionary):
    targetItems = URL_MAIN + auction_summary_json_dictionary["_links"]["itens"]["href"] + JSON_TYPE

    st.write(targetItems)

    try:
        responseItems = requests.get(url = targetItems)
    except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
        st.warning("The request took too long!")

    auction_items_json_dictionary = responseItems.json()
    return auction_items_json_dictionary

"""

get_items_bid_history_for_auction(auction_items_json_dictionary) does http request
to target: <TODO>
and return a .json object with the history of bids for every item auctioned.

param auction_summary_json_dictionary <TODO>
"""
def get_items_bid_history_for_auction(auction_items_json_dictionary):
    pregoes_list = auction_items_json_dictionary["_embedded"]["pregoes"]
    list_target = [(URL_MAIN + re.sub(r"(.html)", r".json", pregoes_list[i]["_links"]["Propostas"]["href"])) for i in range(len(pregoes_list))]
    
    try:
        responseItems = requests.get(url = list_target[0])
    except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
        st.warning("The request took too long!")

    responseItemsJSON = responseItems.json()
    return responseItemsJSON



