import streamlit as st
import model.Bilevel_Programming as bls
import model.Solver_Parser as sl
import data.DataBase as db
import re

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

        # TODO: Dictionary of Item Utility {Item, Demand}
        # TODO: Dictionary of Item Expected Cost {Item, ExpectedCost}
        # TODO: LIST of Participating Suppliers
        # TODO: Dictionary {Tuple, Integer} of Supplier Capacity 

        # Getting list of auctioned items
        list_auction_items = sl.get_cell_as_list(text_input, dataframe, "Items_Auctioned")
        # st.write(list_auction_items)

        # Getting list of demands for items
        list_demand_items = sl.get_cell_as_list(text_input, dataframe, "Demanded_Quantity_Items")
        # st.write(list_demand_items)

        # Getting list of expected prices per item
        list_budget_items = sl.get_cell_as_list(text_input, dataframe, "Estimated_Price_Items")
        st.write(list_budget_items)

        # Getting list of winner bids per item
        list_winner_bids = sl.get_cell_as_list(text_input, dataframe, "Winning_Bids")
        st.write(list_winner_bids)

        # Building DICT: {Item, Demand}
        demand = sl.parse_to_dictionary_format(list_auction_items, list_demand_items)
        st.markdown("##### Item Demand")
        st.write(demand)

        # Building DICT: {Item, Demand}
        # utility_input = get_utility_from_user()
        utility = sl.parse_to_dictionary_format(list_auction_items, 0)
        st.write(utility)

        # st.write({'Lot_Item': 'RODO', 'Participating_Suppliers': ['41205907000174', '06910908000119'], 'History_Bids_Lot': [['1804'], ['4800']], 'History_Bid_Dates_Lot': [['2006-06-07T00:00:00'], ['2006-06-08T00:00:00']], 'Winning_Bid': 1804.0, 'Winner_Supplier': None})

        # Build model & Solve
        # bls.build_model()

def get_utility_from_user():

    collect_numbers = lambda x : [int(i) for i in re.split("[^0-9]", x) if i != ""]
    numbers = st.text_input("PLease enter numbers")
    st.write(collect_numbers(numbers))

    fixed_numbers = st.multiselect("Please select numbers", [1, 2, 3, 4, 5])
    st.write(fixed_numbers)
    return fixed_numbers