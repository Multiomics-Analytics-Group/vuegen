import os
from pathlib import Path
import report as r
from typing import Dict, List, Union, Tuple

def _create_title_fromdir(file_dirname: str) -> str:
    """
    Infers title from a file or directory, removing leading numeric prefixes.

    Parameters
    ----------
    file_dirname : str
        The file or directory name to infer the title from.

    Returns
    -------
    str
        A title generated from the file or directory name.
    """
    # Remove leading numbers and underscores if they exist
    name = os.path.splitext(file_dirname)[0]
    parts = name.split("_", 1)
    title = parts[1] if parts[0].isdigit() and len(parts) > 1 else name
    return title.replace("_", " ").title()

def _create_component_config_fromfile(file_path: Path) -> Dict[str, str]:
    """
    Infers a component config from a file, including component type, plot type, and additional fields.

    Parameters
    ----------
    file_path : Path
        The file path to analyze.

    Returns
    -------
    component_config : Dict[str, str]
        A dictionary containing inferred component configuration.
    """
    file_ext = file_path.suffix.lower()
    component_config = {}

    # Infer component config
    if file_ext in [r.DataFrameFormat.CSV.value_with_dot, r.DataFrameFormat.TXT.value_with_dot]:
        # Check for CSVNetworkFormat keywords
        if "edgelist" in file_path.stem.lower():
            component_config["component_type"] = r.ComponentType.PLOT.value
            component_config["plot_type"] = r.PlotType.INTERACTIVE_NETWORK.value
            component_config ["csv_network_format"] = r.CSVNetworkFormat.EDGELIST.value
        elif "adjlist" in file_path.stem.lower():
            component_config ["component_type"] = r.ComponentType.PLOT.value
            component_config ["plot_type"] = r.PlotType.INTERACTIVE_NETWORK.value
            component_config ["csv_network_format"] = r.CSVNetworkFormat.ADJLIST.value
        # Fill the config with dataframe content
        else:
            component_config ["component_type"] = r.ComponentType.DATAFRAME.value
            component_config ["file_format"] = r.DataFrameFormat.CSV.value if file_ext == r.DataFrameFormat.CSV.value_with_dot else r.DataFrameFormat.TXT.value
            component_config ["delimiter"] = "," if file_ext == r.DataFrameFormat.CSV.value_with_dot else "\\t"
    # Check other DataframeFormats than csv and txt
    elif file_ext in [fmt.value_with_dot for fmt in r.DataFrameFormat if fmt not in [r.DataFrameFormat.CSV, r.DataFrameFormat.TXT]]:
        component_config ["component_type"] = r.ComponentType.DATAFRAME.value
        component_config ["file_format"] = next(fmt.value for fmt in r.DataFrameFormat if fmt.value_with_dot == file_ext)
    # Check for network formats
    elif file_ext in [fmt.value_with_dot for fmt in r.NetworkFormat]:
        component_config ["component_type"] = r.ComponentType.PLOT.value
        if file_ext in [
            r.NetworkFormat.PNG.value_with_dot,
            r.NetworkFormat.JPG.value_with_dot,
            r.NetworkFormat.JPEG.value_with_dot,
            r.NetworkFormat.SVG.value_with_dot,
        ]:
            component_config ["plot_type"] = r.PlotType.STATIC.value
        else:
            component_config ["plot_type"] = r.PlotType.INTERACTIVE_NETWORK.value
    # Check for interactive plots 
    elif file_ext == ".json":
        component_config ["component_type"] = r.ComponentType.PLOT.value
        if "plotly" in file_path.stem.lower():
            component_config ["plot_type"] = r.PlotType.PLOTLY.value
        elif "altair" in file_path.stem.lower():
            component_config ["plot_type"] = r.PlotType.ALTAIR.value
        else:
            component_config ["plot_type"] = "unknown"
    elif file_ext == ".md":
        component_config ["component_type"] = r.ComponentType.MARKDOWN.value
    else:
        error_msg = (
            f"Unsupported file extension: {file_ext}. "
            f"Supported extensions include:\n"
            f"  - Network formats: {', '.join(fmt.value_with_dot for fmt in r.NetworkFormat)}\n"
            f"  - DataFrame formats: {', '.join(fmt.value_with_dot for fmt in r.DataFrameFormat)}"
        )
        #self.logger.error(error_msg)
        raise ValueError(error_msg)

    return component_config 

