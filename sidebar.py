import streamlit as st

class SideBar:
    """Side Bar Class Declaration""" 

    # Sidebar attribute Logo
    def sidebar_functionality(self):
        st.sidebar.image('assets/tum_logo.png')
        st.sidebar.markdown('---')

    def sidebar_contact(self):
        st.sidebar.markdown('##### Creator')
        st.sidebar.markdown('Lucas Perasolo')
        st.sidebar.markdown('---')