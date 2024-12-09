import os
import yaml
from pathlib import Path
from typing import Dict, List, Union, Tuple


def infer_title_from_file_dir_name(filename: str) -> str:
    """
    Infers a human-readable title from a filename, removing leading numeric prefixes.

    Parameters
    ----------
    filename : str
        The filename to infer the title from.

    Returns
    -------
    str
        A human-readable title generated from the filename.
    """
    # Remove leading numbers and underscores if they exist
    name = os.path.splitext(filename)[0]
    parts = name.split("_", 1)
    title = parts[1] if parts[0].isdigit() and len(parts) > 1 else name
    return title.replace("_", " ").title()


def infer_component_metadata(file: Path) -> Dict[str, Union[str, None]]:
    """
    Infers metadata for a file, including component type, plot type, and additional fields.

    Parameters
    ----------
    file : Path
        The file to analyze.

    Returns
    -------
    Dict[str, Union[str, None]]
        A dictionary containing inferred metadata.
    """
    ext = file.suffix.lower()
    metadata = {}

    # Infer component type
    if ext in [".png", ".jpg", ".jpeg", ".gif", ".html", ".graphml", ".gml", ".gexf", ".cyjs"]:
        metadata["component_type"] = "plot"
        if ext in [".png", ".jpg", ".jpeg", ".gif"]:
            metadata["plot_type"] = "static"
        else:
            metadata["plot_type"] = "interactive_network"
    elif ext == ".json":
        metadata["component_type"] = "plot"
        if "plotly" in file.stem.lower():
            metadata["plot_type"] = "plotly"
        elif "altair" in file.stem.lower():
            metadata["plot_type"] = "altair"
        else:
            metadata["plot_type"] = "unknown"
    elif ext in [".csv", ".txt", ".xls", ".xlsx", ".parquet"]:
        metadata["component_type"] = "dataframe"
        metadata["file_format"] = ext.lstrip(".")
        if ext == ".csv":
            metadata["delimiter"] = ","
        elif ext == ".txt":
            metadata["delimiter"] = "\\t"
    elif ext == ".md":
        metadata["component_type"] = "markdown"
    else:
        metadata["component_type"] = "unknown"

    return metadata

def sort_items_by_number_prefix(items: List[Path]) -> List[Path]:
    """
    Sorts a list of Paths by numeric prefixes in their names, placing non-numeric items at the end.

    Parameters
    ----------
    items : List[Path]
        The list of Path objects to sort.

    Returns
    -------
    List[Path]
        The sorted list of Path objects.
    """
    def get_sort_key(item: Path) -> tuple:
        parts = item.name.split("_", 1)
        if parts[0].isdigit():
            numeric_prefix = int(parts[0])
        else:
            numeric_prefix = float('inf')  # Non-numeric prefixes go to the end
        return numeric_prefix, item.name.lower()  # Use `.lower()` for consistent sorting

    return sorted(items, key=get_sort_key)

def generate_subsection_data(subsection_folder: Path, base_folder: Path) -> Dict[str, Union[str, List[Dict]]]:
    """
    Generates data for a single subsection.

    Parameters
    ----------
    subsection_folder : Path
        Path to the subsection folder.
    base_folder : Path
        The base folder path to ensure proper path calculation.

    Returns
    -------
    Dict[str, Union[str, List[Dict]]]
        The subsection data.
    """
    subsection_data = {
        "title": infer_title_from_file_dir_name(subsection_folder.name),
        "description": "",
        "components": [],
    }

    # Sort files by number prefix
    sorted_files = sort_items_by_number_prefix(list(subsection_folder.iterdir()))

    for file in sorted_files:
        if file.is_file():
            metadata = infer_component_metadata(file)

            # Ensure the file path is absolute and relative to base_folder
            file_path = file.resolve()  # Get the absolute path

            # The relative path from base_folder is now absolute to the folder structure
            component_data = {
                "title": infer_title_from_file_dir_name(file.name),
                "file_path": str(file_path),  # Use the absolute file path here
                "description": "",
            }

            # Merge inferred metadata into component data
            component_data.update(metadata)

            subsection_data["components"].append(component_data)

    return subsection_data


def generate_section_data(section_folder: Path, base_folder: Path) -> Dict[str, Union[str, List[Dict]]]:
    """
    Generates data for a single section.

    Parameters
    ----------
    section_folder : Path
        Path to the section folder.
    base_folder : Path
        The base folder path to ensure proper path calculation.

    Returns
    -------
    Dict[str, Union[str, List[Dict]]]
        The section data.
    """
    section_data = {
        "title": infer_title_from_file_dir_name(section_folder.name),
        "description": "",
        "subsections": [],
    }

    # Sort subsections by number prefix 
    sorted_subsections = sort_items_by_number_prefix(list(section_folder.iterdir()))

    for subsection_folder in sorted_subsections:
        if subsection_folder.is_dir():
            section_data["subsections"].append(generate_subsection_data(subsection_folder, base_folder))

    return section_data


def resolve_base_folder(base_folder: str) -> Path:
    """
    Resolves the provided base folder to an absolute path from the root, accounting for relative paths.

    Parameters
    ----------
    base_folder : str
        The relative or absolute path to the base folder.

    Returns
    -------
    Path
        The absolute path to the base folder.
    """
    # Check if we are in a subdirectory and need to go up one level
    project_dir = Path(__file__).resolve().parents[1]

    # If the base_folder is a relative path, resolve it from the project root
    base_folder_path = project_dir / base_folder

    # Make sure the resolved base folder exists
    if not base_folder_path.is_dir():
        raise ValueError(f"Base folder '{base_folder}' does not exist or is not a directory.")

    return base_folder_path


def generate_yaml_structure(folder: str) -> Tuple[Dict[str, Union[str, List[Dict]]], Path]:
    """
    Generates a YAML-compatible structure from a folder hierarchy and returns the resolved folder path.

    Parameters
    ----------
    folder : str
        The base folder containing section and subsection folders.

    Returns
    -------
    Tuple[Dict[str, Union[str, List[Dict]]], Path]
        The YAML-compatible structure and the resolved folder path.
    """
    folder_path = resolve_base_folder(folder)  # Resolve the base folder path

    # Generate the YAML structure
    yaml_structure = {
        "report": {
            "title": infer_title_from_file_dir_name(folder_path.name),
            "description": "",
            "graphical_abstract": "",
            "logo": "",
        },
        "sections": [],
    }

    # Sort sections by their number prefix
    sorted_sections = sort_items_by_number_prefix(list(folder_path.iterdir()))

    for section_folder in sorted_sections:
        if section_folder.is_dir():
            yaml_structure["sections"].append(generate_section_data(section_folder, folder_path))

    return yaml_structure, folder_path

def write_yaml_to_file(yaml_data: Dict, folder_path: Path) -> None:
    """
    Writes the generated YAML structure to a file.

    Parameters
    ----------
    yaml_data : Dict
        The YAML data to write.
    folder_path : Path
        The path where the YAML file should be saved.

    Returns
    -------
    None
    """
    assert isinstance(yaml_data, dict), "YAML data must be a dictionary."
    
    # Generate the output YAML file path based on the folder name
    output_yaml = folder_path / (folder_path.name + "_config.yaml")

    # Ensure the directory exists (but don't create a new folder)
    if not folder_path.exists():
        raise FileNotFoundError(f"The directory {folder_path} does not exist.")

    # Now write the YAML file
    with open(output_yaml, "w") as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False, sort_keys=False)

    print(f"YAML file has been written to {output_yaml}")