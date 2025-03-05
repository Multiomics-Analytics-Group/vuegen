# VueGen GUI

## Local execution of the GUI

Install required dependencies from package

```bash
pip install 'vuegen[gui]'
# or with local repo
pip install '.[gui]'
# or for local editable install
pip install -e '.[gui]'
```

Can be started locally with

```bash
# from within gui directory
python app.py
```

## Build executable GUI

For now do not add the `--windowed` option, as it will not show the console output,
which is useful for debugging and especially terminating any running processes, e.g.
as the streamlit server and the GUI itself.

```bash
# from this README folder
pyinstaller \
-n vuegen_gui \
--noconfirm \
--onedir \
--collect-all pyvis \
--collect-all streamlit \
--collect-all  st_aggrid  \
--collect-all customtkinter \
--add-data ../docs/example_data/Basic_example_vuegen_demo_notebook:example_data/Basic_example_vuegen_demo_notebook \
app.py
```

- pyvis templates were not copied, so make these explicit (see [this](https://stackoverflow.com/a/72687433/9684872))
- same for streamlit, customtkinter and st_aggrid
- might be copying too much, but for now we go the safe route

## relevant Pyinstaller options

```bash
What to generate:
  -D, --onedir          Create a one-folder bundle containing an executable (default)
  -F, --onefile         Create a one-file bundled executable.
  --specpath DIR        Folder to store the generated spec file (default: current directory)
  -n NAME, --name NAME  Name to assign to the bundled app and spec file (default: first script's basename)
Windows and macOS specific options:
  -c, --console, --nowindowed
                        Open a console window for standard i/o (default). On Windows this option has no effect if the first script is a
                        '.pyw' file.
  -w, --windowed, --noconsole
                        Windows and macOS: do not provide a console window for standard i/o. On macOS this also triggers building a
                        macOS .app bundle. On Windows this option is automatically set if the first script is a '.pyw' file. This option
                        is ignored on *NIX systems.
```

## Quarto notebook execution

- add python exe to bundle as suggested [on stackoverflow](https://stackoverflow.com/a/72639099/9684872)
- use [copy_python_executable.py](copy_python_executable.py) to copy the python executable to the bundle after PyInstaller is done

Basic workflow for bundle:

1. use quarto (pandoc?) to convert qmd to ipynb
1. use nbconvert and a copied Python executable to execute notebook
1. use quarto (pandoc?) ot convert executed ipynb to desired format
