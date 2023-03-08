import streamlit as st
import model.Bilevel_Programming as bls
import model.Solver_Parser as sl
import data.DataBase as db
from collections import OrderedDict
import re

def solve_auction():
    st.title("SOLVER: Bilevel Programming")

    # Get Data Set
    dataframe = db.get_db()
    st.dataframe(dataframe)

    # Insert Target 
    text_input = st.text_input("Enter the auctionID: ", key="auction_id", help= "The actionID is the identifier of the Pregao.")

    if (text_input):

        # Getting list of auctioned items
        list_auction_items = sl.get_cell_as_list(text_input, dataframe, "Items_Auctioned")
        st.write("#### List Items")
        st.write(list_auction_items)

        # Getting list of demands for items
        list_demand_items = sl.get_cell_as_list(text_input, dataframe, "Demanded_Quantity_Items")
        # st.write("#### Demand Items")
        # st.write(list_demand_items)

        # Getting list of expected prices per item
        list_budget_items = sl.get_cell_as_list(text_input, dataframe, "Estimated_Price_Items")
        # st.write("#### Budget Items")
        # st.write(list_budget_items)

        # Getting list of winner bids per item
        list_winner_bids = sl.get_cell_as_list(text_input, dataframe, "Winning_Bids")
        # st.write("#### Winner Items")
        # st.write(list_winner_bids)

        # Getting list of auction lots
        list_auction_lots = sl.get_cell_as_list_of_dict(text_input, dataframe)
        st.write(list_auction_lots)

        # Building list of participating suppliers
        auction_lots = len(list_auction_lots)
        Participating_Supplier = [str(supp) for i in range(auction_lots) for supp in list_auction_lots[i]["Participating_Suppliers"]]
        Participating_Supplier = list(OrderedDict.fromkeys(Participating_Supplier))
        st.markdown("##### Participating Suppliers")
        st.write(Participating_Supplier)

        # Building DICT: {TUPLE, Capacity}
        Supplies_Item_Pair_List = [(str(list_auction_lots[i].get("Participating_Suppliers")[j]), list_auction_lots[i].get("Lot_Item")) for i in range(auction_lots) for j in range(len(list_auction_lots[i].get("Participating_Suppliers")))]
        # st.write(##### Pair of (Supplier, Item))
        # st.write(Supplies_Item_Pair_List)

        # Building list of tuples [(Supplier, Item)]
        tuple_supp_item_list = sl.parse_two_lists_into_one_tuple_list(Participating_Supplier, list_auction_items)
        # st.markdown("##### Tuple List")
        # st.write(tuple_supp_item_list)

        # Building DICT: {Item, Demand}
        Demand = sl.parse_to_dictionary_format(list_auction_items, list_demand_items)
        st.markdown("##### Item Demand")
        st.write(Demand)

        # Building DICT: {(Supp, Item), Supply_Capacity}
        lenght_supp_items = len(Supplies_Item_Pair_List)
        Suppliers_Capacity = {str(Supplies_Item_Pair_List[i]) : (Demand.get(Supplies_Item_Pair_List[i][1]) if Supplies_Item_Pair_List[i][1] in Demand else -1) for i in range(lenght_supp_items)}
        st.markdown("##### Supplier Capacity")
        st.write(Suppliers_Capacity)

        # Building DICT: {Item, Budget}
        Budget = sl.parse_to_dictionary_format(list_auction_items, list_budget_items)
        st.markdown("##### Budget per Item")
        st.write(Budget)

        # Building DICT: {(Supp, Item), Production_Cost}
        percentage_cost_multiplier = st.number_input("Enter COGS Multiplier")

        if (percentage_cost_multiplier):

            Suppliers_Production_Cost = {
                str(Supplies_Item_Pair_List[i]) : ((percentage_cost_multiplier *  list_auction_lots[j]["History_Bids_Lot"][0]) 
                                                if (Supplies_Item_Pair_List[i][0] == list_auction_lots[j]["Participating_Suppliers"][k] and  
                                                    Supplies_Item_Pair_List[i][1] == list_auction_lots[j]["Lot_Item"]) else -1)
                for i in range(lenght_supp_items) 
                for j in range(auction_lots)
                for k in range(len(list_auction_lots[j]["Participating_Suppliers"]))
                }
            
            
            st.markdown("##### Supplier Production Cost Per Item")
            st.write(Suppliers_Production_Cost)

            st.markdown("---")  
            
            # Getting User Input
            collect_numbers = lambda x : [int(i) for i in re.split("[^0-9]", x) if i != ""]
            utility_input_list  = st.text_input("Please enter numbers", key = "Utility_Input")
            utility_list = collect_numbers(utility_input_list)

            if (utility_input_list):
                Utility = sl.parse_to_dictionary_format(list_auction_items, utility_list)
                st.markdown("#### Utility per Item")
                st.write(Utility)
        
                # Production_Cost = sl.parse_to_dictionary_format(list_auction_items, cost_list)
                # st.markdown("#### Production Cost per Item")
                # st.write(Production_Cost)