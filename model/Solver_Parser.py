import pandas as pd

def get_items_auctioned(auction_id, dataframe):
    return dataframe.loc[dataframe["Auction_Id"] == auction_id, "Items_Auctioned"][0]
