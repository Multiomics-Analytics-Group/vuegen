from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime

try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum

from io import StringIO
from pathlib import Path
from typing import Iterable, Type
from urllib.parse import urlparse

import networkx as nx
import requests
import yaml
from bs4 import BeautifulSoup


## CHECKS
def check_path(filepath: Path) -> bool:
    """
    Checks if the given file or folder path exists.

    Parameters
    ---------
    filepath : Path
        The file or folder path to check.

    Returns
    -------
    bool
        True if the path exists, False otherwise.
    """

    # Check if the path exists
    return os.path.exists(os.path.abspath(filepath))


def assert_enum_value(
    enum_class: Type[StrEnum], value: str, logger: logging.Logger
) -> StrEnum:
    """
    Validate that the given value is a valid member of the specified enumeration class.

    Parameters
    ----------
    enum_class : Type[StrEnum]
        The enumeration class to validate against.
    value : str
        The value to be validated.
    logger : logging.Logger
        A logger object to track warnings, errors, and info messages.

    Returns
    -------
    StrEnum
        The corresponding member of the enumeration if valid.

    Raises
    ------
    ValueError
        If the value is not a valid member of the enumeration class.
    """
    try:
        return enum_class[value.upper()]
    except KeyError:
        expected_values = ", ".join([str(e.value) for e in enum_class])
        logger.error(
            f"Invalid value for {enum_class.__name__}: '{value}'. Expected values are: {expected_values}"
        )
        raise ValueError(
            f"Invalid {enum_class.__name__}: {value}. Expected values are: {expected_values}"
        )


def is_url(filepath: Path) -> bool:
    """
    Check if the provided path is a valid URL.

    Parameters
    ----------
    filepath : Path
        The filepath to check.

    Returns
    -------
    bool
        True if the input path is a valid URL, meaning it contains both a scheme
        (e.g., http, https, ftp) and a network location (e.g., example.com).
        Returns False if either the scheme or the network location is missing or invalid.
    """
    # Parse the url and return validation
    parsed_url = urlparse(str(filepath))
    return bool(parsed_url.scheme and parsed_url.netloc)


def is_pyvis_html(filepath: str) -> bool:
    """
    Check if the provided HTML file is a Pyvis network visualization.

    Parameters
    ----------
    filepath : str
        The path to the HTML file to check.

    Returns
    -------
    bool
        True if the input HTML file is a Pyvis network, meaning:
        - It contains a `<div>` element with `id="mynetwork"`.
        - The `<body>` only contains `<div>` and `<script>` elements.
        Returns False otherwise.

    """
    # Parse the HTML file
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Validate both conditions
    pyvis_identifier_valid = bool(soup.find("div", {"id": "mynetwork"}))

    # Count top-level elements inside <body>
    body_children = [tag.name for tag in soup.body.find_all(recursive=False)]

    # A pure Pyvis file should contain only "div" and "script" elements in <body>
    body_structure_valid = set(body_children) <= {"div", "script"}

    # Both conditions must be true
    return pyvis_identifier_valid and body_structure_valid


## FILE_SYSTEM
def create_folder(directory_path: str, is_nested: bool = False) -> bool:
    """
    Create a folder. Optionally create nested directories if the specified path includes subdirectories.

    Parameters
    ----------
    directory_path : str
        The path of the directory to create.
    is_nested : bool
        A flag indicating whether to create nested directories (True uses os.makedirs, False uses os.mkdir).

    Returns
    -------
    bool
        True if the folder was created or False if it already existed.

    Raises
    ------
    OSError
        If there is an error creating the directory.
    """
    try:
        if not check_path(directory_path):
            if is_nested:
                # Create the directory and any necessary parent directories
                os.makedirs(directory_path, exist_ok=True)
                return True
            else:
                # Create only the final directory (not nested)
                os.mkdir(directory_path)
                return True
        else:
            return False
    except OSError as e:
        raise OSError(f"Error creating directory '{directory_path}': {e}")


