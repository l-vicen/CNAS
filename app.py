# 3rd party library dependencies
import streamlit as st
import data.Extractor as Extractor
import data.DataBase as DataBase
import router

# Creates Router
router.Router()

# In-house dependencies
st.title("ComprasNet's Auction Solver (CNAS)")

# Insert Target 
text_input = st.text_input("Enter the auctionID: ", help= "The actionID is the identifier of the Pregao.")

auction_summary_data = None
items_auctioned = None
items_bid_history = None

if(text_input):

    auction_summary_data = Extractor.get_auction_summary(text_input)
    st.markdown("## Auction Summary")
    st.write(auction_summary_data)
    st.markdown("---")

    items_auctioned = Extractor.get_auction_itens_information(text_input)
    st.markdown("## Items Auctioned")
    st.write(items_auctioned)
    st.markdown("---")

    # items_bid_history = Extractor.get_items_bid_history_for_auction(items_auctioned)
    # st.markdown("## Items Bid History")
    # st.write(items_bid_history)
    # st.markdown("---")
    text_input = None


if (items_bid_history != None):
    DataBase.post_db(text_input, auction_summary_data, items_auctioned)
