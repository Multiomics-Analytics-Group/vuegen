df_index = 1
import json
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import requests
import streamlit as st

st.markdown('''<h3 style='text-align: center; color: #023558;'>Nestedness</h3>''', unsafe_allow_html=True)
st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Nestedness Random Subset</h4>''', unsafe_allow_html=True)
df = pd.read_csv('example_data/Earth_microbiome_vuegen_demo_notebook/2_Metagenomics/3_nestedness/1_nestedness_random_subset.csv')


# Displays a DataFrame using AgGrid with configurable options.
grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_builder.configure_default_column(editable=True, groupable=True)
grid_builder.configure_side_bar(filters_panel=True, columns_panel=True)
grid_builder.configure_selection(selection_mode="multiple")
grid_builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=20)
grid_options = grid_builder.build()

AgGrid(df, gridOptions=grid_options)

# Button to download the df
df_csv = df.to_csv(sep=',', header=True, index=False).encode('utf-8')
st.download_button(
    label="Download dataframe as CSV",
    data=df_csv,
    file_name=f"dataframe_{df_index}.csv",
    mime='text/csv',
    key=f"download_button_{df_index}")
df_index += 1
st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>All Samples</h4>''', unsafe_allow_html=True)

with open('example_data/Earth_microbiome_vuegen_demo_notebook/2_Metagenomics/3_nestedness/2_all_samples.json', 'r') as plot_file:
    plot_json = json.load(plot_file)
st.plotly_chart(plot_json, use_container_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Plant Samples</h4>''', unsafe_allow_html=True)

with open('example_data/Earth_microbiome_vuegen_demo_notebook/2_Metagenomics/3_nestedness/3_plant_samples.json', 'r') as plot_file:
    plot_json = json.load(plot_file)
st.plotly_chart(plot_json, use_container_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Animal Samples</h4>''', unsafe_allow_html=True)

st.image('example_data/Earth_microbiome_vuegen_demo_notebook/2_Metagenomics/3_nestedness/4_animal_samples.png', caption='', use_column_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Non Saline Samples</h4>''', unsafe_allow_html=True)

st.image('example_data/Earth_microbiome_vuegen_demo_notebook/2_Metagenomics/3_nestedness/5_non_saline_samples.png', caption='', use_column_width=True)

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