def get_parser(prog_name: str, others: dict = {}) -> argparse.Namespace:
    """
    Initiates argparse.ArgumentParser() and adds common arguments.

    Parameters
    ----------
    prog_name : str
        The name of the program.

    others : dict, optional
        Additional keyword arguments for ArgumentParser initialization.

    Returns
    -------
    argparse.Namespace
        Parsed command-line arguments.

    Raises
    ------
    AssertionError
        If prog_name is not a string or others is not a dictionary.
    """
    # Preconditions
    assert isinstance(prog_name, str), f"prog_name should be a string: {prog_name}"
    assert isinstance(others, dict), f"others must be a dict: {others}"

    # Initialize argument parser
    parser = argparse.ArgumentParser(prog=prog_name, **others)

    # Add arguments
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=None,
        help="Path to the YAML configuration file.",
    )
    parser.add_argument(
        "-dir",
        "--directory",
        type=str,
        default=None,
        help="Path to the directory from which the YAML config will be inferred.",
    )
    parser.add_argument(
        "-rt",
        "--report_type",
        type=str,
        default="streamlit",
        help="Type of the report to generate (streamlit, html, pdf, docx, odt, revealjs, pptx, or jupyter).",
    )
    parser.add_argument(
        "-st_autorun",
        "--streamlit_autorun",
        action="store_true",  # Automatically sets True if the flag is passed
        default=False,
        help="Automatically run the Streamlit app after report generation.",
    )

    # Parse arguments
    return parser


def fetch_file_stream(file_path: str) -> StringIO:
    """
    Fetches a file-like stream from a given file path or URL.

    Parameters
    ----------
    file_path : str
        The path to a local file or a URL to fetch content from.

    Returns
    -------
    StringIO
        A file-like object containing the content of the file or URL.

    Raises
    ------
    AssertionError
        If the file_path is not a valid string.
    FileNotFoundError
        If the file path does not exist for a local file.
    ValueError
        If an error occurs while fetching content from a URL.
    """
    # Assert that the file_path is a string
    assert isinstance(file_path, str), f"File path must be a string: {file_path}"

    if is_url(file_path):
        # Handle URL input
        try:
            response = requests.get(file_path)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return StringIO(response.text)
        except requests.exceptions.RequestException as e:
            raise ValueError(
                f"Error fetching content from URL: {file_path}. Error: {str(e)}"
            )
    else:
        # Handle local file input
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"The file at {file_path} was not found or cannot be accessed."
            )
        with open(file_path, "r") as file:
            return StringIO(file.read())


## FILE_CONVERSION
def cyjs_to_networkx(file_path: str, name: str = "name", ident: str = "id") -> nx.Graph:
    """
    Create a NetworkX graph from a `.cyjs` file in Cytoscape format, including all attributes present in the JSON data.
    This function is modified from the `cytoscape_graph` networkx function to handle the 'value' key explicitly and to include
    all additional attributes found in the JSON data for both nodes and edges.

    Parameters
    ----------
    file_path : str
        The path to a `.cyjs` file (Cytoscape JSON format) containing the network data.
    name : str, optional
        A string which is mapped to the 'name' node element in Cytoscape JSON format.
    ident : str, optional
        A string which is mapped to the 'id' node element in Cytoscape JSON format.
        Must not have the same value as `name`. Default is "id".

    Returns
    -------
    graph : networkx.Graph
        The graph created from the Cytoscape JSON data, including all node and edge attributes.

    Raises
    ------
    NetworkXError
        If the `name` and `ident` attributes are identical.
    ValueError
        If the data format is invalid or missing required elements, such as 'id' or 'name' for nodes.
    """
    try:
        # If file_path is a file-like object (e.g., StringIO), read from it
        if hasattr(file_path, "read"):
            data = json.load(file_path)
        else:
            # Otherwise, assume it's a file path and open the file
            with open(file_path, "r") as json_file:
                data = json.load(json_file)

        if name == ident:
            raise nx.NetworkXError("name and ident must be different.")

        multigraph = data.get("multigraph", False)
        directed = data.get("directed", False)

        if multigraph:
            graph = nx.MultiGraph()
        else:
            graph = nx.Graph()

        if directed:
            graph = graph.to_directed()

        graph.graph = dict(data.get("data", {}))

        # Add nodes with all attributes from the 'data' field of the JSON
        for d in data["elements"]["nodes"]:
            node_data = d["data"].copy()
            node = d["data"].get(ident)  # Use 'id' (or other unique identifier)

            if node is None:
                raise ValueError("Each node must contain an 'id' key.")

            # Optionally include 'name' and 'id' attributes if present
            if name in d["data"]:
                node_data[name] = d["data"].get(name)

            graph.add_node(node)
            graph.nodes[node].update(node_data)

        # Add edges with all attributes from the 'data' field of the JSON
        for d in data["elements"]["edges"]:
            edge_data = d["data"].copy()
            sour = d["data"].get("source")
            targ = d["data"].get("target")
            if sour is None or targ is None:
                raise ValueError("Each edge must contain 'source' and 'target' keys.")

            if multigraph:
                key = d["data"].get("key", 0)
                graph.add_edge(sour, targ, key=key)
                graph.edges[sour, targ, key].update(edge_data)
            else:
                graph.add_edge(sour, targ)
                graph.edges[sour, targ].update(edge_data)
        return graph

    except KeyError as e:
        raise ValueError(f"Missing required key in data: {e}")


