## About the project

**VueGen** is a tool that automates the creation of **reports** from bioinformatics outputs, allowing researchers with minimal coding experience to communicate their results effectively. With VueGen, users can produce reports by simply specifying a directory containing output files, such as plots, tables, networks, Markdown text, HTML components, and API calls, along with the report format. Supported formats include **documents** (PDF, HTML, DOCX, ODT), **presentations** (PPTX, Reveal.js), **Jupyter notebooks**, and [Streamlit](https://streamlit.io/) **web applications**.

A YAML configuration file is generated from the directory to define the structure of the report. Users can customize the report by modifying the configuration file, or they can create their own configuration file instead of passing a directory as input. The configuration file specifies the structure of the report, including sections, subsections, and various components such as plots, dataframes, markdown, html, and API calls.

An overview of the VueGen workflow is shown in the figure below:

![VueGen Abstract](https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_graph_abstract.png)

Also, the class diagram for the project is presented below to illustrate the architecture and relationships between classes:

![VueGen Class Diagram](https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_classdiagram_noattmeth.png)

An extended version of the class diagram with attributes and methods is available [here](https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_classdiagram_withattmeth.pdf).

The VueGen documentation is available at [vuegen.readthedocs.io](https://vuegen.readthedocs.io/), where you can find detailed information of the package’s classes and functions, installation and execution instructions, and case studies to demonstrate its functionality.