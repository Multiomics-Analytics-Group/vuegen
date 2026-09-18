<!-- https://myst-parser.readthedocs.io/en/latest/faq/index.html
#include-a-file-from-outside-the-docs-folder-like-readme-md -->

```{include} ./sections_readme/home_page.md
:caption: VueGen
:relative-docs: docs
:relative-images:
```

Install using pip (details at [installation](sections_readme/installation.md)):

```bash
$ pip install vuegen
```

and then run the command line interface (CLI) to see the available options:

```bash
$ vuegen --help
usage: VueGen [-h] [-v] [-c CONFIG] [-d DIRECTORY] [-r REPORT_TYPE] [-o OUTPUT_DIRECTORY] [-s] [-q] [-m MAX_DEPTH] [-eft EXT [EXT ...]]

options:
  -h, --help            show this help message and exit
  -v, --version         show version number and exit
  -c, --config CONFIG   Path to the YAML configuration file.
  -d, --directory DIRECTORY
                        Path to the directory from which the YAML config will be inferred.
  -r, --report-type REPORT_TYPE
                        Type of the report to generate: streamlit, html, pdf, docx, odt, revealjs, pptx, or jupyter.
  -o, --output-directory OUTPUT_DIRECTORY
                        Path to the output directory for the generated report.
  -s, --streamlit-autorun
                        Automatically run the Streamlit app after report generation.
  -q, --quarto-checks   Check if Quarto is installed and available for report generation.
  -m, --max-depth MAX_DEPTH
                        Maximum depth for the recursive search of files in the input directory. Ignored if a config file is provided.
  -eft, --exclude_file_types EXT [EXT ...]
                        One or more file extensions to exclude when scanning the input directory (e.g. csv png or .csv .png). When files with the same name exist in multiple formats, the excluded types are dropped first; remaining duplicates are resolved
                        automatically by preferring interactive/richer formats over plain-text or static ones. Ignored if a config file is provided.
```

The easiest way is to start with a directory for which you want to create a report.

```{include} ./sections_readme/folder_structure.md
:caption: Folder Structure
:relative-docs: docs
:relative-images:
```

```{toctree}
:maxdepth: 1
:caption: Overview
:hidden:

sections_readme/about
sections_readme/installation
sections_readme/example_earch_microbiome
sections_readme/gui
sections_readme/container_execution
sections_readme/case_studies
sections_readme/web_app_deploy
sections_readme/citation
sections_readme/faq
```

```{toctree}
:maxdepth: 1
:caption: Building a report
:hidden:

vuegen_basic_case_study
vuegen_basic_case_study_configfile
vuegen_earth_microbiome_case_study
vuegen_earth_microbiome_case_study_configfile
example_report
vuegen_apicall_case_study
vuegen_apicall_case_study_configfile
vuegen_chatbot_case_study
vuegen_chatbot_case_study_configfile
```

```{toctree}
:maxdepth: 2
:caption: API Reference
:hidden:

reference/vuegen
```

```{toctree}
:maxdepth: 1
:caption: Project Support
:hidden:

sections_readme/contributing
sections_readme/credits
sections_readme/contact
sections_readme/changelog
```

```{toctree}
:maxdepth: 1
:caption: Extra Materials
:hidden:

README.md
```
