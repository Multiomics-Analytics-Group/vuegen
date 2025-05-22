import streamlit as st
import streamlit as st
import requests
st.markdown('''<p style='text-align: center; color: #000000;'>The Earth Microbiome Project (EMP) is a systematic attempt to characterize global microbial taxonomic and functional diversity for the benefit of the planet and humankind. 
  It aimed to sample the Earth’s microbial communities at an unprecedented scale in order to advance our understanding of the organizing biogeographic principles that govern microbial community structure. 
  The EMP dataset is generated from samples that individual researchers have compiled and contributed to the EMP. 
  The result is both a reference database giving global context to DNA sequence data and a framework for incorporating data from future studies, fostering increasingly complete characterization of Earth’s microbial diversity.
  
  You can find more information about the Earth Microbiome Project at https://earthmicrobiome.org/ and in the [original article](https://www.nature.com/articles/nature24621).
</p>''', unsafe_allow_html=True)

st.image('https://raw.githubusercontent.com/ElDeveloper/cogs220/master/emp-logo.svg', use_column_width=True)
st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Description</h4>''', unsafe_allow_html=True)

with open('example_data/Earth_microbiome_vuegen_demo_notebook/description.md', 'r') as markdown_file:
    markdown_content = markdown_file.read()

st.markdown(markdown_content, unsafe_allow_html=True)

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
