# Overview

<!-- https://myst-parser.readthedocs.io/en/latest/faq/index.html
#include-a-file-from-outside-the-docs-folder-like-readme-md -->

```{include} ../README.md
:start-line: 0
:relative-docs: docs
:relative-images:
```

```{toctree}
:maxdepth: 2

vuegen_demo
```

```{toctree}
:maxdepth: 1
:caption: Building a report

vuegen_basic_case_study
vuegen_case_study_earth_microbiome
example_report
```

```{toctree}
:maxdepth: 2
:caption: Modules
:hidden:

reference/vuegen
```

```{toctree}
:maxdepth: 1
:caption: MISC:
:hidden:

README.md
```
