clean:
	rm -r dist build lib vuegen.spec quarto_report streamlit_report

clean-all: clean
	rm -r logs

bundle:
	pip install -e ../.
	pyinstaller \
	-n vuegen_gui \
	--noconfirm \
	--onedir \
	--windowed \
	--collect-all streamlit \
	--collect-all st_aggrid  \
	--collect-all customtkinter \
	--collect-all quarto_cli \
	--collect-all plotly \
	--collect-all _plotly_utils \
	--collect-all pyvis \
	--collect-all pandas \
	--collect-all numpy \
	--collect-all matplotlib \
	--collect-all openpyxl \
	--collect-all xlrd \
	--collect-all nbformat \
	--collect-all nbclient \
	--collect-all altair \
	--collect-all itables \
	--collect-all kaleido \
	--collect-all pyarrow \
	--collect-all dataframe_image \
	--collect-all narwhals \
	--collect-all PIL \
	--collect-all traitlets \
	--collect-all referencing \
	--collect-all rpds \
	--collect-all tenacity \
	--collect-all vl_convert \
	--collect-all typing-extensions \
	--add-data ../docs/example_data/Basic_example_vuegen_demo_notebook:example_data/Basic_example_vuegen_demo_notebook \
	--add-data ../docs/images/logo/vuegen_logo.png:. \
	app.py


# jupyter kernel specific:
# --collect-all yaml \
# --collect-all strenum \
# --collect-all jinja2 \
# --collect-all fastjsonschema \
# --collect-all jsonschema \
# --collect-all jsonschema_specifications \
# --collect-all nbclient \
# --collect-all nbformat \

#  beautifulsoup4, bleach, defusedxml, importlib-metadata, jinja2, jupyter-core, jupyterlab-pygments, markupsafe, mistune, nbclient, nbformat, packaging, pandocfilters, pygments, traitlets
# remaining packages in full environment:
# --collect-all jupyterlab \
# --collect-all jupyter_core \
# --collect-all yaml \
# --collect-all ipykernel \
# --collect-all nbconvert \
# --collect-all notebook \
# --collect-all ipywidgets \
# --collect-all jupyter_console \
# --collect-all jupyter_client \
# --collect-all webencodings \
# --collect-all wcwidth \
# --collect-all pytz \
# --collect-all python-decouple\
# --collect-all pure-eval \
# --collect-all ptyprocess \
# --collect-all kaleido \
# --collect-all fastjsonschema\
# --collect-all xlrd \
# --collect-all widgetsnbextension\
# --collect-all wheel \
# --collect-all websocket-client\
# --collect-all webcolors \
# --collect-all vl-convert-python\
# --collect-all urllib3 \
# --collect-all uri-template \
# --collect-all tzdata \
# --collect-all types-python-dateutil \
# --collect-all traitlets \
# --collect-all tornado \
# --collect-all toml \
# --collect-all tinycss2 \

# --collect-all soupsieve \
# --collect-all sniffio \
# --collect-all smmap \
# --collect-all six \
# --collect-all setuptools \
# --collect-all send2trash \
# --collect-all rpds-py \
# --collect-all rfc3986-validator\
# --collect-all pyzmq \
# --collect-all pyyaml \
# --collect-all python-json-logger\
# --collect-all pyparsing \
# --collect-all pygments \
# --collect-all pycparser \
# --collect-all pyarrow \
# --collect-all psutil \
# --collect-all protobuf \
# --collect-all propcache \
# --collect-all prompt_toolkit\
# --collect-all prometheus-client \
# --collect-all platformdirs \
# --collect-all pillow \ # PIL
# --collect-all pexpect \
# --collect-all parso \
# --collect-all pandocfilters\
# --collect-all packaging \
# --collect-all overrides \
# --collect-all numpy \
# --collect-all networkx \
# --collect-all nest-asyncio \
# --collect-all multidict \
# --collect-all more-itertools\
# --collect-all mistune \
# --collect-all mdurl \
# --collect-all MarkupSafe \
# --collect-all lxml \
# --collect-all kiwisolver \
# --collect-all jupyterlab_widgets\
# --collect-all jupyterlab_pygments \
# --collect-all jsonpointer \
# --collect-all jsonpickle \
# --collect-all json5 \
# --collect-all idna \
# --collect-all h11\
# --collect-all greenlet \
# --collect-all frozenlist \
# --collect-all fqdn \
# --collect-all fonttools \
# --collect-all executing \
# --collect-all et-xmlfile \
# --collect-all defusedxml \
# --collect-all decorator \
# --collect-all debugpy \
# --collect-all cycler \
# --collect-all cssselect \
# --collect-all click \
# --collect-all charset-normalizer\
# --collect-all certifi \
# --collect-all cachetools \
# --collect-all blinker \
# --collect-all bleach \
# --collect-all babel \
# --collect-all attrs \
# --collect-all async-lru \
# --collect-all asttokens \
# --collect-all appnope \
# --collect-all aiohappyeyeballs\
# --collect-all yarl \
# --collect-all terminado \
# --collect-all stack_data \
# --collect-all rfc3339-validator\
# --collect-all requests \
# --collect-all referencing\
# --collect-all python-dateutil \
# --collect-all pyee \
# --collect-all plotly \
# --collect-all openpyxl \
# --collect-all matplotlib-inline\
# --collect-all markdown-it-py \
# --collect-all jupyter-core \
# --collect-all jinja2 \
# --collect-all jedi \
# --collect-all ipython-pygments-lexers\
# --collect-all httpcore \
# --collect-all gitdb \
# --collect-all cssutils \
# --collect-all contourpy \
# --collect-all comm \
# --collect-all cffi \
# --collect-all beautifulsoup4\
# --collect-all anyio \
# --collect-all aiosignal \
# --collect-all rich \
# --collect-all pydeck \
# --collect-all playwright \
# --collect-all pandas \
# --collect-all matplotlib \
# --collect-all jupyter-server-terminals\
# --collect-all jupyter-client \
# --collect-all jsonschema-specifications \
# --collect-all ipython \
# --collect-all httpx \
# --collect-all gitpython \
# --collect-all arrow \
# --collect-all argon2-cffi-bindings\
# --collect-all aiohttp \
# --collect-all pyvis \
# --collect-all jsonschema \
# --collect-all isoduration\
# --collect-all ipywidgets \
# --collect-all ipykernel \
# --collect-all argon2-cffi\
# --collect-all nbformat \
# --collect-all jupyter-console\
# --collect-all altair \
# --collect-all streamlit \
# --collect-all nbclient \
# --collect-all jupyter-events\
# --collect-all streamlit-aggrid \
# --collect-all nbconvert \
# --collect-all jupyter-server\
# --collect-all dataframe-image \
# --collect-all notebook-shim \
# --collect-all jupyterlab-server \
# --collect-all jupyter-lsp \
# --collect-all jupyterlab \
# --collect-all notebook \
# --collect-all jupyter \
# --collect-all vuegen

