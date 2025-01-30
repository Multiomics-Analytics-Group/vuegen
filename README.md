<!-- <div align="center">
  <img width="300px" src="images/vuegen_logo.svg">
</div> -->
![VueGen Logo](docs/images/vuegen_logo.svg)
-----------------
<p align="center">
   VueGen is a Python library that automates the creation of scientific reports.
</p>

## Table of contents:
- [About the project](#about-the-project)
- [Installation](#installation)
- [Execution](#execution)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## About the project
VueGen automates the creation of reports based on a directory with plots, dataframes, and other files in different formats. A YAML configuration file is generated from the directory to define the structure of the report. Users can customize the report by modifying the configuration file, or they can create their own configuration file instead of passing a directory as input. 

The configuration file specifies the structure of the report, including sections, subsections, and various components such as plots, dataframes, markdown, html, and API calls. Reports can be generated in various formats, including documents (PDF, HTML, DOCX, ODT), presentations (PPTX, Reveal.js), notebooks (Jupyter) or [Streamlit](streamlit) web applications.

An overview of the VueGen workflow is shown in the figure below:

<!-- <p align="center">
<figure>
  <img width="650px" src="images/vuegen_graph_abstract.png" alt="VueGen overview"/>
</figure>
</p> -->
![VueGen Abstract](docs/images/vuegen_graph_abstract.png)

Also, the class diagram for the project is presented below to illustrate the architecture and relationships between classes:

<!-- <p align="center">
<figure>
  <img width="650px" src="images/vuegen_classdiagram_noattmeth.png" alt="VueGen class diagram"/>
</figure>
</p> -->

![VueGen Class Diagram](docs/images/vuegen_classdiagram_noattmeth.png)

## Installation

You can install the package for development from this repository by running the following command:

```bash
pip install -e path/to/vuegen # specify location 
pip install -e . # in case your pwd is in the vuegen directory
```

This will both install `quarto` and `streamlit` as our backends for report generation.

### Verify quarto installation

Test your quarto installation by running the following command:

```bash
quarto check
```

If you use conda a conda environement you can install quatro from the conda-forge channel 
in case it did not work.

```bash
conda install -c conda-forge quarto
```

## Execution

Run VueGen using a directory with the following command:

```bash
cd docs
vuegen --directory example_data/Earth_microbiome_vuegen_demo_notebook --report_type streamlit
```

> 💡 If `vuegen` does not work, try `python -m vuegen` instead.

By default, the `streamlit_autorun` argument is set to False, but you can use it in case you want to automatically run the streamlit app.

It's also possible to provide a configuration file instead of a directory:

```bash
vuegen --config example_data/Earth_microbiome_vuegen_demo_notebook/Earth_microbiome_vuegen_demo_notebook_config.yaml --report_type streamlit
```

The current report types are streamlit, html, pdf, docx, odt, revealjs, pptx, and jupyter.

## Acknowledgements

- Vuegen was developed by the [Multiomics Network Analytics Group (MoNA)][Mona] at the [Novo Nordisk Foundation Center for Biosustainability (DTU Biosustain)][Biosustain].
- The vuegen logo was designed based on an image created by [Scriberia][scriberia] for The [Turing Way Community][turingway], which is shared under a CC-BY licence. The original image can be found at [Zenodo][zenodo-turingway].

## Contact
If you have comments or suggestions about this project, you can [open an issue][issues] in this repository.

[issues]: https://github.com/Multiomics-Analytics-Group/vuegen/issues/new
[streamlit]: https://streamlit.io/ 
[Mona]: https://multiomics-analytics-group.github.io/
[Biosustain]: https://www.biosustain.dtu.dk/
[scriberia]: https://www.scriberia.co.uk/
[turingway]: https://github.com/the-turing-way/the-turing-way
[zenodo-turingway]: https://zenodo.org/records/3695300


