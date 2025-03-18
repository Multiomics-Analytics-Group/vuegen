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

- [ ] can we ship a python environment with the app which can be used to launch a kernel?

## Features of the GUI

- select a directory via a file dialog button
- specify the distination of a config file manually
- select a report
- select if streamlit app should be started - has no effect for quarto reports
- show set PATH
- select a Python environment for starting jupyter kernels for quarto reports which is cached
- some message boxes

## Bundled PyInstaller execution (current status)

1. Can be executed. Streamlit apps can be run (although sometimes not easily terminated)
2. All quarto based reports need to specify a path to a python environment where python 3.12
   is installed along `jupyter`
   - This could be partly replace by a full anaconda distribution on the system.
   - maybe a self-contained minimal virtual environment for kernel starting can be added later
   - we could add some logic to make sure a correct path is added.

## Using bundle vuegen release

This should both work on Windows and MacOs, but the paths for environments can be different
dependent on the system.

### Create environment using conda

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

### virtualenv

Following the
[Python Packaging User Guide's instructions](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-a-new-virtual-environment)
you can run the following command to create a new virtual environment.

Install an offical Python version from [python.org/downloads/](https://www.python.org/downloads/)

#### On MacOs

```bash
# being in the folder you want to create the environment
python -m venv .venv
# if that does not work, try
# python3 -m venv .venv
source .venv/bin/activate
pip install jupyter
```

#### On Windows

```powershell
# being in the folder you want to create the environment
python -m venv .venv
# if that does not work, try
# py -m venv .venv
.venv\Scripts\activate
```

#### Troubleshooting venv

For more information on the options, see also the
[virutalenv documentation](https://docs.python.org/3/library/venv.html) in the Python
standard library documentation.

```
python -m venv .venv --copies --clear --prompt vuegenvenv
```

### On Windows

On windows the default Paths is available in the application. This would allow to use
the default python installation and a global quarto installation.

to test, one could

- use global quarto and python installations can be used
- add a deactivate button into app for bundled quarto (so path is not set)

### On MacOs

- on MacOs the default paths are not set, but only the minimal one `/usr/bin:/bin:/usr/sbin:/sbin`,
  see pyinstaller hints
  [on path manipulations](https://pyinstaller.org/en/stable/common-issues-and-pitfalls.html#macos)
- requires to add path to python environment manually
