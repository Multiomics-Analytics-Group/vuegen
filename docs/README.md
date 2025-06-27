# Docs creation

In order to build the docs you need to

1. Install sphinx and additional support packages
2. Build the package reference files
3. Run sphinx to create a local html version

The documentation is build using readthedocs automatically.

Install the docs dependencies of the package (as speciefied in toml):

```bash
# in main folder
# pip install ".[docs]"
poetry install --with docs
```

## Build docs using Sphinx command line tools

Command to be run from `path/to/docs`, i.e. from within the `docs` package folder:

Options:

- `--separate` to build separate pages for each (sub-)module

```bash
# pwd: docs
# apidoc
sphinx-apidoc --force --implicit-namespaces --module-first -o reference ../src/vuegen
# build docs
sphinx-build -n -W --keep-going -b html ./ ./_build/
```

## Include repo README into docs

The README is included in the `Overview` section of the docs. We created a [Python script](https://github.com/Multiomics-Analytics-Group/vuegen/blob/split-readme-docs/docs/split_readme.py) to split the README sections into separate md files, stored in `docs/sections_readme`. The `index.md` file contains the structure of the docs with the generated sections and additional information.

Relative links are used in the main README, which need to be resolved when building. It's
possible to include the a `relative-docs` option if one uses `index.md` ([see docs](https://myst-parser.readthedocs.io/en/latest/faq/index.html#include-a-file-from-outside-the-docs-folder-like-readme-md)). This does not work
with `href` links, only native markdown links.
