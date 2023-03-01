# 3rd party libraries
import pandas as pd
import streamlit as st
import requests
import re
import time
import json

""" Global Variables Definitions

In this section, I define the macro variables to build the strings.

(1) Query Auction Summary for specific Auction
    - URL: "https://compras.dados.gov.br/pregoes/doc/pregao/`<AuctionID>`.csv"
    - `AuctionID`: 1530740900092006

(2) Query Auction Items for specific Auction
    - URL: "https://compras.dados.gov.br/pregoes/id/pregao/`<AuctionID>`/itens.csv"
    - `AuctionID`: 1530740900092006

(3) Query Item specific list of bids for a specific Auction
    - "https://compras.dados.gov.br/pregoes/v1/proposta_item_pregao.csv?item=`<ItemID>`&co_pregao=`<coPregaoID>`"
    https://compras.dados.gov.br/pregoes/v1/proposta_item_pregao.json?item=709095&co_pregao=29107
    - `<ItemID>`: 709103
    - `<coPregaoID>`: 29107
"""
URL_MAIN =  "https://compras.dados.gov.br"
URL_AUCTION = "/pregoes/doc/pregao/"
JSON_TYPE = ".json"

def get_auction_summary(auctionID):
    target = URL_MAIN + URL_AUCTION + auctionID + JSON_TYPE
    responseAuctionSummary = requests.get(url = target)
    auction_summary_json_dictionary = responseAuctionSummary.json()
    return auction_summary_json_dictionary

def get_auction_itens_information(auction_summary_json_dictionary):
    targetItems = URL_MAIN + auction_summary_json_dictionary["_links"]["itens"]["href"] + JSON_TYPE
    responseItems = requests.get(url = targetItems)
    auction_items_json_dictionary = responseItems.json()
    return auction_items_json_dictionary

def get_items_bid_history_for_auction(auction_items_json_dictionary):
    pregoes_list = auction_items_json_dictionary["_embedded"]["pregoes"]
    list_target = [(URL_MAIN + re.sub(r"(.html)", r".json", pregoes_list[i]["_links"]["Propostas"]["href"])) for i in range(len(pregoes_list))]
    st.write(list_target)