def pyvishtml_to_networkx(html_file: str) -> nx.Graph:
    """
    Converts a PyVis HTML file to a NetworkX graph.

    Parameters
    ----------
    html_file : str
        Path to the PyVis HTML file.

    Returns
    -------
    graph : nx.Graph
        NetworkX graph object reconstructed from the PyVis network data.

    Raises
    ------
    ValueError
        If the HTML file does not contain the expected network data, or if nodes lack 'id' attribute.
    """
    # Load the HTML file
    if isinstance(html_file, StringIO):
        # If the input is a StringIO, read its content
        html_content = html_file.getvalue()
    else:
        # Otherwise, treat it as a file path
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Extract the network data from the JavaScript objects
    script_tag = soup.find(
        "script", text=lambda x: x and "nodes = new vis.DataSet" in x
    )
    if not script_tag:
        raise ValueError("Could not find network data in the provided HTML file.")

    # Parse the nodes and edges
    script_text = script_tag.string
    nodes_json = json.loads(
        script_text.split("nodes = new vis.DataSet(")[1].split(");")[0]
    )
    edges_json = json.loads(
        script_text.split("edges = new vis.DataSet(")[1].split(");")[0]
    )

    # Create a NetworkX graph
    graph = nx.Graph()

    # Add nodes
    for node in nodes_json:
        node_id = node.pop("id", None)
        if node_id is None:
            raise ValueError("Node is missing an 'id' attribute.")

        graph.add_node(node_id, **node)

    # Add edges
    for edge in edges_json:
        source = edge.pop("from")
        target = edge.pop("to")
        graph.add_edge(source, target, **edge)

    # Relabel nodes to use 'name' as the identifier, or 'id' if 'name' is unavailable
    mapping = {}
    for node_id, data in graph.nodes(data=True):
        name = data.get("name")
        if name:
            mapping[node_id] = name
        else:
            # Fallback to the original ID if no 'name' exists
            mapping[node_id] = node_id

    graph = nx.relabel_nodes(graph, mapping)

    return graph


## CONFIG
def load_yaml_config(file_path: str) -> dict:
    """
    Load a YAML configuration file and return its contents as a dictionary.

    Parameters
    ----------
    file_path : str
        The path to the YAML configuration file.

    Returns
    -------
    config : dict
        The contents of the YAML file as a dictionary.

    RAISES
    ------
    FileNotFoundError
        If the file does not exist at the specified path.
    ValueError
        If there is an error parsing the YAML file.
    """
    # Check the existence of the file_path
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The config file at {file_path} was not found.")

    # Load the YAML configuration file
    with open(file_path, "r") as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            raise ValueError(f"Error parsing YAML file: {exc}")

    return config


def write_yaml_config(yaml_data: dict, directory_path: Path) -> Path:
    """
    Writes the generated YAML structure to a file.

    Parameters
    ----------
    yaml_data : dict
        The YAML data to write.
    directory_path : Path
        The path where the YAML file should be saved.

    Returns
    -------
    output_yaml : Path
        The path to the written YAML file.
    """
    assert isinstance(yaml_data, dict), "YAML data must be a dictionary."
    assert isinstance(directory_path, Path), "directory_path must be a Path object."

    # Generate the output YAML file path based on the folder name
    _name = yaml_data["report"]["title"].replace(" ", "_").lower()
    output_yaml = directory_path / f"{_name}_config.yaml"

    # Ensure the directory exists (but don't create a new folder)
    if not directory_path.exists():
        raise FileNotFoundError(f"The directory {directory_path} does not exist.")

    # Now write the YAML file
    with open(output_yaml, "w", encoding="utf-8") as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False, sort_keys=False)

    # Return the path to the written file
    return output_yaml


