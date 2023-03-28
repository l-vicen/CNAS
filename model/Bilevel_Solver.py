# 3rd Party libraries
from pyomo.environ import *
from pao.pyomo import *
import plotly.express as px
import pandas as pd
import streamlit as st
import collections
from streamlit.runtime.scriptrunner.script_run_context import SCRIPT_RUN_CONTEXT_ATTR_NAME
from threading import current_thread
from contextlib import contextmanager
from io import StringIO
import sys

''' Model Objective Functions
1) Upper-level: 
    def auction_objective_function(model)  := Maximizes the return of expected utility for given item purchase (Utility * X - Supplier Price)
2) Lower-level:
    def pricing_objective_function(model)  := Maximizes the overall bid price submission.
'''
def auction_objective_function(model):
    return sum((model.Utility[i] * model.X[j,i]) - model.L.P[j,i] for j,i in model.j*model.i)

def pricing_objective_function(submodel, model):
    return sum(submodel.P[j,i] for j,i in model.j * model.i)

''' Model Constraints
1) Upper-level: 
    def single_sourcing_constraint(model, i): Ensures there is only 1 winner per auctioned item.
    def demand_requirement_constraint(model, i): Ensures that the respective supplier can supply the whole quantity of the demanded item. 
2) Lower-level:
    def lower_and_upper_bound_constraint(submodel, j, i): Ensures that the submitted bid prices lays within a reasonable range. 
    The lower bound represents the cost of production, the upper bound represents the auctioneer budget.
'''
def single_sourcing_constraint(model, i):
    return sum(model.X[j,i] for j in model.j) == 1

def demand_requirement_constraint(model, i):
    return sum(model.Supply_capacity[j,i] * model.X[j,i] for j in model.j) >= model.Demand[i]

def lower_and_upper_bound_constraint(submodel, j, i):
    # return (submodel.Production_Costs[j,i], submodel.P[j,i], submodel.Budget[i])
    return (0, submodel.P[j,i], submodel.Budget[i])

def build_model(chosen_solver, set_items, set_suppliers, demand_dictionary, utility_dictionary, supplier_capacity_dictionary, budget_dictionary, production_costs_dictionary, actual_winning_bids_list, demanded_quantities_list, estimated_prices_list):

    # Upper-level definition: Auction Problem
    model = ConcreteModel("Upper-level: Auction Problem")

    '''   Model Subscripts
    model.i := Set of auctioned items.
    model.j := Set of auction participating suppliers.
    '''
    model.i = Set(initialize = set_items, doc='Auctioned_Items')
    # print_into_streamlit("Auctioned Items", model.i)

    model.j = Set(initialize = set_suppliers, doc='Auction_Participating_Suppliers')
    # print_into_streamlit("Participating Suppliers in Auction", model.j)

    ''' Upper-level decision variable 
    model.X := Binary variable, equal to 1 if quotation for item i is allocated to supplier j ; 0
    otherwise.
    '''
    model.X = Var(model.j, model.i, domain=Binary, doc='Decision_Variable_X') 

    # Lower-level definition: Pricing Problem 
    model.L = SubModel(fixed=model.X)

    ''' Lower-level decision variable 
    model.L.P := Real variable, represents the supplier bid price.
    '''
    model.L.P = Var(model.j, model.i, domain=Reals, doc='Decision_Variable_P') 

    ''' Model Parameters 
    model.Demand := the total demand for item i submitted by auctioneer.
    model.Utility := expected utility from purchase by the auctioneer.
    model.supply_capacity := the quantity of item i that supplier j can procure.
    model.production_costs := the production cost of item i if produced by supplier j.
    '''
    model.Demand = Param(model.i, initialize= demand_dictionary, mutable=False, doc='Auctioneer\'s_Demand_per_Item')
    # print_into_streamlit("Auctioneer's Demand per Item", model.Demand)

    model.Utility = Param(model.i, initialize= utility_dictionary, mutable=False, doc='Auctioneer\'s_Perceived_Utility_per_Item')
    # print_into_streamlit("Auctioneer's Perceived Utility per Item",  model.Utility)

    model.Supply_capacity = Param(model.j, model.i, initialize= supplier_capacity_dictionary, mutable=False, doc='Suppliers\'_individual_Supply_Capacity_per_Item')
    # print_into_streamlit("Suppliers\' individual Supply Capacity per Item",   model.Supply_capacity)

    model.L.Budget = Param(model.i, initialize= budget_dictionary, mutable=False, doc='Auctioneer\'s_expected_Expense_per_Items')
    # print_into_streamlit("Auctioneer's expected Expense per Items",  model.L.Budget)

    model.L.Production_Costs = Param(model.j, model.i, initialize = production_costs_dictionary, mutable=False, doc='Suppliers\'_individual_Production_Cost_per_Item')
    # print_into_streamlit("Suppliers\' individual Production Cost per Item",  model.L.Production_Costs)

    # Objective function assignments
    model.o = Objective(rule=auction_objective_function(model), sense=maximize, doc='Auction_Problem') # Upper-level 
    # print_into_streamlit("Upper-level Objective Function",  model.o)

    model.L.o = Objective(rule= pricing_objective_function(model.L, model), sense=maximize, doc='Pricing_Problem') # Lower-level
    # print_into_streamlit("Lower-level Objective Function",  model.L.o)

    # Upper-level constraint assignments
    model.SingleSourcingConstraint = Constraint(model.i, rule=single_sourcing_constraint, doc='There_is_at_most_1_winner')
    # print_into_streamlit("Single Sourcing Constraint",  model.SingleSourcingConstraint)

    model.DemandConstraint = Constraint(model.i, rule=demand_requirement_constraint, doc='Auctioneer\'s_Demand_is_fulfilled')
    # print_into_streamlit("Demand Constraint",  model.DemandConstraint)

    # Lower-level constraint assignment
    model.L.BidPriceBoundaryConstraint = Constraint(model.j, model.i, rule=lower_and_upper_bound_constraint, doc='Bid_Price_is_non-negative')
    # print_into_streamlit("Bid Price Constraint",  model.L.BidPriceBoundaryConstraint)

    print_into_streamlit("Model Formulation",  model)

    try:
        if (chosen_solver == "pao.pyomo.FA"):
            # Calling the Big-M Relaxation Solver
            solver = Solver(chosen_solver)
            solver.solve(model)
        else:
            solver = Solver(chosen_solver)
            solver.solve(model)

        # This prints the model formulation again filled with the solutions for X and P
        # print_into_streamlit("Solved Model Formulation",  model)

        # Display Auction Winners as a Heat Map
        x_vals = pd.Series(model.X.extract_values(), name=model.X.name)
        winner_dataframe_pre = x_vals.to_frame().reset_index()
        winner_dataframe = winner_dataframe_pre.pivot(index='level_1', columns='level_0')['X'].fillna(0)
        auctionWinners_HeatMap(winner_dataframe)

        # Display Prices as a Scatter Plot 
        p_vals = pd.Series(model.L.P.extract_values(), name=model.X.name)
        prices_dataframe_pre = p_vals.to_frame().reset_index()
        prices_dataframe_pre = prices_dataframe_pre.rename(columns={"X": "P"})
        results_effect = prices_dataframe_pre.merge(winner_dataframe_pre, how='left', on=['level_0', 'level_1'])
        results_effect= results_effect[results_effect['X'] != 0]
        results_dict = pd.Series(results_effect.P.values, index=results_effect.level_1).to_dict()
        priceVector_plot(set_items, actual_winning_bids_list, estimated_prices_list, results_dict, demanded_quantities_list)
       
    except ValueError:
        st.warning("No feasible Solution exists!")

