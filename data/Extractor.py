# 3rd party libraries
import pandas as pd
import streamlit as st
import requests
import re

# Global Variables used to build http request targets
URL_MAIN =  "https://compras.dados.gov.br"
URL_AUCTION = "/pregoes/doc/pregao/"
JSON_TYPE = ".json"

"""

get_auction_summary(auctionId) does http request
to target: https://compras.dados.gov.br/pregoes/doc/pregao/<auctionID>json
and return a .json object with summary data from one auction.

param auctionID Auction Identifier 
"""
def get_auction_summary(auctionID):
    target = URL_MAIN + URL_AUCTION + auctionID + JSON_TYPE
    responseAuctionSummary = requests.get(url = target)
    auction_summary_json_dictionary = responseAuctionSummary.json()

    return {
        "co_processo": auction_summary_json_dictionary["co_processo"],
        "co_uasg": auction_summary_json_dictionary["co_uasg"],
        "dtDataEdital": auction_summary_json_dictionary["dtDataEdital"],
        "dtInicioProposta": auction_summary_json_dictionary["dtInicioProposta"],
        "dtFimProposta": auction_summary_json_dictionary["dtFimProposta"],
        "valorHomologadoTotal": auction_summary_json_dictionary["valorHomologadoTotal"],
        "valorEstimadoTotal": auction_summary_json_dictionary["valorEstimadoTotal"]
    }

"""

get_auction_itens_information(auction_summary_json_dictionary) does http request
to target: <TODO>
and return a .json object with the information on the items auctioned in a specific auction. 

param auction_summary_json_dictionary <TODO>
"""
def get_auction_itens_information(auction_summary_json_dictionary):
    targetItems = URL_MAIN + auction_summary_json_dictionary["_links"]["itens"]["href"] + JSON_TYPE
    responseItems = requests.get(url = targetItems)
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
    responseItems = requests.get(url = list_target[0])
    responseItemsJSON = responseItems.json()
    return responseItemsJSON



