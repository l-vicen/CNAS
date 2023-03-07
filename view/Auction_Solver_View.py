import streamlit as st
import model.BilevelSolver as bls
import data.DataBase as db

def solve_auction():
    st.title("SOLVER: Bilevel Programming")

    df = db.get_db()
    st.dataframe(df)


    bls.build_model()
