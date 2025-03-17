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

- add python exe to bundle as suggested [on stackoverflow](https://stackoverflow.com/a/72639099/9684872) [not this way at least]

## test shipping a python virtual environment with vuegen installed

## Bundled PyInstaller execution (current status)

1. Can be executed. Streamlit apps can be run (although sometimes not easily terminated)
2. All quarto based reports need to specify a path to a python environment where python 3.12
   is installed along `jupyter`
   - This could be partly replace by a full anaconda distribution on the system.
   - maybe a self-contained minimal virtual environment for kernel starting can be added later
   - we could add some logic to make sure a correct path is added.

## Using bundle vuegen release

## On Windows

- global quarto and python installations can be used
- quarto can be shipped with app, but maybe it can be deactivated

## On MacOs

- on MacOs the default paths are not set

#### Create environment using conda

```bash
conda create -n vuegen_gui -c conda-forge python=3.12 jupyter
conda info -e # find environment location
```

This might for example display the following path for the `vuegen_gui` environment:

```
/Users/user/miniforge3/envs/vuegen_gui
```

In the app, set the python environment path to this location, but to the `bin` folder, e.g.

```bash
/Users/user/miniforge3/envs/vuegen_gui/bin
```

#### virtualenv

- tbc

[virutalenv documentation](https://docs.python.org/3/library/venv.html)

```bash
python -m venv .venv --copies --clear --prompt vuegenvenv
```
