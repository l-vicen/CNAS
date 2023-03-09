import ast

""" Returns the cell value as a list in a targeted column based on the auction id."""
def get_cell_as_list(auction_id, dataframe, column):
    cell_value = dataframe.loc[dataframe["Auction_Id"] == auction_id, column].iloc[0]
    cell_value = " ".join(cell_value.split())
    cell_values_as_list = ast.literal_eval(cell_value)  
    return [x.lower() for x in cell_values_as_list]

""" Returns the cell value as a list of dictionaries in the column {"Auction_Lot_Summary"} based on the auction id."""
def get_cell_as_list_of_dict(auction_id, dataframe):
    cell_value = dataframe.loc[dataframe["Auction_Id"] == auction_id, "Auction_Lot_Summary"].iloc[0]
    cell_value = cell_value.replace("[{", "{")
    cell_value = cell_value.replace("}]", "}")
    cell_value = cell_value.replace(", {", "**&** {")
    return [ast.literal_eval(x) for x in cell_value.split("**&** ")]

""" Parser helper method to construct dictionary """
def parse_to_dictionary_format(auctioned_items, numeric_value_list):
    return dict(zip(auctioned_items, numeric_value_list))
