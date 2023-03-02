import streamlit as st

class SideBar:

    def start(self):
        """Side Bar Class Declaration""" 

        st.sidebar.image('assets/tum_logo.png')
        st.sidebar.markdown('---')

        # Sidebar attributes
        features = ['Home Page', 'Solve Auction', 'Data Set']
        page = st.sidebar.selectbox('Choose Page', features)
        st.sidebar.markdown('---')

        if page == features[0]:
            pass

        elif page == features[1]:
            pass

        else:
            pass

        st.sidebar.markdown('---')
        st.sidebar.markdown('##### Creator')
        st.sidebar.markdown('Lucas Perasolo')
        st.sidebar.markdown('---')
