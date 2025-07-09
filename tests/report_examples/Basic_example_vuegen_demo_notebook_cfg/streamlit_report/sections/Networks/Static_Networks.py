import streamlit as st


st.markdown(
    (
        "<h3 style='text-align: center; "
        "color: #023558;'>Static Networks</h3>"
    ),
    unsafe_allow_html=True)


st.markdown(
    (
        "<h4 style='text-align: center; "
        "color: #2b8cbe;'>Phyla Correlation Network</h4>"
    ),
    unsafe_allow_html=True)


st.image('example_data/Basic_example_vuegen_demo_notebook/3_Networks/2_Static_networks/1_phyla_correlation_network.png',  caption='', use_column_width=True)

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
