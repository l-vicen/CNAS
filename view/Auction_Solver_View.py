import streamlit as st
import model.BilevelSolver as bls
import data.DataBase as db
import model.Parser as ps

def solve_auction():
    st.title("SOLVER: Bilevel Programming")

    dataframe = db.get_db()

    st.write(ps.get_items_auctioned(1530740900092006, dataframe))

    bls.build_model()
