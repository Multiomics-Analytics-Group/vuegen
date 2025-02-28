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
