import altair as alt
df_index = 1
from st_aggrid import AgGrid, GridOptionsBuilder
import requests
import json
import streamlit as st
import pandas as pd

st.markdown('''<h3 style='text-align: center; color: #023558;'>Sample Exploration</h3>''', unsafe_allow_html=True)
st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Metadata Random Subset</h4>''', unsafe_allow_html=True)
df = pd.read_csv('example_data/Earth_microbiome_vuegen_demo_notebook/1_Exploratory_data_analysis/1_sample_exploration/1_metadata_random_subset.csv')


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
st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Animal Samples Map</h4>''', unsafe_allow_html=True)

st.image('example_data/Earth_microbiome_vuegen_demo_notebook/1_Exploratory_data_analysis/1_sample_exploration/2_animal_samples_map.png', caption='', use_column_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Plant Samples Map</h4>''', unsafe_allow_html=True)

with open('example_data/Earth_microbiome_vuegen_demo_notebook/1_Exploratory_data_analysis/1_sample_exploration/3_plant_samples_map.json', 'r') as plot_file:
    plot_json = json.load(plot_file)

# Keep only 'data' and 'layout' sections
plot_json = {key: plot_json[key] for key in plot_json if key in ['data', 'layout']}

# Remove 'frame' section in 'data'
plot_json['data'] = [{k: v for k, v in entry.items() if k != 'frame'} for entry in plot_json.get('data', [])]
st.plotly_chart(plot_json, use_container_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Saline Samples Map</h4>''', unsafe_allow_html=True)

with open('example_data/Earth_microbiome_vuegen_demo_notebook/1_Exploratory_data_analysis/1_sample_exploration/4_saline_samples_map.json', 'r') as plot_file:
    plot_json = json.load(plot_file)

altair_plot = alt.Chart.from_dict(plot_json)
st.vega_lite_chart(json.loads(altair_plot.to_json()), use_container_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Physicochemical properties of the EMP samples</h4>''', unsafe_allow_html=True)

st.image('https://raw.githubusercontent.com/biocore/emp/master/methods/images/figureED1_physicochemical.png', caption='Pairwise scatter plots of available physicochemical metadat are shown for temperature, salinity, oxygen, and pH, and for phosphate, nitrate, and ammonium', use_column_width=True)

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
