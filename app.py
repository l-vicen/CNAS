# 3rd party library dependencies
import streamlit as st
import data.Extractor as Extractor
import data.DataBase as DataBase
import view.DataSet_View as ds_view

# Home page title
st.title("ComprasNet's Auction Solver (CNAS)")

"""Side Bar Class Declaration""" 

st.sidebar.image('assets/tum_logo.png')
st.sidebar.markdown('---')

# Sidebar attributes
features = ['Home Page', 'Solve Auction', 'Data Set']
page = st.sidebar.selectbox('Choose Page', features)
st.sidebar.markdown('---')

if page == features[0]:
    pass

elif page == features[1]:
    pass

else:
    ds_view.construct_data_set_page()

st.sidebar.markdown('##### Creator')
st.sidebar.markdown('Lucas Perasolo')
st.sidebar.markdown('---')


# Insert Target 
text_input = st.text_input("Enter the auctionID: ", help= "The actionID is the identifier of the Pregao.")

items_bid_history = []

if(text_input):

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
