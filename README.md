<!-- <div align="center">
  <img width="300px" src="images/vuegen_logo.svg">
</div> -->
![VueGen Logo](https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_logo.svg)
-----------------
<p align="center">
   VueGen is a Python library that automates the creation of scientific reports.
</p>

| Information | Links |
| :--- | :--- |
| **Package** |[ ![PyPI Latest Release](https://img.shields.io/pypi/v/vuegen.svg)](https://pypi.org/project/vuegen/) [![Supported versions](https://img.shields.io/pypi/pyversions/vuegen.svg)](https://pypi.org/project/vuegen/)|
| **Documentation** | [![Docs](https://readthedocs.org/projects/vuegen/badge/?style=flat)](https://vuegen.readthedocs.io/)|
| **Build** | [![CI](https://github.com/Multiomics-Analytics-Group/vuegen/actions/workflows/cdci.yml/badge.svg)](https://github.com/Multiomics-Analytics-Group/vuegen/actions/workflows/cdci.yml) [![Docs](https://github.com/Multiomics-Analytics-Group/vuegen/actions/workflows/docs.yml/badge.svg)](https://github.com/Multiomics-Analytics-Group/vuegen/actions/workflows/docs.yml)|
| **Examples** | [![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://multiomics-analytics-group.github.io/vuegen/) [![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://multiomics-analytics-group.github.io/vuegen/)|
| **Discuss on GitHub** | [![GitHub issues](https://img.shields.io/github/issues/Multiomics-Analytics-Group/vuegen)](https://github.com/Multiomics-Analytics-Group/vuegen/issues) [![GitHub pull requests](https://img.shields.io/github/issues-pr/Multiomics-Analytics-Group/vuegen)](https://github.com/Multiomics-Analytics-Group/vuegen/pulls) |

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
![VueGen Abstract](https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_graph_abstract.png)

Also, the class diagram for the project is presented below to illustrate the architecture and relationships between classes:

<!-- <p align="center">
<figure>
  <img width="650px" src="images/vuegen_classdiagram_noattmeth.png" alt="VueGen class diagram"/>
</figure>
</p> -->

![VueGen Class Diagram](https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_classdiagram_noattmeth.png)

## Installation

Vuegen is available on [PyPI][vuegen-pypi] and can be installed using pip:

```bash
pip install vuegen
```

You can also install the package for development from this repository by running the following command:

```bash
pip install -e path/to/vuegen # specify location 
pip install -e . # in case your pwd is in the vuegen directory
```

### Quarto installation

Vuegen uses [Quarto][quarto] to generate various report types. The pip insallation includes quarto using the [quarto-cli Python library][quarto-cli-pypi]. To test if quarto is installed in your computer, run the following command:

```bash
quarto check
```

If quarto is not installed, you can download the command-line interface from the [Quarto website][quarto-cli] for your operating system.

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

The current report types supported by VueGen are:
* Streamlit
* HTML
* PDF
* DOCX
* ODT
* Reveal.js
* PPTX
* Jupyter

## Acknowledgements

- Vuegen was developed by the [Multiomics Network Analytics Group (MoNA)][Mona] at the [Novo Nordisk Foundation Center for Biosustainability (DTU Biosustain)][Biosustain].
- The vuegen logo was designed based on an image created by [Scriberia][scriberia] for The [Turing Way Community][turingway], which is shared under a CC-BY licence. The original image can be found at [Zenodo][zenodo-turingway].

## Contact
If you have comments or suggestions about this project, you can [open an issue][issues] in this repository.

[streamlit]: https://streamlit.io/ 
[vuegen-pypi]: https://pypi.org/project/vuegen/
[quarto]: https://quarto.org/
[quarto-cli-pypi]: https://pypi.org/project/quarto-cli/
[quarto-cli]: https://quarto.org/docs/get-started/
[Mona]: https://multiomics-analytics-group.github.io/
[Biosustain]: https://www.biosustain.dtu.dk/
[scriberia]: https://www.scriberia.co.uk/
[turingway]: https://github.com/the-turing-way/the-turing-way
[zenodo-turingway]: https://zenodo.org/records/3695300
[issues]: https://github.com/Multiomics-Analytics-Group/vuegen/issues/new


