import streamlit as st
from pathlib import Path

section_dir = Path(__file__).resolve().parent.parent



st.markdown(
    '''
    <p style='text-align: center;
    color: #000000;'>
    A general description of the report.

    It should test all major components which are available
    to be integrated into VueGen.

    Check our tests folder for examples of report files used to generate actual reports:
    [basic_example_vuegen_demo_notebook](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/docs/example_data/Basic_example_vuegen_demo_notebook)
    </p>
    ''',
    unsafe_allow_html=True)

plot_file_path = '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/home_image.png'

st.image((section_dir / plot_file_path).resolve().as_posix(), use_column_width=True)
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
