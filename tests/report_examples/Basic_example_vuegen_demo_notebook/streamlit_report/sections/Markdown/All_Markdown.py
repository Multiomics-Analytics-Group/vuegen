from pathlib import Path
import requests
import streamlit as st
section_dir = Path(__file__).resolve().parent.parent


st.markdown(
    (
        "<h3 style='text-align: center; "
        "color: #023558;'>All Markdown</h3>"
    ),
    unsafe_allow_html=True)


st.markdown(
    (
        "<h4 style='text-align: center; "
        "color: #2b8cbe;'>Readme</h4>"
    ),
    unsafe_allow_html=True)


file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/5_Markdown/1_All_markdown/README.md').resolve().as_posix()
with open(file_path, 'r') as markdown_file:
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
