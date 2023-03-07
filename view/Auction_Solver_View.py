import streamlit as st
import model.Bilevel_Programming as bls
import model.Solver_Parser as sl
import data.DataBase as db


def solve_auction():
    st.title("SOLVER: Bilevel Programming")

    dataframe = db.get_db()

    st.write(sl.get_items_auctioned(1530740900092006, dataframe))

    bls.build_model()