## LOGGING
def get_basename(fname: None | str = None) -> str:
    """
    - For a given filename, returns basename WITHOUT file extension
    - If no fname given (i.e., None) then return basename that the function is called in

    Parameters
    ----------
    fname: str, optional
        The filename to get basename from. Default is None.

    Returns
    -------
    str
        basename of given filepath or the current file the function is executed

    Examples
    ---------
    1)
    >>> get_basename()
    utils

    2)
    >>> get_basename('this/is-a-filepath.csv')
    is-a-filepath
    """
    if fname is not None:
        # PRECONDITION
        if not check_path(fname):
            raise FileNotFoundError(f"The specified path does not exist: {fname}")
        # MAIN FUNCTIONS
        return os.path.splitext(os.path.basename(fname))[0]
    else:
        return os.path.splitext(os.path.basename(sys.argv[0]))[0]


def get_time(incl_time: bool = True, incl_timezone: bool = True) -> str:
    """
    Gets current date, time (optional) and timezone (optional) for file naming

    Parameters
    ----------
    - incl_time (bool): whether to include timestamp in the string
    - incl_timezone (bool): whether to include the timezone in the string

    Returns
    -------
    str
        fname that includes date, timestamp and/or timezone
        connected by '_' in one string e.g. yyyyMMdd_hhmm_timezone

    Examples
    --------
    1)
    >>> get_time()
    '20231019_101758_CEST'

    2)
    >>> get_time(incl_time=False)
    '20231019_CEST'

    """

    # PRECONDITIONALS
    assert isinstance(incl_time, bool), "incl_time must be True or False"
    assert isinstance(incl_timezone, bool), "incl_timezone must be True or False"

    # MAIN FUNCTION
    # getting current time and timezone
    the_time = datetime.now()
    timezone = datetime.now().astimezone().tzname()
    # convert date parts to string

    # putting date parts into one string
    if incl_time and incl_timezone:
        fname = the_time.isoformat(sep="_", timespec="seconds") + "_" + timezone
    elif incl_time:
        fname = the_time.isoformat(sep="_", timespec="seconds")
    elif incl_timezone:
        fname = "_".join([the_time.isoformat(sep="_", timespec="hours")[:-3], timezone])
    else:
        y = str(the_time.year)
        m = str(the_time.month)
        d = str(the_time.day)
        fname = y + m + d

    # optional
    fname = fname.replace(":", "-")  # remove ':' from hours, minutes, seconds

    return fname


def generate_log_filename(folder: str = "logs", suffix: str = "") -> str:
    """
    Creates log file name and path

    Parameters
    ----------
    folder (str): name of the folder to put the log file in
    suffix (str): anything else you want to add to the log file name

    Returns
    -------
    str
        The file path to the log file
    """
    try:
        # PRECONDITIONS
        create_folder(folder)  # ? Path(folder).mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f"Error creating directory '{folder}': {e}")
    # MAIN FUNCTION
    log_filename = get_time(incl_timezone=False) + "_" + suffix + ".log"
    log_filepath = os.path.join(folder, log_filename)

    return log_filepath


def init_log(
    filename: str, display: bool = False, logger_id: str | None = None
) -> logging.Logger:
    """
    - Custom python logger configuration (basicConfig())
        with two handlers (for stdout and for file)
    - from: https://stackoverflow.com/a/44760039
    - Keeps a log record file of the python application, with option to
        display in stdout

    Parameters
    ----------
    filename (str): filepath to log record file
    - display (bool): whether to print the logs to whatever standard output
    - logger_id (str): an optional identifier for yourself,
        if None then defaults to 'root'

    Returns
    -------
    logging.Logger
        The logger object

    Examples
    -----
    >>> logger = init_log('logs/tmp.log', display=True)
    >>> logger.info('Loading things')
    [2023-10-20 10:38:03,074] root: INFO - Loading things
    """
    # PRECONDITIONALS
    assert isinstance(filename, str), "Filename must be a string"
    assert (
        isinstance(logger_id, str) or logger_id is None
    ), "logger_id must be a string or None"

    # MAIN FUNCTION
    # init handlers
    file_handler = logging.FileHandler(filename=filename)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    if display:
        handlers = [file_handler, stdout_handler]
    else:
        handlers = [file_handler]

    # instantiate the logger
    logger = logging.getLogger(logger_id)
    logger.setLevel(logging.DEBUG)
    # logger configuration
    # ! logging.basicConfig has no effect if called once anywhere in the code
    # ! set handlers and format for the logger manually
    # Reset any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Set up the new handlers and format
    formatter = logging.Formatter("[%(asctime)s] %(name)s: %(levelname)s - %(message)s")
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logging.getLogger("matplotlib.font_manager").disabled = True

    return logger


