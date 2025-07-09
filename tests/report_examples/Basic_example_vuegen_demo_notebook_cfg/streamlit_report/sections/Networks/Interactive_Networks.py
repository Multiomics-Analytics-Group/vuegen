import requests
import streamlit as st


st.markdown(
    (
        "<h3 style='text-align: center; "
        "color: #023558;'>Interactive Networks</h3>"
    ),
    unsafe_allow_html=True)


st.markdown(
    (
        "<p style='text-align: center; "
        "color: #000000;'>Optional description for subsection</p>"
    ),
    unsafe_allow_html=True)


st.markdown(
    (
        "<h4 style='text-align: center; "
        "color: #2b8cbe;'>Man Example</h4>"
    ),
    unsafe_allow_html=True)


with open('../tests/report_examples/Basic_example_vuegen_demo_notebook_cfg/streamlit_report/static/Man_Example.html', 'r') as html_file:
    html_content = html_file.read()


st.markdown(("<p style='text-align: center; color: black;'> "
            "<b>Number of nodes:</b> 9 </p>"),
            unsafe_allow_html=True)
st.markdown(("<p style='text-align: center; color: black;'>"
             " <b>Number of relationships:</b> 14"
             " </p>"),
            unsafe_allow_html=True)

# Streamlit checkbox for controlling the layout
control_layout = st.checkbox('Add panel to control layout', value=True)
net_html_height = 1200 if control_layout else 630
# Load HTML into HTML component for display on Streamlit
st.components.v1.html(html_content, height=net_html_height)


st.markdown(
    (
        "<h4 style='text-align: center; "
        "color: #2b8cbe;'>Description</h4>"
    ),
    unsafe_allow_html=True)


with open('example_data/Basic_example_vuegen_demo_notebook/3_Networks/1_Interactive_networks/description.md', 'r') as markdown_file:
    markdown_content = markdown_file.read()

st.markdown(markdown_content, unsafe_allow_html=True)

footer = '''
<style type="text/css">
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
        <img src="https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/HEAD/docs/images/logo/vuegen_logo.svg" alt="VueGen" width="65px">
    </a>
    | Copyright 2025 <a href="https://github.com/Multiomics-Analytics-Group" target="_blank">
        Multiomics Network Analytics Group (MoNA)
    </a>
</footer>
'''

st.markdown(footer, unsafe_allow_html=True)
