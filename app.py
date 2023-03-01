# 3rd party library dependencies
import streamlit as st
import data.Extractor as Extractor
import data.DataBase as DataBase

# In-house dependencies
st.title("ComprasNet's Auction Solver (CNAS)")

DataBase.get_db()
DataBase.insert_row_db()

# Insert Target 
text_input = st.text_input("Enter the auctionID: ", help= "The actionID is the identifier of the Pregao.")

if(text_input):

    auction_summary_data = Extractor.get_auction_summary(text_input)
    st.markdown("## Auction Summary")
    st.write(auction_summary_data)
    st.markdown("---")

    items_auctioned = Extractor.get_auction_itens_information(auction_summary_data)
    st.markdown("## Items Auctioned")
    st.write(items_auctioned)
    st.markdown("---")

    items_bid_history = Extractor.get_items_bid_history_for_auction(items_auctioned)
    st.markdown("## Items Bid History")
    st.write(items_bid_history)
    st.markdown("---")




