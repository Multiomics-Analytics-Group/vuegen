<!-- https://myst-parser.readthedocs.io/en/latest/faq/index.html
#include-a-file-from-outside-the-docs-folder-like-readme-md -->

```{include} ./sections_readme/home_page.md
:caption: VueGen
:relative-docs: docs
:relative-images:
```

```{toctree} 
:maxdepth: 1
:caption: Overview

sections_readme/about
sections_readme/installation
sections_readme/execution
sections_readme/gui
sections_readme/case_studies
sections_readme/web_app_deploy
sections_readme/citation
```

```{toctree}
:maxdepth: 1
:caption: Building a report

vuegen_basic_case_study
vuegen_basic_case_study_configfile
vuegen_case_study_earth_microbiome
vuegen_case_study_earth_microbiome_configfile
example_report
vuegen_APICall_configfile
vuegen_Chatbot_configfile
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

sections_readme/contributing
sections_readme/credits
sections_readme/contact
```

```{toctree}
:maxdepth: 1
:caption: Extra Materials
:hidden:

README.md
```
