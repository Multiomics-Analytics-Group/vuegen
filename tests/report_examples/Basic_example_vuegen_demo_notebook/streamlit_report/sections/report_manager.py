import os
import time

import psutil
import streamlit as st

st.set_page_config(layout="wide",
                   page_title="Basic Example Vuegen Demo Notebook")

st.markdown(
    '''
    <h1 style='text-align: center;
    color: #023858;'>
    Basic Example Vuegen Demo Notebook
    </h1>
    ''',
    unsafe_allow_html=True)


sections_pages = {}
homepage = st.Page('Home/Homepage.py', title='Homepage')
sections_pages['Home'] = [homepage]

Interactive_Plots = st.Page('Plots/Interactive_Plots.py', title='Interactive Plots')
Static_Plots = st.Page('Plots/Static_Plots.py', title='Static Plots')
sections_pages['Plots'] = [Interactive_Plots, Static_Plots]

All_Formats = st.Page('Dataframes/All_Formats.py', title='All Formats')
sections_pages['Dataframes'] = [All_Formats]

Interactive_Networks = st.Page('Networks/Interactive_Networks.py', title='Interactive Networks')
Static_Networks = st.Page('Networks/Static_Networks.py', title='Static Networks')
sections_pages['Networks'] = [Interactive_Networks, Static_Networks]

All_Html = st.Page('Html/All_Html.py', title='All Html')
sections_pages['Html'] = [All_Html]

All_Markdown = st.Page('Markdown/All_Markdown.py', title='All Markdown')
sections_pages['Markdown'] = [All_Markdown]

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
