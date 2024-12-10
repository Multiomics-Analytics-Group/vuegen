<div align="center">
  <img width="300px" src="docs/images/vuegen_logo.svg">
</div>

-----------------

<p align="center">
   VueGen is a Python library that automates the creation of scientific reports.
</p>

## Table of contents:
- [About the project](#about-the-project)
- [Installation](#installation)
- [Execution](#execution)
- [Contact](#contact)

## About the project
VueGen automates the creation of scientific reports based on a YAML configuration file.  This configuration file specifies the structure of the report, including sections, subsections, and various components such as plots, dataframes, markdown, and API calls. Reports can be generated in various formats, including documents (PDF, HTML, DOCX, ODT), presentations (PPTX, Reveal.js), notebooks (Jupyter) or [Streamlit](streamlit) web applications.

An overview of the VueGen workflow is shown in the figure below:

<p align="center">
<figure>
  <img width="650px" src="docs/images/vuegen_graph_abstract.png" alt="VueGen overview"/>
</figure>
</p>

Also, the class diagram for the project is presented below to illustrate the architecture and relationships between classes:

<p align="center">
<figure>
  <img width="650px" src="docs/images/vuegen_classdiagram_noattmeth.png" alt="VueGen class diagram"/>
</figure>
</p>

## Installation

You can install the package for development from this repository by running the following command:

```bash
pip install -e path/to/vuegen # specify location 
pip install -e . # in case you pwd is in the vuegen directory
```

## Execution

```bash
python vuegen/main.py --config report_config_micw2graph.yaml --report_type streamlit 
```

The current report types are streamlit, html, pdf, docx, odt, revealjs, pptx, and jupyter.

## Contact
If you have comments or suggestions about this project, you can [open an issue][issues] in this repository.

[issues]: https://github.com/Multiomics-Analytics-Group/vuegen/issues/new
[streamlit]: https://streamlit.io/ 
