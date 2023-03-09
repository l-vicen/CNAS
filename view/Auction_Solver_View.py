import streamlit as st
import model.Bilevel_Programming as bls
import model.Solver_Parser as sl
import data.DataBase as db
from collections import OrderedDict
import random
import itertools

def solve_auction():

    st.title("SOLVER: Bilevel Programming")

    # Get Data Set
    dataframe = db.get_db()
    st.dataframe(dataframe)

    # Insert Target 
    text_input = st.text_input("Enter the auctionID: ", key="solver_input", help= "The actionID is the identifier of the Pregao.")
    st.markdown("---")

    if (text_input):

        # Getting list of auctioned items
        list_auction_items = sl.get_cell_as_list(text_input, dataframe, "Items_Auctioned", 1)
        st.write(list_auction_items)

        # Getting list of demands for items
        list_demand_items = sl.get_cell_as_list(text_input, dataframe, "Demanded_Quantity_Items", 0)
        st.write(list_demand_items)

        # Building DICT: {Item, Demand}
        Demand = sl.parse_to_dictionary_format(list_auction_items, list_demand_items)
        st.write(Demand)

        # Getting list of expected prices per item
        list_budget_items = sl.get_cell_as_list(text_input, dataframe, "Estimated_Price_Items", 0)
        st.write(list_budget_items)

        # Building DICT: {Item, Budget}
        Budget = sl.parse_to_dictionary_format(list_auction_items, list_budget_items)

        # Getting list of auction lots
        list_auction_lots = sl.get_cell_as_list_of_dict(text_input, dataframe)

        # Building list of participating suppliers
        auction_lots = len(list_auction_lots)
        Participating_Supplier = [str(supp) for i in range(auction_lots) for supp in list_auction_lots[i]["Participating_Suppliers"]]
        Participating_Supplier = list(OrderedDict.fromkeys(Participating_Supplier))

        # Cross Product (all combinations (Supplier & Items))
        pair_cross_products = list(itertools.product(Participating_Supplier, list_auction_items))
 
        # Observed Combinations (Supplier & Items)
        Supplies_Item_Pair_List = [(str(list_auction_lots[i].get("Participating_Suppliers")[j]), str(list_auction_lots[i].get("Lot_Item"))) for i in range(auction_lots) for j in range(len(list_auction_lots[i].get("Participating_Suppliers")))]
        for i in range(len(Supplies_Item_Pair_List)):
            st.write(Supplies_Item_Pair_List[i][0])
            st.write(Supplies_Item_Pair_List[i][1])

        # Building DICT: {(Supp, Item), Supply_Capacity}
        length_cross_product = len(pair_cross_products)
        length_supp_with_capacity_list = len(Supplies_Item_Pair_List)
        Suppliers_Capacity = {(Supplies_Item_Pair_List[i][0], Supplies_Item_Pair_List[i][1]) : (Demand.get(Supplies_Item_Pair_List[i][1]) if Supplies_Item_Pair_List[i][1] in Demand else 0) for i in range(length_supp_with_capacity_list)}
        for key, value in Suppliers_Capacity.items():
            st.write(key)
            st.write(value)


        # Adding missing pairs from cross product
        for i in range(length_cross_product):
            key = pair_cross_products[i]
            if key not in Suppliers_Capacity:
                Suppliers_Capacity[key] = 0
                
        st.markdown("### Input Section")
        percentage_cost_multiplier = st.number_input("Enter COGS Multiplier")
        if (percentage_cost_multiplier):
            
            # Building DICT: {(Supp, Item), Production_Cost}
            Suppliers_Production_Cost = {}
            for i in range(length_supp_with_capacity_list):

                key = Supplies_Item_Pair_List[i]

                for j in range(auction_lots):

                    number_of_supplier_in_this_lot = len(list_auction_lots[j]["Participating_Suppliers"])
                    lot_supplier = list_auction_lots[j]["Participating_Suppliers"]
                    lot_item = list_auction_lots[j]["Lot_Item"]

                    for k in range(number_of_supplier_in_this_lot):

                        if (key[0] == lot_supplier[k] and key[1] == lot_item):
                            value = percentage_cost_multiplier * float(list_auction_lots[j]["History_Bids_Lot"][k][0])
                            Suppliers_Production_Cost[key] = value
            
            # Adding missing pairs from cross product
            for i in range(length_cross_product):
                key = pair_cross_products[i]
                if key not in Suppliers_Production_Cost:
                    Suppliers_Production_Cost[key] = 0

            # Building Bilevel Program
            number_auctioned_items = len(list_auction_items)
            utility_list = []
            for i in range(number_auctioned_items):
                utility_list.append(random.uniform(100, 200))

            Utility = sl.parse_to_dictionary_format(list_auction_items, utility_list)
    
            btn_apply_bilevel = st.button("Apply Bilevel Solver")
            st.markdown("---")
            if (btn_apply_bilevel):
                bls.build_model(list_auction_items, Participating_Supplier, Demand, Utility, Suppliers_Capacity, Budget, Suppliers_Production_Cost)
            
            # Getting User Input
            # collect_numbers = lambda x : [int(i) for i in re.split("[^0-9]", x) if i != ""]
            # utility_input_list  = st.text_input("Please enter numbers", key = "Utility_Input")
            # utility_list = collect_numbers(utility_input_list)

            # if (utility_input_list):
            #     Utility = sl.parse_to_dictionary_format(list_auction_items, utility_list)
                # st.markdown("#### Auctioneer's perceived Utility per Item")
                # st.write(Utility)
                # st.markdown("---")

                # # building Bilevel Program
                # btn_apply_bilevel = st.button("Apply Bilevel Solver")
                # st.markdown("---")
                # if (btn_apply_bilevel):
                #     bls.build_model(list_auction_items, Participating_Supplier, Demand, Utility, Suppliers_Capacity, Budget, Suppliers_Production_Cost)
