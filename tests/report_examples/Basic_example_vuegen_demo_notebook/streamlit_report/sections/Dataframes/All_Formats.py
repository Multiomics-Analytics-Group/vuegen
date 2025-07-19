from pathlib import Path
from st_aggrid import AgGrid, GridOptionsBuilder
from vuegen import table_utils
import pandas as pd
import streamlit as st
df_index = 1
section_dir = Path(__file__).resolve().parent.parent

st.markdown(
    '''
    <h3 style='text-align: center;
    color: #023558;'>
    All Formats
    </h3>
    ''',
    unsafe_allow_html=True)

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    Phyla Correlation Network Csv
    </h4>
    ''',
    unsafe_allow_html=True)

file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/2_Dataframes/1_All_formats/1_phyla_correlation_network_csv.csv').resolve().as_posix()
df = pd.read_csv(file_path)


# Displays a DataFrame using AgGrid with configurable options.
grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_builder.configure_default_column(editable=True,
                                      groupable=True,
                                      filter=True,
)
grid_builder.configure_side_bar(filters_panel=True,
                                columns_panel=True)
grid_builder.configure_selection(selection_mode="multiple")
grid_builder.configure_pagination(enabled=True,
                                paginationAutoPageSize=False,
                                paginationPageSize=20,
)
grid_options = grid_builder.build()

AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)

# Button to download the df
df_csv = df.to_csv(sep=',', header=True, index=False
                  ).encode('utf-8')
st.download_button(
    label="Download dataframe as CSV",
    data=df_csv,
    file_name=f"dataframe_{df_index}.csv",
    mime='text/csv',
    key=f"download_button_{df_index}")
df_index += 1
st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    Abundance Table Example Xls
    </h4>
    ''',
    unsafe_allow_html=True)

selected_sheet = 0
file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/2_Dataframes/1_All_formats/2_abundance_table_example_xls.xls').resolve().as_posix()
sheet_names = table_utils.get_sheet_names(file_path)
selected_sheet = st.selectbox("Select a sheet to display",
                              options=sheet_names,
                )

file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/2_Dataframes/1_All_formats/2_abundance_table_example_xls.xls').resolve()
df = pd.read_excel(file_path, sheet_name=selected_sheet)


# Displays a DataFrame using AgGrid with configurable options.
grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_builder.configure_default_column(editable=True,
                                      groupable=True,
                                      filter=True,
)
grid_builder.configure_side_bar(filters_panel=True,
                                columns_panel=True)
grid_builder.configure_selection(selection_mode="multiple")
grid_builder.configure_pagination(enabled=True,
                                paginationAutoPageSize=False,
                                paginationPageSize=20,
)
grid_options = grid_builder.build()

AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)

# Button to download the df
df_csv = df.to_csv(sep=',', header=True, index=False
                  ).encode('utf-8')
st.download_button(
    label="Download dataframe as CSV",
    data=df_csv,
    file_name=f"dataframe_{df_index}.csv",
    mime='text/csv',
    key=f"download_button_{df_index}")
df_index += 1
st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    Sample Info Example Txt
    </h4>
    ''',
    unsafe_allow_html=True)

file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/2_Dataframes/1_All_formats/3_sample_info_example_txt.txt').resolve().as_posix()
df = pd.read_table(file_path)


# Displays a DataFrame using AgGrid with configurable options.
grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_builder.configure_default_column(editable=True,
                                      groupable=True,
                                      filter=True,
)
grid_builder.configure_side_bar(filters_panel=True,
                                columns_panel=True)
grid_builder.configure_selection(selection_mode="multiple")
grid_builder.configure_pagination(enabled=True,
                                paginationAutoPageSize=False,
                                paginationPageSize=20,
)
grid_options = grid_builder.build()

AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)

# Button to download the df
df_csv = df.to_csv(sep=',', header=True, index=False
                  ).encode('utf-8')
st.download_button(
    label="Download dataframe as CSV",
    data=df_csv,
    file_name=f"dataframe_{df_index}.csv",
    mime='text/csv',
    key=f"download_button_{df_index}")
df_index += 1
st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    Sample Info Example Parquet
    </h4>
    ''',
    unsafe_allow_html=True)

file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/2_Dataframes/1_All_formats/4_sample_info_example_parquet.parquet').resolve().as_posix()
df = pd.read_parquet(file_path)


# Displays a DataFrame using AgGrid with configurable options.
grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_builder.configure_default_column(editable=True,
                                      groupable=True,
                                      filter=True,
)
grid_builder.configure_side_bar(filters_panel=True,
                                columns_panel=True)
grid_builder.configure_selection(selection_mode="multiple")
grid_builder.configure_pagination(enabled=True,
                                paginationAutoPageSize=False,
                                paginationPageSize=20,
)
grid_options = grid_builder.build()

AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)

# Button to download the df
df_csv = df.to_csv(sep=',', header=True, index=False
                  ).encode('utf-8')
st.download_button(
    label="Download dataframe as CSV",
    data=df_csv,
    file_name=f"dataframe_{df_index}.csv",
    mime='text/csv',
    key=f"download_button_{df_index}")
df_index += 1
st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    Example Xlsx
    </h4>
    ''',
    unsafe_allow_html=True)

selected_sheet = 0
file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/2_Dataframes/1_All_formats/5_example_xlsx.xlsx').resolve()
df = pd.read_excel(file_path, sheet_name=selected_sheet)


# Displays a DataFrame using AgGrid with configurable options.
grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_builder.configure_default_column(editable=True,
                                      groupable=True,
                                      filter=True,
)
grid_builder.configure_side_bar(filters_panel=True,
                                columns_panel=True)
grid_builder.configure_selection(selection_mode="multiple")
grid_builder.configure_pagination(enabled=True,
                                paginationAutoPageSize=False,
                                paginationPageSize=20,
)
grid_options = grid_builder.build()

AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)

# Button to download the df
df_csv = df.to_csv(sep=',', header=True, index=False
                  ).encode('utf-8')
st.download_button(
    label="Download dataframe as CSV",
    data=df_csv,
    file_name=f"dataframe_{df_index}.csv",
    mime='text/csv',
    key=f"download_button_{df_index}")
df_index += 1
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
