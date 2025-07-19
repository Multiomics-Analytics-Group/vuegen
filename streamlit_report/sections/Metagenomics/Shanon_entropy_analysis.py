from pathlib import Path
import streamlit as st
section_dir = Path(__file__).resolve().parent.parent

st.markdown(
    '''
    <h3 style='text-align: center;
    color: #023558;'>
    Shanon entropy analysis
    </h3>
    ''',
    unsafe_allow_html=True)

st.markdown(
    '''
    <p style='text-align: center;
    color: #000000;'>
    This subsection contains the Shannon entropy analysis of the EMP dataset.
    </p>
    ''',
    unsafe_allow_html=True)

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    Specificity of sequences and higher taxonomic groups for environment
    </h4>
    ''',
    unsafe_allow_html=True)

plot_file_path = 'https://raw.githubusercontent.com/biocore/emp/master/methods/images/figure4_entropy.png'
st.image(plot_file_path, caption='a) Environment distribution in all genera and 400 randomly chosen tag sequence. b) and c) Shannon entropy within each taxonomic group.', use_column_width=True)

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
