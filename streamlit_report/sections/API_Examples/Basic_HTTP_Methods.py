from pathlib import Path
import streamlit as st
section_dir = Path(__file__).resolve().parent.parent

st.markdown(
    '''
    <h3 style='text-align: center;
    color: #023558;'>
    Basic HTTP Methods
    </h3>
    ''',
    unsafe_allow_html=True)

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    GET request
    </h4>
    ''',
    unsafe_allow_html=True)

st.write({'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False})

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    POST request
    </h4>
    ''',
    unsafe_allow_html=True)

st.write({'userId': 1, 'title': 'Go running', 'completed': False, 'id': 201})

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    PUT request
    </h4>
    ''',
    unsafe_allow_html=True)

st.write({'userId': 1, 'title': 'Play the guitar', 'completed': True, 'id': 10})

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    PATCH request
    </h4>
    ''',
    unsafe_allow_html=True)

st.write({'userId': 1, 'id': 10, 'title': 'Go for a hike', 'completed': True})

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    DELETE request
    </h4>
    ''',
    unsafe_allow_html=True)

st.write({})

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
