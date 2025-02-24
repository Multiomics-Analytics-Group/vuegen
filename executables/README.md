# Pyinstaller one folder executable

- pyvis templates were not copied, so make these explicit (see [this](https://stackoverflow.com/a/72687433/9684872))

```
# from root of the project
pyinstaller -D -w --collect-all pyvis -n vuegen src/vuegen/__main__.py
```
