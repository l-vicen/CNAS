
import streamlit as st
import sidebar as sb

# Adding sidebar component
sidebar = sb.SideBar()
sidebar.sidebar_functionality()
sidebar.sidebar_contact()

class Router:
    def display_router(self):
        # Sidebar attributes
        self.features = ['Home Page', 'Solve Auction', 'Data Set']
        self.page = sidebar.selectbox('Choose Page', self.features)
        st.sidebar.markdown('---')

    def route(self):        
    
        if self.page == self.features[0]:
            pass

        elif self.page == self.features[1]:
            pass

        else:
            pass