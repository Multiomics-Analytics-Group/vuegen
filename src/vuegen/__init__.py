"""VueGen automates the creation of reports from bioinformatics outputs,
supporting formats like PDF, HTML, DOCX, ODT, PPTX, Reveal.js, Jupyter notebooks,
and Streamlit web applications. Users simply provide a directory with output files
and VueGen compiles them into a structured report."""

from importlib import metadata

__version__ = metadata.version("vuegen")
