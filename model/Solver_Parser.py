import pandas as pd
import re

def get_items_auctioned(auction_id, dataframe, column):
    string_items = dataframe.loc[dataframe["Auction_Id"] == auction_id, column][0]
    string_items = string_items.replace("\'",'').replace("]","").replace("[","").lstrip()
    list_string_items = string_items.split(',')
    return list_string_items if column == "Items_Auctioned" else [int(i) for i in list_string_items]

def get_demand_items_auctioned(auction_id, dataframe):
    return list(dataframe.loc[dataframe["Auction_Id"] == auction_id, "Demanded_Quantity_Items"][0])

""" Parser helper method to construct dictionary """
def parse_to_dictionary_format(auctioned_items, numeric_value_list):
    return dict(zip(auctioned_items, numeric_value_list))

""" Parser helper method to construct a list of tuples from two lists"""
def parse_two_lists_into_one_tuple_list(list_one, list_two):
    return list(zip(list_one, list_two))