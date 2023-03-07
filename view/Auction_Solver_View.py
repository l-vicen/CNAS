import streamlit as st
import model.Bilevel_Programming as bls
import model.Solver_Parser as sl
import data.DataBase as db


def solve_auction():
    st.title("SOLVER: Bilevel Programming")

    # Get Data Set
    dataframe = db.get_db()
    st.dataframe(dataframe)

    # Insert Target 
    text_input = st.text_input("Enter the auctionID: ", key="auction_id", help= "The actionID is the identifier of the Pregao.")
    btn_clicked = st.button("Insert")
    st.markdown("---")

    if (btn_clicked):

        # Getting list of auctioned items
        list_auction_items = sl.get_items_auctioned(text_input, dataframe)
        st.write(list_auction_items)

        # Getting list of auctioned items
        list_demand_items = sl.get_demand_items_auctioned(text_input, dataframe)
        st.write(list_demand_items)
    
    
