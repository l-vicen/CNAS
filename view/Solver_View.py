import streamlit as st
import model.Bilevel_Solver as bls
import model.Parser as sl
import data.DataBase as db
from collections import OrderedDict
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
        List_Auction_Items = sl.get_cell_as_list(text_input, dataframe, "Items_Auctioned")

        # Getting list of demands for items
        list_demand_items = sl.get_cell_as_list(text_input, dataframe, "Demanded_Quantity_Items")

        # Building DICT: {Item, Demand}
        Demand = sl.parse_to_dictionary_format(List_Auction_Items, list_demand_items)

        # Getting list of expected prices per item
        list_budget_items = sl.get_cell_as_list(text_input, dataframe, "Estimated_Price_Items")

        # Building DICT: {Item, Budget}
        budget_item_set = [a*b for a,b in zip(list_demand_items,list_budget_items)]
        Budget = sl.parse_to_dictionary_format(List_Auction_Items, budget_item_set)

        # Getting list of auction lots
        list_auction_lots = sl.get_cell_as_list_of_dict(text_input, dataframe)

        # Building list of participating suppliers
        auction_lots = len(list_auction_lots)
        Participating_Supplier = [str(supp) for i in range(auction_lots) for supp in list_auction_lots[i]["Participating_Suppliers"]]
        Participating_Supplier = list(OrderedDict.fromkeys(Participating_Supplier))

        # Cross Product (all combinations (Supplier & Items))
        pair_cross_products = list(itertools.product(Participating_Supplier, List_Auction_Items))
 
        # Observed Combinations (Supplier & Items)
        Supplies_Item_Pair_List = [(str(list_auction_lots[i].get("Participating_Suppliers")[j]), str(list_auction_lots[i].get("Lot_Item"))) for i in range(auction_lots) for j in range(len(list_auction_lots[i].get("Participating_Suppliers")))]
        
        ''' PART: Building DICTIONARY {(Supp, Item), Supply_Capacity} for Model '''

        length_cross_product = len(pair_cross_products)
        length_supp_with_capacity_list = len(Supplies_Item_Pair_List)
        Suppliers_Capacity = {Supplies_Item_Pair_List[i] : (Demand.get(Supplies_Item_Pair_List[i][1]) if Supplies_Item_Pair_List[i][1] in Demand else 0) for i in range(length_supp_with_capacity_list)}

        # Adding missing pairs from cross product
        for i in range(length_cross_product):
            key = pair_cross_products[i]
            if key not in Suppliers_Capacity:
                Suppliers_Capacity[key] = 0

        ''' PART: Building DICTIONARY {(Supp, Item), Production_Cost_per_Supplier_per_Item} for Model '''
        st.markdown("### Input Section")
        percentage_cost_multiplier = st.number_input("Enter COGS Multiplier")

        if (percentage_cost_multiplier):
            Suppliers_Production_Cost = {}
            for i in range(length_supp_with_capacity_list):
                key = Supplies_Item_Pair_List[i]
                for j in range(auction_lots):
                    number_of_supplier_in_this_lot = len(list_auction_lots[j]["Participating_Suppliers"])
                    lot_supplier = list_auction_lots[j]["Participating_Suppliers"]
                    lot_item = list_auction_lots[j]["Lot_Item"]
                    for k in range(number_of_supplier_in_this_lot):
                        if (key[0] == str(lot_supplier[k]) and key[1] == str(lot_item)):

                            # In case there are more than one bid from a supplier we derive his cost based on the average of its
                            # submitted bids
                            bids_supp_k = list_auction_lots[j]["History_Bids_Lot"][k]
                            number_bids_supp_k = len(bids_supp_k)
                            sum_bids = 0

                            for bid in range(number_bids_supp_k):
                                sum_bids += float(bids_supp_k[bid])
                            average_bids = (sum_bids / number_bids_supp_k)

                            # Multiply by a Cost of Goods Sold Factor
                            value = percentage_cost_multiplier * float(average_bids)
                            Suppliers_Production_Cost[key] = value
            
            # Adding missing pairs from cross product
            for i in range(length_cross_product):
                key = pair_cross_products[i]
                if key not in Suppliers_Production_Cost:
                    Suppliers_Production_Cost[key] = -1
        
            # Defining Utility
            utility_list = [(exp_expense * 1.2)  for exp_expense in budget_item_set]
            Utility = sl.parse_to_dictionary_format(List_Auction_Items, utility_list)
    
            # Executing Bilevel Solver if btn is pressed
            btn_apply_bilevel = st.button("Apply Bilevel Solver")
            st.markdown("---")
            if (btn_apply_bilevel):
                
                # For Visualizations
                Estimated_prices_list = sl.get_cell_as_list(text_input, dataframe, "Estimated_Price_Items")
                Actual_winning_bids_list = sl.get_cell_as_list(text_input, dataframe, "Winning_Bids")
                Demanded_quantities_list = sl.get_cell_as_list(text_input, dataframe, "Demanded_Quantity_Items")

                # Model Build and Solution
                bls.build_model(List_Auction_Items, Participating_Supplier, Demand, Utility, Suppliers_Capacity, Budget, Suppliers_Production_Cost, Actual_winning_bids_list, Demanded_quantities_list, Estimated_prices_list)