"""Scatter Plot Function"""
def priceVector_plot(list_items, actual_winning_bids_list, estimated_prices_list, total_price_model_suggestion, demanded_quantities_list):
    st.markdown('---')
    st.markdown('### Pricing Determination')
    total_expected_expense_price = [a*b for a,b in zip(estimated_prices_list, demanded_quantities_list)]
    total_actual_winning_bid_price = [a*b for a,b in zip(actual_winning_bids_list, demanded_quantities_list)]
    dataframe = pd.DataFrame(list(zip(list_items, total_expected_expense_price, total_actual_winning_bid_price)), columns=['Items', 'Expected Pricing', 'Actual Winning Pricing'])    
    # st.write(demanded_quantities_list)
    # st.write(total_price_model_suggestion)

    # Adjusting price found per unit to the whole quantity
    total_price_model_suggestion = collections.OrderedDict(sorted(total_price_model_suggestion.items()))
    # st.write(total_price_model_suggestion)
    quantity_mapper = collections.OrderedDict(sorted(dict(zip(list_items, demanded_quantities_list)).items()))
    # st.write(quantity_mapper)
    total_adjusted_for_quantity = {k: total_price_model_suggestion[k]*quantity_mapper[k] for k in quantity_mapper}
    # st.write(total_adjusted_for_quantity)

    dataframe['Model Suggested Pricing'] = dataframe['Items'].map(total_adjusted_for_quantity)
    # st.write(dataframe)

    figOne = px.scatter(dataframe, x=['Expected Pricing', 'Actual Winning Pricing', 'Model Suggested Pricing'], y="Items",
                labels={
                     "value": "Pricing",
                     "variable": "Pricing Models"
                 })
    

    figTwo = px.box(dataframe, y=['Expected Pricing', 'Actual Winning Pricing', 'Model Suggested Pricing'], x="Items",
                    # points="all",
                    labels={
                     "value": "Pricing",
                     "variable": "Pricing Models"
                 })
    
    figOne.update_traces(marker_size=10)

    col1, col2 = st.columns(2)
    col1.plotly_chart(figOne, use_container_width=True)
    col2.plotly_chart(figTwo, use_container_width=True)


"""Heat Map Plot Function"""
def auctionWinners_HeatMap(winner_dataframe):
    st.markdown('---')
    st.markdown('### Auction Winners')
    fig = px.imshow(winner_dataframe,
                labels=dict(x="Suppliers", y="Items"),
                x=winner_dataframe.columns,
                y=winner_dataframe.index)
    
    fig.update_xaxes(type='category')
    st.plotly_chart(fig, use_container_width=True)
    

""" 
The redirect code was developed different streamlit community members as discussed in this 
issue / feature forum discussion: https://discuss.streamlit.io/t/cannot-print-the-terminal-output-in-streamlit/6602/25.
It has been adapted by myself to work in the newest versions of streamlit.
"""
@contextmanager
def st_redirect(src, dst):
    placeholder = st.empty()
    output_func = getattr(placeholder, dst)

    with StringIO() as buffer:
        old_write = src.write

        def new_write(b):
            if getattr(current_thread(), SCRIPT_RUN_CONTEXT_ATTR_NAME, None):
                buffer.write(b + '')
                output_func(buffer.getvalue() + '')
            else:
                old_write(b)

        try:
            src.write = new_write
            yield
        finally:
            src.write = old_write

@contextmanager
def st_stdout(dst):
    "this will show the prints"
    with st_redirect(sys.stdout, dst):
        yield

@contextmanager
def st_stderr(dst):
    "This will show the logging"
    with st_redirect(sys.stderr, dst):
        yield

""" Helper method to print model components into streamlit """
def print_into_streamlit(title, model_component):
    msg = "###### {}".format(title)
    st.markdown(msg)
    with st_stdout("code"):
        model_component.pprint()
