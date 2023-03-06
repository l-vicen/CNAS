import streamlit as st
import model.BilevelSolver as bls

def solve_auction():
    st.title("SOLVER: Bilevel Programming")
    bls.build_model()
