## GUI

### Local GUI

We have a simple GUI for VueGen that can be run locally or through a standalone executable.
For now you will need to have a copy of this repository.

```bash
pip install '.[gui]'
cd gui
python app.py
```

### Bundled GUI

The **bundle GUI** with the VueGen package is available under the
[latest releases](https://github.com/Multiomics-Analytics-Group/vuegen/releases/latest).
You will need to unzip the file and run `vuegen_gui` in the unpacked main folder.
Most dependencies are included into the bundle using PyInstaller.

Streamlit works out of the box as a purely Python based package. For `html` creation you will have to
have a Python 3.12 installation with the `jupyter` package installed as `quarto` needs to start
a kernel for execution. This is also true if you install `quarto` globally on your machine.

We recommend using miniforge to install Python and the conda package manager:

- [conda-forge.org/download/](https://conda-forge.org/download/)

We continous our example assuming you have installed the `miniforge` distribution for your
machine (MacOS with arm64/ apple silicon or x86_64/ intel or Windows x86_64). Also download
the [latest `vuegen_gui` bundle](https://github.com/Multiomics-Analytics-Group/vuegen/releases/latest)
from the releases page according to your operating system.

```bash
conda create -n vuegen_gui -c conda-forge python=3.12 jupyter
conda info -e # find environment location
```

Find the vuegen_gui path for your local `user`.

On **MacOS** you need to add a `bin` to the path:

```bash
/Users/user/miniforge3/envs/vuegen_gui/bin
```

On **Windows** you can use the path as displayed by `conda info -e`:

> Note: On Windows a base installation of miniforge with `jupyter` might work as well as
> the app can see your entire Path which is not the case on MacOS.

```bash
C:\Users\user\miniforge3\envs\vuegen_gui
```

More information regarding the app and builds can be found in the
[GUI README](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/gui/README.md).