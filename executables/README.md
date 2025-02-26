# Pyinstaller one folder executable

- pyvis templates were not copied, so make these explicit (see [this](https://stackoverflow.com/a/72687433/9684872))

```bash
# from root of the project
pyinstaller -D --collect-all pyvis -n vuegen src/vuegen/__main__.py
# from this README folder
pyinstaller -D --collect-all pyvis --collect-all streamlit -n vuegen ../src/vuegen/__main__.py
```

## Pyinstaller options

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

## Using bundled executable

try using basic example

```bash
./dist/vuegen/vuegen -d  ../docs/example_data/Basic_example_vuegen_demo_notebook -st_autorun
```
