import streamlit as st
from pathlib import Path
section_dir = Path(__file__).resolve().parent.parent

st.markdown(
    '''
    <h3 style='text-align: center;
    color: #023558;'>
    Static Plots
    </h3>
    ''',
    unsafe_allow_html=True)

st.markdown(
    '''
    <p style='text-align: center;
    color: #000000;'>
    Static plots.
    </p>
    ''',
    unsafe_allow_html=True)

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
