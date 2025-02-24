import altair as alt
import streamlit as st
import requests
import json

st.markdown('''<h3 style='text-align: center; color: #023558;'>Interactive Plots</h3>''', unsafe_allow_html=True)
st.markdown('''<p style='text-align: center; color: #000000;'>Optional description for section.
</p>''', unsafe_allow_html=True)
st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Top Species Plot By Biome Plotly</h4>''', unsafe_allow_html=True)

with open('example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/1_top_species_plot_by_biome_plotly.json', 'r') as plot_file:
    plot_json = json.load(plot_file)
st.plotly_chart(plot_json, use_container_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Multiline Plot Altair</h4>''', unsafe_allow_html=True)

with open('example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/2_multiline_plot_altair.json', 'r') as plot_file:
    plot_json = json.load(plot_file)

altair_plot = alt.Chart.from_dict(plot_json)
st.vega_lite_chart(json.loads(altair_plot.to_json()), use_container_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Pie Plot Countries Plotly</h4>''', unsafe_allow_html=True)

with open('example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/3_pie_plot_countries_plotly.json', 'r') as plot_file:
    plot_json = json.load(plot_file)
st.plotly_chart(plot_json, use_container_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Pie Plots Biomes Plotly</h4>''', unsafe_allow_html=True)

with open('example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/4_pie_plots_biomes_plotly.json', 'r') as plot_file:
    plot_json = json.load(plot_file)
st.plotly_chart(plot_json, use_container_width=True)

st.markdown('''<h4 style='text-align: center; color: #2b8cbe;'>Saline Metagenomics Samples Map Altair</h4>''', unsafe_allow_html=True)

with open('example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/5_saline_metagenomics_samples_map_altair.json', 'r') as plot_file:
    plot_json = json.load(plot_file)

altair_plot = alt.Chart.from_dict(plot_json)
st.vega_lite_chart(json.loads(altair_plot.to_json()), use_container_width=True)

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
