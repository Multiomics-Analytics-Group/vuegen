import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from . import report as r
from .utils import assert_enum_value, get_logger, is_pyvis_html


class ConfigManager:
    """
    Class for handling metadata of reports from YAML config file and creating report objects.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initializes the ConfigManager with a logger.

        Parameters
        ----------
        logger : logging.Logger, optional
            A logger instance for the class. If not provided, a default logger will be created.
        """
        if logger is None:
            logger, _ = get_logger("report")
        self.logger = logger

    def _create_title_fromdir(self, file_dirname: str) -> str:
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

    def _create_component_config_fromfile(self, file_path: Path) -> Dict[str, str]:
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

        # Add title, file path, and description
        component_config["title"] = self._create_title_fromdir(file_path.name)
        component_config["file_path"] = (
            file_path.resolve().as_posix()
        )  # ! needs to be posix for all OS support
        component_config["description"] = ""
        component_config["caption"] = ""

        # Infer component config
        if file_ext in [
            r.DataFrameFormat.CSV.value_with_dot,
            r.DataFrameFormat.TXT.value_with_dot,
        ]:
            # Check for CSVNetworkFormat keywords
            if "edgelist" in file_path.stem.lower():
                component_config["component_type"] = r.ComponentType.PLOT.value
                component_config["plot_type"] = r.PlotType.INTERACTIVE_NETWORK.value
                component_config["csv_network_format"] = (
                    r.CSVNetworkFormat.EDGELIST.value
                )
            elif "adjlist" in file_path.stem.lower():
                component_config["component_type"] = r.ComponentType.PLOT.value
                component_config["plot_type"] = r.PlotType.INTERACTIVE_NETWORK.value
                component_config["csv_network_format"] = (
                    r.CSVNetworkFormat.ADJLIST.value
                )
            # Fill the config with dataframe content
            else:
                component_config["component_type"] = r.ComponentType.DATAFRAME.value
                component_config["file_format"] = (
                    r.DataFrameFormat.CSV.value
                    if file_ext == r.DataFrameFormat.CSV.value_with_dot
                    else r.DataFrameFormat.TXT.value
                )
                component_config["delimiter"] = (
                    "," if file_ext == r.DataFrameFormat.CSV.value_with_dot else "\\t"
                )
        # Check other DataframeFormats than csv and txt
        elif file_ext in [
            fmt.value_with_dot
            for fmt in r.DataFrameFormat
            if fmt not in [r.DataFrameFormat.CSV, r.DataFrameFormat.TXT]
        ]:
            component_config["component_type"] = r.ComponentType.DATAFRAME.value
            component_config["file_format"] = next(
                fmt.value for fmt in r.DataFrameFormat if fmt.value_with_dot == file_ext
            )
        elif file_ext == ".html":
            if is_pyvis_html(file_path):
                component_config["component_type"] = r.ComponentType.PLOT.value
                component_config["plot_type"] = r.PlotType.INTERACTIVE_NETWORK.value
            else:
                component_config["component_type"] = r.ComponentType.HTML.value
        # Check for network formats
        elif file_ext in [fmt.value_with_dot for fmt in r.NetworkFormat]:
            component_config["component_type"] = r.ComponentType.PLOT.value
            if file_ext in [
                r.NetworkFormat.PNG.value_with_dot,
                r.NetworkFormat.JPG.value_with_dot,
                r.NetworkFormat.JPEG.value_with_dot,
                r.NetworkFormat.SVG.value_with_dot,
            ]:
                component_config["plot_type"] = r.PlotType.STATIC.value
            else:
                component_config["plot_type"] = r.PlotType.INTERACTIVE_NETWORK.value
        # Check for interactive plots
        elif file_ext == ".json":
            component_config["component_type"] = r.ComponentType.PLOT.value
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                if "$schema" in json_data:
                    component_config["plot_type"] = r.PlotType.ALTAIR.value
                else:
                    component_config["plot_type"] = r.PlotType.PLOTLY.value
            except Exception as e:
                self.logger.warning(f"Could not parse JSON file {file_path}: {e}")
                component_config["plot_type"] = "unknown"
        elif file_ext == ".md":
            component_config["component_type"] = r.ComponentType.MARKDOWN.value
        else:
            self.logger.error(
                f"Unsupported file extension: {file_ext}. Skipping file: {file_path}\n"
            )
            return None

        return component_config

    def _sort_paths_by_numprefix(self, paths: List[Path]) -> List[Path]:
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
                numeric_prefix = float("inf")
            return numeric_prefix, path.name.lower()

        return sorted(paths, key=get_sort_key)

    def _read_description_file(self, folder_path: Path) -> str:
        """
        Reads the content of a description.md file if it exists in the given folder.

        Parameters
        ----------
        folder_path : Path
            Path to the folder where description.md might be located.

        Returns
        -------
        str
            Content of the description.md file if found, otherwise an empty string.
        """
        description_file = folder_path / "description.md"
        if description_file.exists():
            ret = description_file.read_text().strip().replace("\n", "\n  ")
            return f"{ret}\n"
        return ""

    def _create_subsect_config_fromdir(
        self, subsection_dir_path: Path
    ) -> Dict[str, Union[str, List[Dict]]]:
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
        # Sort files by number prefix
        sorted_files = self._sort_paths_by_numprefix(
            list(subsection_dir_path.iterdir())
        )

        components = []
        for file in sorted_files:
            if file.is_file():
                component_config = self._create_component_config_fromfile(file)
                # Skip unsupported files
                if component_config is None:
                    continue
                # Add component config to list
                components.append(component_config)

        subsection_config = {
            "title": self._create_title_fromdir(subsection_dir_path.name),
            "description": self._read_description_file(subsection_dir_path),
            "components": components,
        }
        return subsection_config

    def _create_sect_config_fromdir(
        self, section_dir_path: Path
    ) -> Dict[str, Union[str, List[Dict]]]:
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
        # Sort subsections by number prefix
        sorted_subsections = self._sort_paths_by_numprefix(
            list(section_dir_path.iterdir())
        )

        subsections = []
        for subsection_dir in sorted_subsections:
            if subsection_dir.is_dir():
                subsections.append(self._create_subsect_config_fromdir(subsection_dir))

        section_config = {
            "title": self._create_title_fromdir(section_dir_path.name),
            "description": self._read_description_file(section_dir_path),
            "subsections": subsections,
        }
        return section_config

    def create_yamlconfig_fromdir(
        self, base_dir: str
    ) -> Tuple[Dict[str, Union[str, List[Dict]]], Path]:
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
        base_dir_path = Path(base_dir)

        # Generate the YAML config
        yaml_config = {
            "report": {
                "title": self._create_title_fromdir(base_dir_path.name),
                "description": self._read_description_file(base_dir_path),
                "graphical_abstract": "",
                "logo": "",
            },
            "sections": [],
        }

        # Sort sections by their number prefix
        sorted_sections = self._sort_paths_by_numprefix(list(base_dir_path.iterdir()))

        # Generate sections and subsections config
        for section_dir in sorted_sections:
            if section_dir.is_dir():
                yaml_config["sections"].append(
                    self._create_sect_config_fromdir(section_dir)
                )

        return yaml_config, base_dir_path

    def initialize_report(self, config: dict) -> tuple[r.Report, dict]:
        """
        Extracts report metadata from a YAML config file and returns a Report object and the raw metadata.

        Parameters
        ----------
        config : dict
            The report metadata obtained from a YAML config file.

        Returns
        -------
        report, config : tuple[Report, dict]
            A tuple containing the Report object created from the YAML config file and the raw metadata dictionary.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        ValueError
            If the YAML config file is corrupted or contains missing/invalid values.
        """
        # Create a Report object from metadata
        report = r.Report(
            title=config["report"]["title"],
            logger=self.logger,
            sections=[],
            description=config["report"].get("description"),
            graphical_abstract=config["report"].get("graphical_abstract"),
            logo=config["report"].get("logo"),
        )

        # Create sections and subsections
        for section_data in config.get("sections", []):
            section = self._create_section(section_data)
            report.sections.append(section)

        self.logger.info(
            f"Report '{report.title}' initialized with {len(report.sections)} sections."
        )
        return report, config

    def _create_section(self, section_data: dict) -> r.Section:
        """
        Creates a Section object from a dictionary of section data.

        Parameters
        ----------
        section_data : dict
            A dictionary containing section metadata.

        Returns
        -------
        section : Section
            A Section object populated with the provided metadata.
        """
        # Initialize the Section object
        section = r.Section(
            title=section_data["title"],
            subsections=[],
            description=section_data.get("description"),
        )

        # Create subsections
        for subsection_data in section_data.get("subsections", []):
            subsection = self._create_subsection(subsection_data)
            section.subsections.append(subsection)

        return section

    def _create_subsection(self, subsection_data: dict) -> r.Subsection:
        """
        Creates a Subsection object from a dictionary of subsection data.

        Parameters
        ----------
        subsection_data : dict
            A dictionary containing subsection metadata.

        Returns
        -------
        subsection : Subsection
            A Subsection object populated with the provided metadata.
        """
        # Initialize the Subsection object
        subsection = r.Subsection(
            title=subsection_data["title"],
            components=[],
            description=subsection_data.get("description"),
        )

        # Create components
        for component_data in subsection_data.get("components", []):
            component = self._create_component(component_data)
            subsection.components.append(component)

        return subsection

    def _create_component(self, component_data: dict) -> r.Component:
        """
        Creates a Component object from a dictionary of component data.

        Parameters
        ----------
        component_data : dict
            A dictionary containing component metadata.

        Returns
        -------
        Component
            A Component object (Plot, DataFrame, or Markdown) populated with the provided metadata.
        """
        # Determine the component type
        component_type = assert_enum_value(
            r.ComponentType, component_data["component_type"], self.logger
        )

        # Dispatch to the corresponding creation method
        if component_type == r.ComponentType.PLOT:
            return self._create_plot_component(component_data)
        elif component_type == r.ComponentType.DATAFRAME:
            return self._create_dataframe_component(component_data)
        elif component_type == r.ComponentType.MARKDOWN:
            return self._create_markdown_component(component_data)
        elif component_type == r.ComponentType.HTML:
            return self._create_html_component(component_data)
        elif component_type == r.ComponentType.APICALL:
            return self._create_apicall_component(component_data)
        elif component_type == r.ComponentType.CHATBOT:
            return self._create_chatbot_component(component_data)

    def _create_plot_component(self, component_data: dict) -> r.Plot:
        """
        Creates a Plot component.

        Parameters
        ----------
        component_data : dict
            A dictionary containing plot component metadata.

        Returns
        -------
        Plot
            A Plot object populated with the provided metadata.
        """
        # Validate enum fields
        plot_type = assert_enum_value(
            r.PlotType, component_data["plot_type"], self.logger
        )
        csv_network_format = (
            assert_enum_value(
                r.CSVNetworkFormat,
                component_data.get("csv_network_format", ""),
                self.logger,
            )
            if component_data.get("csv_network_format")
            else None
        )

        return r.Plot(
            title=component_data["title"],
            logger=self.logger,
            file_path=component_data["file_path"],
            plot_type=plot_type,
            csv_network_format=csv_network_format,
            caption=component_data.get("caption"),
        )

    def _create_dataframe_component(self, component_data: dict) -> r.DataFrame:
        """
        Creates a DataFrame component.

        Parameters
        ----------
        component_data : dict
            A dictionary containing dataframe component metadata.

        Returns
        -------
        DataFrame
            A DataFrame object populated with the provided metadata.
        """
        # Validate enum field and return dataframe
        file_format = assert_enum_value(
            r.DataFrameFormat, component_data["file_format"], self.logger
        )

        return r.DataFrame(
            title=component_data["title"],
            logger=self.logger,
            file_path=component_data["file_path"],
            file_format=file_format,
            delimiter=component_data.get("delimiter"),
            caption=component_data.get("caption"),
        )

    def _create_markdown_component(self, component_data: dict) -> r.Markdown:
        """
        Creates a Markdown component.

        Parameters
        ----------
        component_data : dict
            A dictionary containing markdown component metadata.

        Returns
        -------
        Markdown
            A Markdown object populated with the provided metadata.
        """
        return r.Markdown(
            title=component_data["title"],
            logger=self.logger,
            file_path=component_data["file_path"],
            caption=component_data.get("caption"),
        )

    def _create_html_component(self, component_data: dict) -> r.Html:
        """
        Creates an Html component.

        Parameters
        ----------
        component_data : dict
            A dictionary containing hml component metadata.

        Returns
        -------
        Html
            An Html object populated with the provided metadata.
        """
        return r.Html(
            title=component_data["title"],
            logger=self.logger,
            file_path=component_data["file_path"],
            caption=component_data.get("caption"),
        )

    def _create_apicall_component(self, component_data: dict) -> r.APICall:
        """
        Creates an APICall component.

        Parameters
        ----------
        component_data : dict
            A dictionary containing apicall component metadata.

        Returns
        -------
        APICall
            An APICall object populated with the provided metadata.
        """
        return r.APICall(
            title=component_data["title"],
            logger=self.logger,
            api_url=component_data["api_url"],
            caption=component_data.get("caption"),
            headers=component_data.get("headers"),
            params=component_data.get("params"),
        )

    def _create_chatbot_component(self, component_data: dict) -> r.ChatBot:
        """
        Creates a ChatBot component.

        Parameters
        ----------
        component_data : dict
            A dictionary containing apicall component metadata.

        Returns
        -------
        APICall
            A chatbot object populated with the provided metadata.
        """
        return r.ChatBot(
            title=component_data["title"],
            logger=self.logger,
            api_url=component_data["api_url"],
            model=component_data["model"],
            caption=component_data.get("caption"),
            headers=component_data.get("headers"),
            params=component_data.get("params"),
        )
