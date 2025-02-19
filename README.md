![VueGen Logo](https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_logo.svg)
-----------------
<p align="center">
   VueGen is a Python package that automates the creation of scientific reports.
</p>

| Information | Links |
| :--- | :--- |
| **Package** |[ ![PyPI Latest Release](https://img.shields.io/pypi/v/vuegen.svg)][vuegen-pypi] [![Supported versions](https://img.shields.io/pypi/pyversions/vuegen.svg)][vuegen-pypi]|
| **Documentation** | [![Docs](https://readthedocs.org/projects/vuegen/badge/?style=flat)][vuegen-docs]|
| **Build** | [![CI](https://github.com/Multiomics-Analytics-Group/vuegen/actions/workflows/cdci.yml/badge.svg)][ci-gh-action] [![Docs](https://github.com/Multiomics-Analytics-Group/vuegen/actions/workflows/docs.yml/badge.svg)][ci-docs]|
| **Examples** | [![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)][emp-html-demo] [![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)][emp-st-demo]|
| **Discuss on GitHub** | [![GitHub issues](https://img.shields.io/github/issues/Multiomics-Analytics-Group/vuegen)][issues] [![GitHub pull requests](https://img.shields.io/github/issues-pr/Multiomics-Analytics-Group/vuegen)][pulls]|

## Table of contents:
- [About the project](#about-the-project)
- [Installation](#installation)
- [Execution](#execution)
- [Case studies](#case-studies)
- [Web application deployment](#web-application-deployment)
- [Credits and acknowledgements](#credits-and-acknowledgements)
- [Contact](#contact)

## About the project
VueGen automates the creation of reports based on a directory with plots, dataframes, and other files in different formats. A YAML configuration file is generated from the directory to define the structure of the report. Users can customize the report by modifying the configuration file, or they can create their own configuration file instead of passing a directory as input. 

The configuration file specifies the structure of the report, including sections, subsections, and various components such as plots, dataframes, markdown, html, and API calls. Reports can be generated in various formats, including documents (PDF, HTML, DOCX, ODT), presentations (PPTX, Reveal.js), notebooks (Jupyter) or [Streamlit](streamlit) web applications.

An overview of the VueGen workflow is shown in the figure below:

![VueGen Abstract](https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_graph_abstract.png)

Also, the class diagram for the project is presented below to illustrate the architecture and relationships between classes:

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

> [!TIP]
> It is recommended to install VueGen inside a virtual environment to manage depenendencies and avoid conflicts with existing packages. You can use the virtual environment manager of your choice, such as `poetry`, `conda`, or `pipenv`.

### Quarto installation
Vuegen uses [Quarto][quarto] to generate various report types. The pip insallation includes quarto using the [quarto-cli Python library][quarto-cli-pypi]. To test if quarto is installed in your computer, run the following command:

```bash
quarto check
```

> [!TIP]
> If quarto is not installed, you can download the command-line interface from the [Quarto website][quarto-cli] for your operating system.

## Execution
Run VueGen using a directory with the following command:

```bash
vuegen --directory example_data/Earth_microbiome_vuegen_demo_notebook --report_type streamlit
```

> [!NOTE]
> By default, the `streamlit_autorun` argument is set to False, but you can use it in case you want to automatically run the streamlit app.

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

## Case studies
VueGen’s functionality is demonstrated through two case studies:

**1. Predefined Directory**

This introductory case study uses a predefined directory with plots, dataframes, Markdown, and HTML components. Users can generate reports in different formats and modify the configuration file to customize the report structure. 

🔗 [![Open in Colab][colab_badge]][colab_link_intro_demo]

**2. Earth Microbiome Project Data**

This advanced case study demonstrates the application of VueGen in a real-world scenario using data from the [Earth Microbiome Project (EMP)][emp]. The EMP is an initiative to characterize global microbial taxonomic and functional diversity. The notebook process the EMP data, create plots, dataframes, and other components, and organize outputs within a directory to produce reports. Report content and structure can be adapted by modifying the configuration file. Each report consists of sections on exploratory data analysis, metagenomics, and network analysis.

🔗 [![Open in Colab][colab_badge]][colab_link_emp_demo]

> [!NOTE]
> An HTML report example of the current vuegen release is available [here][emp-html-demo].

## Web application deployment
Once a Streamlit report is generated, it can be deployed as a web application to make it accessible online. There are multiple ways to achieve this:

* **Streamlit Community Cloud**: Deploy your report easily using [Streamlit Cloud][st-cloud], as demonstrated in the [EMP VueGen Demo][emp-st-demo]. The process involves moving the necessary scripts, data, and a requirements.txt file into a GitHub repository. Then, the app can be deployed via the Streamlit Cloud interface. The deployment example is available in the `streamlit-report-example` branch.
* **Standalone Executables**: Convert your Streamlit application into a desktop app by packaging it as an executable file for different operating systems. A detailed explanation of this process can be found in this [Streamlit forum post][st-forum-exe].
* [Stlite][stlite]: Run Streamlit apps directly in the browser with stlite, a WebAssembly port of Streamlit powered by Pyodide, eliminating the need for a server. It also allows packaging apps as standalone desktop executables using stlite desktop.

These options provide flexibility depending on whether the goal is online accessibility, lightweight execution, or local application distribution.

## Credits and acknowledgements
- Vuegen was developed by the [Multiomics Network Analytics Group (MoNA)][Mona] at the [Novo Nordisk Foundation Center for Biosustainability (DTU Biosustain)][Biosustain].
- The vuegen logo was designed based on an image created by [Scriberia][scriberia] for The [Turing Way Community][turingway], which is shared under a CC-BY licence. The original image can be found at [Zenodo][zenodo-turingway].

## Contact
If you have comments or suggestions about this project, you can [open an issue][issues] in this repository.

[streamlit]: https://streamlit.io/ 
[vuegen-pypi]: https://pypi.org/project/vuegen/
[vuegen-docs]: https://vuegen.readthedocs.io/
[ci-gh-action]: https://github.com/Multiomics-Analytics-Group/vuegen/actions/workflows/cdci.yml
[ci-docs]: https://github.com/Multiomics-Analytics-Group/vuegen/actions/workflows/docs.yml
[emp-html-demo]: https://multiomics-analytics-group.github.io/vuegen/
[emp-st-demo]: https://earth-microbiome-vuegen-demo.streamlit.app/
[issues]: https://github.com/Multiomics-Analytics-Group/vuegen/issues
[pulls]: https://github.com/Multiomics-Analytics-Group/vuegen/pulls
[quarto]: https://quarto.org/
[quarto-cli-pypi]: https://pypi.org/project/quarto-cli/
[quarto-cli]: https://quarto.org/docs/get-started/
[colab_badge]: https://colab.research.google.com/assets/colab-badge.svg
[colab_link_intro_demo]: https://colab.research.google.com/github/Multiomics-Analytics-Group/vuegen/blob/main/docs/vuegen_basic_case_study.ipynb
[colab_link_emp_demo]: https://colab.research.google.com/github/Multiomics-Analytics-Group/vuegen/blob/main/docs/vuegen_case_study_earth_microbiome.ipynb
[emp]: https://earthmicrobiome.org/
[st-cloud]: https://streamlit.io/cloud
[stlite]: https://github.com/whitphx/stlite
[st-forum-exe]: https://discuss.streamlit.io/t/streamlit-deployment-as-an-executable-file-exe-for-windows-macos-and-android/6812
[Mona]: https://multiomics-analytics-group.github.io/
[Biosustain]: https://www.biosustain.dtu.dk/
[scriberia]: https://www.scriberia.co.uk/
[turingway]: https://github.com/the-turing-way/the-turing-way
[zenodo-turingway]: https://zenodo.org/records/3695300
[new-issue]: https://github.com/Multiomics-Analytics-Group/vuegen/issues/new


