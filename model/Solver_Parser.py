import pandas as pd
import ast
import re

def get_cell_as_list(auction_id, dataframe, column):

    # Parsing cell's string
    string_items = dataframe.loc[dataframe["Auction_Id"] == auction_id, column][0]
    string_items = string_items.replace("\'",'').replace("]","").replace("[","")

    # Getting list
    list_target = string_items.split(',')
    list_target = [s.lstrip() for s in list_target]

    return list_target if (column == "Items_Auctioned") else [float(i) for i in list_target]

def get_lot_summary_as_list_of_dictionaries(auction_id, dataframe):
    string_items = dataframe.loc[dataframe["Auction_Id"] == auction_id, "Auction_Lot_Summary"][0]
    string_items = string_items.lstrip()
    string_items = string_items.rstrip()
    string_items = string_items.replace(", {'Lot_Item':", "**&** {'Lot_Item':")
    return string_items.split("**&** ")


""" Parser helper method to construct dictionary """
def parse_to_dictionary_format(auctioned_items, numeric_value_list):
    return dict(zip(auctioned_items, numeric_value_list))

""" Parser helper method to construct a list of tuples from two lists"""
def parse_two_lists_into_one_tuple_list(list_one, list_two):
    return list(zip(list_one, list_two))