import os
import time

import psutil
import streamlit as st

st.set_page_config(layout="wide",
                   page_title="VueGen Chatbot Case Study")


st.markdown(
    (
        "<h1 style='text-align: center; "
        "color: #023858;'>VueGen Chatbot Case Study</h1>"
    ),
    unsafe_allow_html=True)


sections_pages = {}
homepage = st.Page('Home/Homepage.py', title='Homepage')
sections_pages['Home'] = [homepage]

Ollama_style_streaming_chatbot = st.Page('Chatbot_Example/Ollama_style_streaming_chatbot.py', title='Ollama-style streaming chatbot')
sections_pages['Chatbot Example'] = [Ollama_style_streaming_chatbot]

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
