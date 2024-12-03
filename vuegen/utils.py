import os
import sys
import yaml
from datetime import datetime
import logging
import argparse
import networkx as nx
import json
from enum import StrEnum
from typing import Type

## CHECKS
def check_path(filepath: str) -> bool:
    """
    Checks if the given file or folder path exists.

    Parameters
    ---------
    filepath : str
        The file or folder path to check.

    Returns
    -------
    bool
        True if the path exists, False otherwise.

    Raises
    ------
    AssertionError
        If the filepath is not a valid string.
    """
    # Assert that the filepath is a string
    assert isinstance(filepath, str), f"Filepath must be a string: {filepath}"

    # Check if the path exists
    return os.path.exists(os.path.abspath(filepath))


def assert_enum_value(enum_class: Type[StrEnum], value: str, logger: logging.Logger) -> StrEnum:
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
        logger.error(f"Invalid value for {enum_class.__name__}: '{value}'. Expected values are: {expected_values}")
        raise ValueError(f"Invalid {enum_class.__name__}: {value}. Expected values are: {expected_values}")

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

def get_args(prog_name: str, others: dict = {}) -> argparse.Namespace:
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
        default="report_config_micw2graph.yaml",
        help="Path to the YAML configuration file."
    )
    parser.add_argument(
        "-rt",
        "--report_type",
        type=str,
        default=None,
        help="Type of the report to generate (streamlit, html, pdf, docx, odt, revealjs, pptx, or jupyter)."
    )

    # Parse arguments
    return parser.parse_args()


def cyjs2graph(file_path: str, name: str = "name", ident: str = "id") -> nx.Graph:
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
    G : networkx.Graph
        The graph created from the Cytoscape JSON data, including all node and edge attributes.

    Raises
    ------
    NetworkXError
        If the `name` and `ident` attributes are identical.
    ValueError
        If the data format is invalid or missing required elements, such as 'id' or 'name' for nodes.
    """
    try:
        # Load data from the provided .cyjs file path
        with open(file_path, 'r') as json_file:
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
    with open(file_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            raise ValueError(f"Error parsing YAML file: {exc}")

    return config

## LOGGING
def get_basename(fname: None | str = None) -> str:
    """
    - For a given filename, returns basename WITHOUT file extension
    - If no fname given (i.e., None) then return basename that the function is called in

    PARAMS
    -----
    - fname (None or str): the filename to get basename of, or None

    OUTPUTS
    -----
    - basename of given filepath or the current file the function is executed

    Examples
    -----
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
    -----
    - incl_time (bool): whether to include timestamp in the string
    - incl_timezone (bool): whether to include the timezone in the string

    Returns
    -----
    - fname (str): includes date, timestamp and/or timezone
        connected by '_' in one string e.g. yyyyMMdd_hhmm_timezone

    Examples
    -----
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
    y = str(the_time.year)
    M = str(the_time.month)
    d = str(the_time.day)
    h = str(the_time.hour)
    m = str(the_time.minute)
    s = str(the_time.second)
    # putting date parts into one string
    if incl_time and incl_timezone:
        fname = "_".join([y + M + d, h + m + s, timezone])
    elif incl_time:
        fname = "_".join([y + M + d, h + m + s])
    elif incl_timezone:
        fname = "_".join([y + M + d, timezone])
    else:
        fname = y + M + d

    # POSTCONDITIONALS
    parts = fname.split("_")
    if incl_time and incl_timezone:
        assert len(parts) == 3, f"time and/or timezone inclusion issue: {fname}"
    elif incl_time or incl_timezone:
        assert len(parts) == 2, f"time/timezone inclusion issue: {fname}"
    else:
        assert len(parts) == 1, f"time/timezone inclusion issue: {fname}"

    return fname


def generate_log_filename(folder: str = "logs", suffix: str = "") -> str:
    """
    Creates log file name and path

    Parameters
    -----
    folder (str): name of the folder to put the log file in
    suffix (str): anything else you want to add to the log file name

    Returns
    -----
    log_filepath (str): the file path to the log file
    """
    # PRECONDITIONS
    create_folder(folder)

    # MAIN FUNCTION
    log_filename = get_time(incl_timezone=False) + "_" + suffix + ".log"
    log_filepath = os.path.join(folder, log_filename)

    return log_filepath


def init_log(filename: str, display: bool = False, logger_id: str | None = None):
    """
    - Custom python logger configuration (basicConfig())
        with two handlers (for stdout and for file)
    - from: https://stackoverflow.com/a/44760039
    - Keeps a log record file of the python application, with option to
        display in stdout

    Parameters
    -----
    - filename (str): filepath to log record file
    - display (bool): whether to print the logs to whatever standard output
    - logger_id (str): an optional identifier for yourself,
        if None then defaults to 'root'

    Returns
    -----
    - logger object

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

    # logger configuration
    logging.basicConfig(
        # level=logging.DEBUG,
        format="[%(asctime)s] %(name)s: %(levelname)s - %(message)s",
        handlers=handlers,
    )
    logging.getLogger("matplotlib.font_manager").disabled = True

    # instantiate the logger
    logger = logging.getLogger(logger_id)
    logger.setLevel(logging.DEBUG)

    return logger


def get_logger(log_suffix):
    """
    Initialize the logger with a log file name that includes an optional suffix.

    Parameters
    ----------
    log_suffix : str
        A string to append to the log file name.

    Returns
    -------
    logging.Logger
        An initialized logger instance.
    """
    # Generate log file name
    log_file = generate_log_filename(suffix=log_suffix)
    
    # Initialize logger
    logger = init_log(log_file, display=True)
    
    # Log the path to the log file
    logger.info(f"Path to log file: {log_file}")

    return logger
