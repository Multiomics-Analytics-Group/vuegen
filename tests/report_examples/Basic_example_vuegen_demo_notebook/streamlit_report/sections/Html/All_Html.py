import requests
import streamlit as st

st.markdown('''<h3 style='text-align: center; color: #023558;'>All Html</h3>''', unsafe_allow_html=True)
st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Plot</h4>''', unsafe_allow_html=True)

with open('docs/example_data/Basic_example_vuegen_demo_notebook/4_Html/1_All_html/1_plot.html', 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

st.components.v1.html(html_content, height=600, scrolling=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Ckg Network</h4>''', unsafe_allow_html=True)

with open('docs/example_data/Basic_example_vuegen_demo_notebook/4_Html/1_All_html/2_ckg_network.html', 'r') as html_file:
    html_content = html_file.read()


st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of nodes:</b> 33 </p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of relationships:</b> 35 </p>", unsafe_allow_html=True)

# Streamlit checkbox for controlling the layout
control_layout = st.checkbox('Add panel to control layout', value=True)
net_html_height = 1200 if control_layout else 630
# Load HTML into HTML component for display on Streamlit
st.components.v1.html(html_content, height=net_html_height)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Multiqc Report</h4>''', unsafe_allow_html=True)

with open('docs/example_data/Basic_example_vuegen_demo_notebook/4_Html/1_All_html/3_multiqc_report.html', 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

st.components.v1.html(html_content, height=600, scrolling=True)

footer = '''<style type="text/css">
.footer {
    position: relative;
    left: 0;
    width: 100%;
    text-align: center;
}
</style>
<footer class="footer">
    This report was generated with 
    <a href="https://github.com/Multiomics-Analytics-Group/vuegen" target="_blank">
        <img src="https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_logo.svg" alt="VueGen" width="65px">
    </a>
    | Copyright 2025 <a href="https://github.com/Multiomics-Analytics-Group" target="_blank">
        Multiomics Network Analytics Group (MoNA)
    </a>
</footer>'''

st.markdown(footer, unsafe_allow_html=True)
