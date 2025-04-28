## Installation


:::{TIP}
It is recommended to install VueGen inside a virtual environment to manage depenendencies and avoid conflicts with existing packages. You can use the virtual environment manager of your choice, such as `poetry`, `conda`, or `pipenv`.
:::


### Pip

VueGen is available on [PyPI](https://pypi.org/project/vuegen/) and can be installed using pip:

```bash
pip install vuegen
```

You can also install the package for development by cloning this repository and running the following command:

```bash
pip install -e path/to/vuegen # specify location
pip install -e . # in case your pwd is in the vuegen directory
```

### Conda

VueGen is also available on [Bioconda](https://anaconda.org/bioconda/vuegen) and can be installed using conda:

```bash
conda install bioconda::vuegen
```

### Dependencies

VueGen uses [Quarto](https://quarto.org/) to generate various report types. The pip insallation includes quarto using the [quarto-cli Python library](https://pypi.org/project/quarto-cli/). To test if quarto is installed in your computer, run the following command:

```bash
quarto check
```

:::{TIP}
If quarto is not installed, you can download the command-line interface from the [Quarto website](https://quarto.org/docs/get-started/) for your operating system.
:::


For PDF reports, you need to have a LaTeX distribution installed. This can be done with quarto using the following command:

```bash
quarto install tinytex
```

:::{TIP}
Also, you can add the `--quarto_checks` argument to the VueGen command to check and install the required dependencies automatically.
:::


### Docker

If you prefer not to install VueGen on your system, a pre-configured Docker container is available. It includes all dependencies, ensuring a fully reproducible execution environment. See the [Execution section](#execution) for details on running VueGen with Docker. The official Docker images are available at [quay.io/dtu_biosustain_dsp/vuegen](https://quay.io/repository/dtu_biosustain_dsp/vuegen). The Dockerfiles to build the images are available [here](https://github.com/Multiomics-Analytics-Group/nf-vuegen/tree/main/Docker).

### Nextflow and nf-core

VueGen is also available as a [nf-core](https://nf-co.re/) module, customised for compatibility with the [Nextflow](https://www.nextflow.io/) environment. This module is designed to automate report generation from outputs produced by other modules, subworkflows, or pipelines. The code and documentation for the nf-core module are available in the [nf-VueGen repository](https://github.com/Multiomics-Analytics-Group/nf-vuegen/).