import ast
import streamlit as st

""" Returns the cell value as a list in a targeted column based on the auction id."""
def get_cell_as_list(auction_id, dataframe, column):
    cell_value = dataframe.loc[dataframe["Auction_Id"] == auction_id, column].iloc[0]
    msg = "#### {}".format(column)
    st.markdown(msg)
    st.write(cell_value)
    return ast.literal_eval(cell_value)

""" Returns the cell value as a list of dictionaries in the column {"Auction_Lot_Summary"} based on the auction id."""
def get_cell_as_list_of_dict(auction_id, dataframe):
    cell_value = dataframe.loc[dataframe["Auction_Id"] == auction_id, "Auction_Lot_Summary"].iloc[0]
    st.write(cell_value)
    # string_items = dataframe.loc[dataframe["Auction_Id"] == auction_id, "Auction_Lot_Summary"][0].replace("[{", "{").replace("}]", "}")
    # string_items = string_items.replace(", {", "**&** {")
    # return [ast.literal_eval(x) for x in string_items.split("**&** ")]
    return None

""" Parser helper method to construct dictionary """
def parse_to_dictionary_format(auctioned_items, numeric_value_list):
    return dict(zip(auctioned_items, numeric_value_list))

""" Parser helper method to construct a list of tuples from two lists"""
def parse_two_lists_into_one_tuple_list(list_one, list_two):
    return list(zip(list_one, list_two))