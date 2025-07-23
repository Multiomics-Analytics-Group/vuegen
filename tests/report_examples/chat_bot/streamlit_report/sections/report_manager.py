import os
import time

import psutil
import streamlit as st

st.set_page_config(layout="wide",
                   page_title="Chatbot example")

st.markdown(
    '''
    <h1 style='text-align: center;
    color: #023858;'>
    Chatbot example
    </h1>
    ''',
    unsafe_allow_html=True)


sections_pages = {}
homepage = st.Page('Home/Homepage.py', title='Homepage')
sections_pages['Home'] = [homepage]

Simple_test = st.Page('ChatBot_test/Simple_test.py', title='Simple test')
sections_pages['ChatBot test'] = [Simple_test]

report_nav = st.navigation(sections_pages)

# Following https://discuss.streamlit.io/t/close-streamlit-app-with-button-click/35132/5
exit_app = st.sidebar.button("Shut Down App",
                             icon=":material/power_off:",
                             use_container_width=True)
if exit_app:
    st.toast("Shutting down the app...")
    time.sleep(1)
    # Terminate streamlit python process
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()


report_nav.run()
