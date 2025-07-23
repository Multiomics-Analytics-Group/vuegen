from pathlib import Path
import altair as alt
import json
import requests
import streamlit as st
section_dir = Path(__file__).resolve().parent.parent

st.markdown(
    '''
    <h3 style='text-align: center;
    color: #023558;'>
    Interactive Plots
    </h3>
    ''',
    unsafe_allow_html=True)

st.markdown(
    '''
    <p style='text-align: center;
    color: #000000;'>
    Optional description for section.
    </p>
    ''',
    unsafe_allow_html=True)

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    Top Species Plot By Biome Plotly
    </h4>
    ''',
    unsafe_allow_html=True)


file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/1_top_species_plot_by_biome_plotly.json').resolve().as_posix()
with open(file_path, 'r') as plot_file:
    plot_json = json.load(plot_file)

# Keep only 'data' and 'layout' sections
plot_json = {key: plot_json[key] for key in plot_json
                                 if key in ['data', 'layout']}

# Remove 'frame' section in 'data'
plot_json['data'] = [{k: v for k, v in entry.items() if k != 'frame'}
                                for entry in plot_json.get('data', [])]
st.plotly_chart(plot_json, use_container_width=True)

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    Multiline Plot Altair
    </h4>
    ''',
    unsafe_allow_html=True)


file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/2_multiline_plot_altair.json').resolve().as_posix()
with open(file_path, 'r') as plot_file:
    plot_json = json.load(plot_file)

altair_plot = alt.Chart.from_dict(plot_json)
st.vega_lite_chart(json.loads(altair_plot.to_json()),
                   use_container_width=True)

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    Pie Plot Countries Plotly
    </h4>
    ''',
    unsafe_allow_html=True)


file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/3_pie_plot_countries_plotly.json').resolve().as_posix()
with open(file_path, 'r') as plot_file:
    plot_json = json.load(plot_file)

# Keep only 'data' and 'layout' sections
plot_json = {key: plot_json[key] for key in plot_json
                                 if key in ['data', 'layout']}

# Remove 'frame' section in 'data'
plot_json['data'] = [{k: v for k, v in entry.items() if k != 'frame'}
                                for entry in plot_json.get('data', [])]
st.plotly_chart(plot_json, use_container_width=True)

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    Pie Plots Biomes Plotly
    </h4>
    ''',
    unsafe_allow_html=True)


file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/4_pie_plots_biomes_plotly.json').resolve().as_posix()
with open(file_path, 'r') as plot_file:
    plot_json = json.load(plot_file)

# Keep only 'data' and 'layout' sections
plot_json = {key: plot_json[key] for key in plot_json
                                 if key in ['data', 'layout']}

# Remove 'frame' section in 'data'
plot_json['data'] = [{k: v for k, v in entry.items() if k != 'frame'}
                                for entry in plot_json.get('data', [])]
st.plotly_chart(plot_json, use_container_width=True)

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    Saline Metagenomics Samples Map Altair
    </h4>
    ''',
    unsafe_allow_html=True)


file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/5_saline_metagenomics_samples_map_altair.json').resolve().as_posix()
with open(file_path, 'r') as plot_file:
    plot_json = json.load(plot_file)

altair_plot = alt.Chart.from_dict(plot_json)
st.vega_lite_chart(json.loads(altair_plot.to_json()),
                   use_container_width=True)

st.markdown(
    '''
    <h4 style='text-align: center;
    color: #2b8cbe;'>
    Description
    </h4>
    ''',
    unsafe_allow_html=True)


file_path = (section_dir / '../../../../../docs/example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/description.md').resolve().as_posix()
with open(file_path, 'r') as markdown_file:
    markdown_content = markdown_file.read()

st.markdown(markdown_content, unsafe_allow_html=True)

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
