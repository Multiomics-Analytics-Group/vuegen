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

We use `sphinx-apidoc` to create the API reference files from the source code and 
`sphinx-build` to create the html files. Also, we use a custom script `split_readme.py` to
split the main `README.md` file into smaller sections for inclusion in the docs.

We provide a [Makefile](https://github.com/Multiomics-Analytics-Group/vuegen/blob/HEAD/docs/Makefile) 
to simplify the cleaning and building process, which you can run from the `docs` folder:

```bash
# pwd: docs
make clean
make build
```

Alternatevely, you can run these commands manually each at a time, as follows:

```bash
# pwd: docs
sphinx-apidoc --force --implicit-namespaces --module-first -o reference ../src/vuegen
python split_readme.py
sphinx-build -n -W --keep-going -b html ./ ./_build/
```

## Include repo README into docs

The README is included in the `Overview` section of the docs. We created a 
[Python script](https://github.com/Multiomics-Analytics-Group/vuegen/blob/split-readme-docs/docs/split_readme.py) to 
split the README sections into separate md files, stored in `docs/sections_readme`. The `index.md` file contains 
the structure of the docs with the generated sections and additional information.

Relative links are used in the main README, which need to be resolved when building. It's
possible to include the a `relative-docs` option if one uses `index.md` ([see docs](https://myst-parser.readthedocs.io/en/latest/faq/index.html#include-a-file-from-outside-the-docs-folder-like-readme-md)). This does not work
with `href` links, only native markdown links.
