import os
import time

import psutil                    
import streamlit as st

st.set_page_config(layout="wide", page_title="Earth Microbiome Vuegen Demo Notebook", page_icon="https://raw.githubusercontent.com/ElDeveloper/cogs220/master/emp-logo.svg")
st.logo("https://raw.githubusercontent.com/ElDeveloper/cogs220/master/emp-logo.svg")

st.markdown('''<h1 style='text-align: center; color: #023858;'>Earth Microbiome Vuegen Demo Notebook</h1>''', unsafe_allow_html=True)

sections_pages = {}
homepage = st.Page('Home/Homepage.py', title='Homepage')
sections_pages['Home'] = [homepage]

Sample_Exploration = st.Page('Exploratory_Data_Analysis/Sample_Exploration.py', title='Sample Exploration')
sections_pages['Exploratory Data Analysis'] = [Sample_Exploration]

Alpha_Diversity = st.Page('Metagenomics/Alpha_Diversity.py', title='Alpha Diversity')
Average_Copy_Number = st.Page('Metagenomics/Average_Copy_Number.py', title='Average Copy Number')
Nestedness = st.Page('Metagenomics/Nestedness.py', title='Nestedness')
Shanon_entropy_analysis = st.Page('Metagenomics/Shanon_entropy_analysis.py', title='Shanon entropy analysis')
sections_pages['Metagenomics'] = [Alpha_Diversity, Average_Copy_Number, Nestedness, Shanon_entropy_analysis]

Phyla_Association_Networks = st.Page('Network_Analysis/Phyla_Association_Networks.py', title='Phyla Association Networks')
sections_pages['Network Analysis'] = [Phyla_Association_Networks]

report_nav = st.navigation(sections_pages)

# Following https://discuss.streamlit.io/t/close-streamlit-app-with-button-click/35132/5
exit_app = st.sidebar.button("Shut Down App", icon=":material/power_off:", use_container_width=True)
if exit_app:
    st.toast("Shutting down the app...")
    time.sleep(1)
    # Terminate streamlit python process
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()


report_nav.run()
