import requests
import json
import streamlit as st

st.markdown('''<h3 style='text-align: center; color: #023558;'>Average Copy Number</h3>''', unsafe_allow_html=True)
st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Average Copy Number Emp Ontology Level2</h4>''', unsafe_allow_html=True)

st.image('/home/runner/work/vuegen/vuegen/docs/example_data/Earth_microbiome_vuegen_demo_notebook/2_Metagenomics/2_average_copy_number/1_average_copy_number_emp_ontology_level2.png', caption='', use_column_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Average Copy Number Emp Ontology Level3</h4>''', unsafe_allow_html=True)

with open('/home/runner/work/vuegen/vuegen/docs/example_data/Earth_microbiome_vuegen_demo_notebook/2_Metagenomics/2_average_copy_number/2_average_copy_number_emp_ontology_level3.json', 'r') as plot_file:
    plot_json = json.load(plot_file)
st.plotly_chart(plot_json, use_container_width=True)

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
    | © 2025 <a href="https://github.com/Multiomics-Analytics-Group" target="_blank">
        Multiomics Network Analytics Group (MoNA)
    </a>
</footer>'''

st.markdown(footer, unsafe_allow_html=True)
