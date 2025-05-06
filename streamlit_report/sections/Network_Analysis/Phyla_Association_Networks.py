df_index = 1
import requests
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import streamlit as st

st.markdown('''<h3 style='text-align: center; color: #023558;'>Phyla Association Networks</h3>''', unsafe_allow_html=True)
st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Phyla Counts Subset</h4>''', unsafe_allow_html=True)
df = pd.read_csv('example_data/Earth_microbiome_vuegen_demo_notebook/3_Network_analysis/1_phyla_association_networks/1_phyla_counts_subset.csv')


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
st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Phyla Correlation Network With 0.5 Threshold Edgelist</h4>''', unsafe_allow_html=True)

with open('streamlit_report/static/Phyla_Correlation_Network_With_0.5_Threshold_Edgelist.html', 'r') as f:
    html_data = f.read()


st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of nodes:</b> 33 </p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of relationships:</b> 42 </p>", unsafe_allow_html=True)

# Streamlit checkbox for controlling the layout
control_layout = st.checkbox('Add panel to control layout', value=True)
net_html_height = 1200 if control_layout else 630
# Load HTML into HTML component for display on Streamlit
st.components.v1.html(html_data, height=net_html_height)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Phyla Correlation Network With 0.5 Threshold</h4>''', unsafe_allow_html=True)

st.image('example_data/Earth_microbiome_vuegen_demo_notebook/3_Network_analysis/1_phyla_association_networks/3_phyla_correlation_network_with_0.5_threshold.png', caption='', use_column_width=True)

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
