# Predefined Directory Case Study - Configuration File

The [configuration file](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/docs/example_config_files/Basic_example_vuegen_demo_notebook_config.yaml) of the basic case study using a predefined directory is presented below: 

```yaml
report:
  title: Basic Example Vuegen Demo Notebook
  description: A general description of the report.
  graphical_abstract: https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_logo.svg
  logo: https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_logo.svg
sections:
- title: Plots
  description: This section contains example plots.
  subsections:
  - title: Interactive Plots
    description: Optional description for section.
    components:
    - title: Top Species Plot By Biome Plotly
      file_path: example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/1_top_species_plot_by_biome_plotly.json
      description: ''
      caption: ''
      component_type: plot
      plot_type: plotly
    - title: Multiline Plot Altair
      file_path: example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/2_multiline_plot_altair.json
      description: ''
      caption: ''
      component_type: plot
      plot_type: altair
    - title: Pie Plot Countries Plotly
      file_path: example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/3_pie_plot_countries_plotly.json
      description: ''
      caption: ''
      component_type: plot
      plot_type: plotly
    - title: Pie Plots Biomes Plotly
      file_path: example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/4_pie_plots_biomes_plotly.json
      description: ''
      caption: ''
      component_type: plot
      plot_type: plotly
    - title: Saline Metagenomics Samples Map Altair
      file_path: example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/5_saline_metagenomics_samples_map_altair.json
      description: ''
      caption: ''
      component_type: plot
      plot_type: altair
    - title: Description
      file_path: example_data/Basic_example_vuegen_demo_notebook/1_Plots/1_Interactive_plots/description.md
      description: ''
      caption: ''
      component_type: markdown
  - title: Static Plots
    description: ''
    components:
    - title: Number Samples Per Study
      file_path: example_data/Basic_example_vuegen_demo_notebook/1_Plots/2_Static_plots/1_number_samples_per_study.png
      description: ''
      caption: ''
      component_type: plot
      plot_type: static
    - title: Animal Metagenomics Samples Map
      file_path: example_data/Basic_example_vuegen_demo_notebook/1_Plots/2_Static_plots/2_animal_metagenomics_samples_map.png
      description: ''
      caption: ''
      component_type: plot
      plot_type: static
    - title: Alpha Diversity Host Associated Samples
      file_path: example_data/Basic_example_vuegen_demo_notebook/1_Plots/2_Static_plots/3_alpha_diversity_host_associated_samples.png
      description: ''
      caption: ''
      component_type: plot
      plot_type: static
    - title: "Graphical overview of VueGen workflow and components"
      file_path: https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_graph_abstract.png
      description: ''
      caption: The diagram illustrates the processing pipeline of VueGen, starting
        from either a directory or a YAML configuration file. Reports consist of hierarchical
        sections and subsections, each containing various components such as plots,
        dataframes, Markdown, HTML, and data retrieved via API calls.
      component_type: plot
      plot_type: static
- title: Dataframes
  description: ''
  subsections:
  - title: All Formats
    description: This subsection contains example dataframes.
    components:
    - title: Phyla Correlation Network Csv
      file_path: example_data/Basic_example_vuegen_demo_notebook/2_Dataframes/1_All_formats/1_phyla_correlation_network_csv.csv
      description: ''
      caption: ''
      component_type: dataframe
      file_format: csv
      delimiter: ','
    - title: Abundance Table Example Xls
      file_path: example_data/Basic_example_vuegen_demo_notebook/2_Dataframes/1_All_formats/2_abundance_table_example_xls.xls
      description: ''
      caption: ''
      component_type: dataframe
      file_format: xls
    - title: Sample Info Example Txt
      file_path: example_data/Basic_example_vuegen_demo_notebook/2_Dataframes/1_All_formats/3_sample_info_example_txt.txt
      description: ''
      caption: ''
      component_type: dataframe
      file_format: txt
      delimiter: \t
    - title: Sample Info Example Parquet
      file_path: example_data/Basic_example_vuegen_demo_notebook/2_Dataframes/1_All_formats/4_sample_info_example_parquet.parquet
      description: ''
      caption: ''
      component_type: dataframe
      file_format: parquet
- title: Networks
  description: ''
  subsections:
  - title: Interactive Networks
    description: Optional description for subsection
    components:
    - title: Man Example
      file_path: example_data/Basic_example_vuegen_demo_notebook/3_Networks/1_Interactive_networks/1_man_example.graphml
      description: ''
      caption: ''
      component_type: plot
      plot_type: interactive_network
    - title: Description
      file_path: example_data/Basic_example_vuegen_demo_notebook/3_Networks/1_Interactive_networks/description.md
      description: ''
      caption: ''
      component_type: markdown
  - title: Static Networks
    description: ''
    components:
    - title: Phyla Correlation Network
      file_path: example_data/Basic_example_vuegen_demo_notebook/3_Networks/2_Static_networks/1_phyla_correlation_network.png
      description: ''
      caption: ''
      component_type: plot
      plot_type: static
- title: Html
  description: ''
  subsections:
  - title: All Html
    description: ''
    components:
    - title: Plot
      file_path: example_data/Basic_example_vuegen_demo_notebook/4_Html/1_All_html/1_plot.html
      description: ''
      caption: ''
      component_type: html
    - title: Ckg Network
      file_path: example_data/Basic_example_vuegen_demo_notebook/4_Html/1_All_html/2_ckg_network.html
      description: ''
      caption: ''
      component_type: plot
      plot_type: interactive_network
    - title: Multiqc Report
      file_path: example_data/Basic_example_vuegen_demo_notebook/4_Html/1_All_html/3_multiqc_report.html
      description: ''
      caption: ''
      component_type: html
- title: Markdown
  description: ''
  subsections:
  - title: All Markdown
    description: ''
    components:
    - title: Readme
      file_path: example_data/Basic_example_vuegen_demo_notebook/5_Markdown/1_All_markdown/README.md
      description: ''
      caption: ''
      component_type: markdown
```

The directory with he example data is available in the [GitHub repository](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/docs/example_data/Basic_example_vuegen_demo_notebook).
