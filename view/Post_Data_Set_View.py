import streamlit as st
import data.Extractor as Extractor
import data.DataBase as DataBase

def insert_into_data_set_view():

    st.title("POST: Data Set")

    # Insert Target 
    text_input = st.text_input("Enter the auctionID: ", key="auction_id", help= "The actionID is the identifier of the Pregao.")
    btn_clicked = st.button("Insert")

    items_bid_history = []

    if(btn_clicked):
        auction_summary_data = Extractor.get_auction_summary(text_input)
        # st.markdown("## Auction Summary")
        # st.write(auction_summary_data)
        # st.markdown("---")

        items_auctioned = Extractor.get_auction_itens_information(text_input)
        # st.markdown("## Items Auctioned")
        # st.write(items_auctioned)
        # st.markdown("---")

        items_bid_history = Extractor.get_items_bid_history_for_auction(items_auctioned)
        # st.markdown("## Items Bid History")
        # st.write(items_bid_history)
        # st.markdown("---")


    if (len(items_bid_history) > 0):
        DataBase.post_db(text_input, auction_summary_data, items_auctioned, items_bid_history)
        items_bid_history = []
        text_input = ""