def get_logger(
    log_suffix, folder="logs", display=True, logger_id="vuegen"
) -> tuple[logging.Logger, str]:
    """
    Initialize the logger with a log file name that includes an optional suffix.

    Parameters
    ----------
    log_suffix : str
        A string to append to the log file name.

    Returns
    -------
    tuple[logging.Logger, str]
        A tuple containing the logger instance and the log file path.
    """
    # Generate log file name
    log_file = generate_log_filename(folder=folder, suffix=log_suffix)

    # Initialize logger
    logger = init_log(log_file, display=display, logger_id=logger_id)

    # Log the path to the log file
    logger.info(f"Path to log file: {log_file}")

    return logger, log_file


def print_completion_message(report_type: str):
    """
    Prints a formatted completion message after report generation.
    """
    border = "─" * 65  # Creates a separator line
    if report_type == "streamlit":
        print(
            """🚀 Streamlit Report Generated!

📂 All scripts to build the Streamlit app are available at:
    streamlit_report/sections

▶️ To run the Streamlit app, use the following command:
    streamlit run streamlit_report/sections/report_manager.py

✨ You can extend the report by adding new files to the input directory or updating the config file.

🛠️ Advanced users can modify the Python scripts directly in:
    streamlit_report/sections
"""
        )
    else:
        print(
            f"""🚀 {report_type.capitalize()} Report Generated!

📂 Your {report_type} report is available at:
    quarto_report

✨ You can extend the report by adding new files to the input directory or updating the config file.

🛠️ Advanced users can modify the report template directly in:
    quarto_report/quarto_report.qmd
"""
        )

    print(border)


## REPORT FORMATTING
def generate_footer() -> str:
    """
    Generate an HTML footer for a report.

    This function creates a styled HTML footer that includes a link to VueGen
    and the Multiomics Network Analytics Group (MoNA).

    Returns
    -------
    str
        A formatted HTML string representing the footer.
    """
    footer = """<style type="text/css">
.footer {
    position: relative;
    left: 0;
    width: 100%;
    text-align: center;
}
</style>
<footer class="footer">
    This report was generated with 
    <a href="https://github.com/Multiomics-Analytics-Group/vuegen" target="_blank">
        <img src="https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_logo.svg" alt="VueGen" width="65px">
    </a>
    | Copyright 2025 <a href="https://github.com/Multiomics-Analytics-Group" target="_blank">
        Multiomics Network Analytics Group (MoNA)
    </a>
</footer>"""
    return footer


def sort_imports(imp: Iterable[str]) -> tuple[list[str], list[str]]:
    """Separte 'from' and 'import' statements from setup code.

    Parameters
    ----------
    imp : Iterable[str]
        A list of import statements and setup statements.

    Returns
    -------
    Tuple[List[str], List[str]]
        A tuple of two lists: one for import statements and one for setup statements.

    Examples
    --------
    >>> imp = [
    ...     'import logging',
    ...     'import shutil',
    ...     'logging.basicConfig(level=logging.INFO)',
    ...     'import pandas as pd',
    ...     'import numpy as np',
    ... ]
    >>> sort_imports(imp)
    (['import logging', 'import numpy as np', 'import pandas as pd', 'import shutil
    ], ['logging.basicConfig(level=logging.INFO)'])
    """
    imports_statements, setup_statements = [], []
    for line in imp:
        line = line.strip()  # just for safety
        if line.startswith("from ") or line.startswith("import "):
            imports_statements.append(line)
        else:
            setup_statements.append(line)
    imports_statements.sort()
    setup_statements.sort()
    return imports_statements, setup_statements