def _sort_paths_by_numprefix(paths: List[Path]) -> List[Path]:
    """
    Sorts a list of Paths by numeric prefixes in their names, placing non-numeric items at the end.

    Parameters
    ----------
    paths : List[Path]
        The list of Path objects to sort.

    Returns
    -------
    List[Path]
        The sorted list of Path objects.
    """
    def get_sort_key(path: Path) -> tuple:
        parts = path.name.split("_", 1)
        if parts[0].isdigit():
            numeric_prefix = int(parts[0])
        else:
            # Non-numeric prefixes go to the end
            numeric_prefix = float('inf')  
        return numeric_prefix, path.name.lower()  

    return sorted(paths, key=get_sort_key)

def _create_subsect_config_fromdir(subsection_dir_path: Path) -> Dict[str, Union[str, List[Dict]]]:
    """
    Creates subsection config from a directory.

    Parameters
    ----------
    subsection_dir_path : Path
        Path to the subsection directory.

    Returns
    -------
    Dict[str, Union[str, List[Dict]]]
        The subsection config.
    """
    subsection_config = {
        "title": _create_title_fromdir(subsection_dir_path.name),
        "description": "",
        "components": [],
    }

    # Sort files by number prefix
    sorted_files = _sort_paths_by_numprefix(list(subsection_dir_path.iterdir()))

    for file in sorted_files:
        if file.is_file():
            component_config = _create_component_config_fromfile(file)

            # Ensure the file path is absolute
            file_path = file.resolve()  

            component_config_updt = {
                "title": _create_title_fromdir(file.name),
                "file_path": str(file_path), 
                "description": "",
            }

            # Update inferred config information
            component_config.update(component_config_updt)

            subsection_config["components"].append(component_config)

    return subsection_config

def _create_sect_config_fromdir(section_dir_path: Path) -> Dict[str, Union[str, List[Dict]]]:
    """
    Creates section config from a directory.

    Parameters
    ----------
    section_dir_path : Path
        Path to the section directory.

    Returns
    -------
    Dict[str, Union[str, List[Dict]]]
        The section config.
    """
    section_config = {
        "title": _create_title_fromdir(section_dir_path.name),
        "description": "",
        "subsections": [],
    }

    # Sort subsections by number prefix 
    sorted_subsections = _sort_paths_by_numprefix(list(section_dir_path.iterdir()))

    for subsection_dir in sorted_subsections:
        if subsection_dir.is_dir():
            section_config["subsections"].append(_create_subsect_config_fromdir(subsection_dir))

    return section_config


def _resolve_base_dir(base_dir: str) -> Path:
    """
    Resolves the provided base directory to an absolute path from the root, accounting for relative paths.

    Parameters
    ----------
    base_dir : str
        The relative or absolute path to the base directory.

    Returns
    -------
    Path
        The absolute path to the base directory.
    """
    # Check if we are in a subdirectory and need to go up one level
    project_dir = Path(__file__).resolve().parents[1]

    # If the base_dir is a relative path, resolve it from the project root
    base_dir_path = project_dir / base_dir

    # Make sure the resolved base directory exists
    if not base_dir_path.is_dir():
        raise ValueError(f"Base directory '{base_dir}' does not exist or is not a directory.")

    return base_dir_path


def create_yamlconfig_fromdir(base_dir: str) -> Tuple[Dict[str, Union[str, List[Dict]]], Path]:
    """
    Generates a YAML-compatible config file from a directory. It also returns the resolved folder path.

    Parameters
    ----------
    base_dir : str
        The base directory containing section and subsection folders.

    Returns
    -------
    Tuple[Dict[str, Union[str, List[Dict]]], Path]
        The YAML config and the resolved directory path.
    """
    # Get absolute path from base directory
    base_dir_path = _resolve_base_dir(base_dir)

    # Generate the YAML config
    yaml_config = {
        "report": {
            "title": _create_title_fromdir(base_dir_path.name),
            "description": "",
            "graphical_abstract": "",
            "logo": "",
        },
        "sections": [],
    }

    # Sort sections by their number prefix
    sorted_sections = _sort_paths_by_numprefix(list(base_dir_path.iterdir()))

    # Generate sections and subsections config 
    for section_dir in sorted_sections:
        if section_dir.is_dir():
            yaml_config["sections"].append(_create_sect_config_fromdir(section_dir))

    return yaml_config, base_dir_path