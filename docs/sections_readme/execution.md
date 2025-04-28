## Execution


:::{IMPORTANT}
Here we use the `Earth_microbiome_vuegen_demo_notebook` [directory](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/docs/example_data/Earth_microbiome_vuegen_demo_notebook) and the `Earth_microbiome_vuegen_demo_notebook.yaml` [configuration file](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/docs/example_config_files/Earth_microbiome_vuegen_demo_notebook_config) as examples, which are available in the `docs/example_data` and `docs/example_config_files` folders, respectively. Make sure to clone this reposiotry to access these contents, or use your own directory and configuration file.
:::


Run VueGen using a directory with the following command:

```bash
vuegen --directory docs/example_data/Earth_microbiome_vuegen_demo_notebook --report_type streamlit
```

:::{NOTE}
By default, the `streamlit_autorun` argument is set to False, but you can use it in case you want to automatically run the streamlit app.
:::


### Folder structure

Your input directory must follow a **nested folder structure**, where first-level folders are treated as **sections** and second-level folders as **subsections**, containing the components (plots, tables, networks, Markdown text, and HTML files).

Here is an example layout:
```
report_folder/
├── section1/
│   └── subsection1/
│       ├── table.csv
│       ├── image1.png
│       └── chart.json
├── section2/
│   ├── subsection1/
│   │   ├── summary_table.xls
│   │   └── network_plot.graphml
│   └── subsection2/
│       ├── report.html
│       └── summary.md
```

:::{WARNING}
VueGen currently requires each section to contain at least one subsection folder. Defining only sections (with no subsections) or using deeper nesting levels (i.e., sub-subsections) will result in errors. In upcoming releases, we plan to support more flexible directory structures.
:::


The titles for sections, subsections, and components are extracted from the corresponding folder and file names, and afterward, users can add descriptions, captions, and other details to the configuration file. Component types are inferred from the file extensions and names. 
The order of sections, subsections, and components can be defined using numerical suffixes in folder and file names.

It's also possible to provide a configuration file instead of a directory:

```bash
vuegen --config docs/example_config_files/Earth_microbiome_vuegen_demo_notebook.yaml --report_type streamlit
```

If a configuration file is given, users can specify titles and descriptions for sections and subsections, as well as component paths and required attributes, such as file format and delimiter for dataframes, plot types, and other details.

The current report types supported by VueGen are:

- Streamlit
- HTML
- PDF
- DOCX
- ODT
- Reveal.js
- PPTX
- Jupyter

### Running VueGen with Docker

Instead of installing VueGen locally, you can run it directly from a Docker container with the following command:

```bash
docker run --rm \
  -v "$(pwd)/docs/example_data/Earth_microbiome_vuegen_demo_notebook:/home/appuser/Earth_microbiome_vuegen_demo_notebook" \
  -v "$(pwd)/output_docker:/home/appuser/streamlit_report" \
  quay.io/dtu_biosustain_dsp/vuegen:v0.3.2-docker --directory /home/appuser/Earth_microbiome_vuegen_demo_notebook --report_type streamlit
```