# 3rd party library dependencies
import streamlit as st
import view.Get_Data_Set_View as get_view
import view.Post_Data_Set_View as post_view
import view.Auction_Solver_View as auction_solver_view

# App global config setting
st.set_page_config(layout="wide")

# Side Bar Class Declaration
st.sidebar.image('assets/tum_logo.png')
st.sidebar.markdown('---')

# Sidebar attributes
features = ['Get Data', 'Insert Data', 'Solve Auction']
page = st.sidebar.selectbox('Choose Page', features)
st.sidebar.markdown('---')

if page == features[0]:
    get_view.get_data_set_view()
elif page == features[1]:
    post_view.insert_into_data_set_view()
else:
    auction_solver_view.solve_auction()

st.sidebar.markdown('##### Creator')
st.sidebar.markdown('Lucas Perasolo')
st.sidebar.markdown('---')