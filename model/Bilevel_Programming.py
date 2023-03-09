from pyomo.environ import *
from pao.pyomo import *

import streamlit as st
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
    return sum(model.Supply_capacity[j,i] * model.X[j,i] for j in model.j) == model.Demand[i]

def lower_and_upper_bound_constraint(submodel, j, i):
    return (submodel.Production_Costs[j,i], submodel.P[j,i], submodel.Budget[i])

def build_model(set_items, set_suppliers, demand_dictionary, utility_dictionary, supplier_capacity_dictionary, budget_dictionary, production_costs_dictionary):
    
    # Upper-level definition: Auction Problem
    model = ConcreteModel("Upper-level: Auction Problem")

    '''   Model Subscripts
    model.i := Set of auctioned items.
    model.j := Set of auction participating suppliers.
    '''
    model.i = Set(initialize=set_items, doc='Auctioned_Items')
    print_into_streamlit("Auctioned Items", model.i)

    model.j = Set(initialize=set_suppliers, doc='Auction_Participating_Suppliers')
    print_into_streamlit("Participating Suppliers in Auction", model.j)

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
    model.Demand = Param(model.i, initialize= demand_dictionary, doc='Auctioneer\'s_Demand_per_Item')
    print_into_streamlit("Auctioneer's Demand per Item", model.Demand)

    model.Utility = Param(model.i, initialize= utility_dictionary, doc='Auctioneer\'s_Perceived_Utility_per_Item')
    print_into_streamlit("Auctioneer's Perceived Utility per Item",  model.Utility)

    model.Supply_capacity = Param(model.j, model.i, initialize= supplier_capacity_dictionary, doc='Suppliers\'_individual_Supply_Capacity_per_Item')
    print_into_streamlit("Suppliers\' individual Supply Capacity per Item",   model.Supply_capacity)

    model.L.Budget = Param(model.i, initialize= budget_dictionary, doc='Auctioneer\'s_expected_Expense_per_Items')
    print_into_streamlit("Auctioneer's expected Expense per Items",  model.L.Budget)

    model.L.Production_Costs = Param(model.j, model.i, initialize = production_costs_dictionary , doc='Suppliers\'_individual_Production_Cost_per_Item')
    print_into_streamlit("Suppliers\' individual Production Cost per Item",  model.L.Production_Costs)

    # Objective function assignments
    model.o = Objective(rule=auction_objective_function(model), sense=maximize, doc='Auction_Problem') # Upper-level 
    print_into_streamlit("Upper-level Objective Function",  model.o)

    model.L.o = Objective(rule= pricing_objective_function(model.L, model), sense=maximize, doc='Pricing_Problem') # Lower-level
    print_into_streamlit("Lower-level Objective Function",  model.L.o)

    # Upper-level constraint assignments
    model.SingleSourcingConstraint = Constraint(model.i, rule=single_sourcing_constraint, doc='There_is_at_most_1_winner')
    print_into_streamlit("Single Sourcing Constraint",  model.SingleSourcingConstraint)

    model.DemandConstraint = Constraint(model.i, rule=demand_requirement_constraint, doc='Auctioneer\'s_Demand_is_fulfilled')
    print_into_streamlit("Demand Constraint",  model.DemandConstraint)

    # Lower-level constraint assignment
    model.L.BidPriceBoundaryConstraint = Constraint(model.j, model.i, rule=lower_and_upper_bound_constraint, doc='Bid_Price_is_non-negative')
    print_into_streamlit("Bid Price Constraint",  model.L.BidPriceBoundaryConstraint)

    # Calling the Big-M Relaxation Solver
    solver = Solver('pao.pyomo.FA')
    solver.solve(model)   

    with st_stdout("code"):
        model.pprint()


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

""" Helper method to print model components into streamlit """
def print_into_streamlit(title, model_component):
    msg = "###### {}".format(title)
    st.markdown(msg)
    with st_stdout("code"):
        model_component.pprint()
