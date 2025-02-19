import streamlit as st

st.markdown('''<h3 style='text-align: center; color: #023558;'>Static Plots</h3>''', unsafe_allow_html=True)
st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Number Samples Per Study</h4>''', unsafe_allow_html=True)

st.image('example_data/Basic_example_vuegen_demo_notebook/1_Plots/2_Static_plots/1_number_samples_per_study.png', caption='', use_column_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Animal Metagenomics Samples Map</h4>''', unsafe_allow_html=True)

st.image('example_data/Basic_example_vuegen_demo_notebook/1_Plots/2_Static_plots/2_animal_metagenomics_samples_map.png', caption='', use_column_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Alpha Diversity Host Associated Samples</h4>''', unsafe_allow_html=True)

st.image('example_data/Basic_example_vuegen_demo_notebook/1_Plots/2_Static_plots/3_alpha_diversity_host_associated_samples.png', caption='', use_column_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Graphical overview of VueGen’s workflow and components</h4>''', unsafe_allow_html=True)

st.image('https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_graph_abstract.png', caption='The diagram illustrates the processing pipeline of VueGen, starting from either a directory or a YAML configuration file. Reports consist of hierarchical sections and subsections, each containing various components such as plots, dataframes, Markdown, HTML, and data retrieved via API calls.', use_column_width=True)

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
