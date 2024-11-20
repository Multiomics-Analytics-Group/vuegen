import os
import yaml
import report as r
import logging
from utils import get_logger, assert_enum_value

class MetadataManager:
    """
    Class for handling metadata of reports from YAML files and creating report objects.
    """

    def load_report_metadata(self, file_path: str) -> tuple[r.Report, dict]:
        """
        Loads metadata from a YAML file, parses it, and returns a Report object and the raw metadata.

        Parameters
        ----------
        file_path : str
            The path to the YAML file containing the report metadata.

        Returns
        -------
        report, metadata : tuple[Report, dict]
            A tuple containing the Report object created from the YAML metadata and the raw metadata dictionary.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        ValueError
            If the YAML file is corrupted or contains missing/invalid values.
        """
        # Check the existence of the file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The config file at {file_path} was not found.")

        # Load the YAML configuration file
        with open(file_path, 'r') as file:
            try:
                metadata = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                raise ValueError(f"Error parsing YAML file: {exc}")
        
        # Define suffix f"or logger object based on report type and report name
        logger_suffix = f"{metadata['report'].get('report_type')}_report_{metadata['report'].get('name')}"

        # Create a Report object from metadata
        report = r.Report(
            id=metadata['report']['id'],
            name=metadata['report']['name'],
            sections=[],
            title=metadata['report'].get('title'),
            description=metadata['report'].get('description'),
            graphical_abstract=metadata['report'].get('graphical_abstract'),
            logo=metadata['report'].get('logo'),
            logger = get_logger(logger_suffix)
        )

        # Create sections and subsections
        for section_data in metadata.get('sections', []):
            section = self._create_section(section_data, report.logger)
            report.sections.append(section)

        report.logger.info(f"Report '{report.name}' initialized with {len(report.sections)} sections.")
        return report, metadata

    def _create_section(self, section_data: dict, logger: logging.Logger) -> r.Section:
        """
        Creates a Section object from a dictionary of section data.

        Parameters
        ----------
        section_data : dict
            A dictionary containing section metadata.
        logger : logging.Logger
            A logger object to track warnings, errors, and info messages.

        Returns
        -------
        section : Section
            A Section object populated with the provided metadata.
        """
        # Initialize the Section object
        section = r.Section(
            id=section_data['id'],
            name=section_data['name'],
            title=section_data.get('title'),
            description=section_data.get('description'),
            subsections=[]
        )

        # Create subsections
        for subsection_data in section_data.get('subsections', []):
            subsection = self._create_subsection(subsection_data, logger)
            section.subsections.append(subsection)
        
        return section

    def _create_subsection(self, subsection_data: dict, logger: logging.Logger) -> r.Subsection:
        """
        Creates a Subsection object from a dictionary of subsection data.

        Parameters
        ----------
        subsection_data : dict
            A dictionary containing subsection metadata.
        logger : logging.Logger
            A logger object to track warnings, errors, and info messages.

        Returns
        -------
        subsection : Subsection
            A Subsection object populated with the provided metadata.
        """
        # Initialize the Subsection object
        subsection = r.Subsection(
            id=subsection_data['id'],
            name=subsection_data['name'],
            title=subsection_data.get('title'),
            description=subsection_data.get('description'),
            components=[]
        )

        # Create components
        for component_data in subsection_data.get('components', []):
            component = self._create_component(component_data, logger)
            subsection.components.append(component)

        return subsection

    def _create_component(self, component_data: dict, logger: logging.Logger) -> r.Component:
        """
        Creates a Component object from a dictionary of component data.

        Parameters
        ----------
        component_data : dict
            A dictionary containing component metadata.
        logger : logging.Logger
            A logger object to track warnings, errors, and info messages.

        Returns
        -------
        Component
            A Component object (Plot, DataFrame, or Markdown) populated with the provided metadata.
        """
        # Determine the component type
        component_type = assert_enum_value(r.ComponentType, component_data['component_type'], logger)

        # Dispatch to the corresponding creation method
        if component_type == r.ComponentType.PLOT:
            return self._create_plot_component(component_data, logger)
        elif component_type == r.ComponentType.DATAFRAME:
            return self._create_dataframe_component(component_data, logger)
        elif component_type == r.ComponentType.MARKDOWN:
            return self._create_markdown_component(component_data, logger)

    def _create_plot_component(self, component_data: dict, logger: logging.Logger) -> r.Plot:
        """
        Creates a Plot component.

        Parameters
        ----------
        component_data : dict
            A dictionary containing plot component metadata.
        logger : logging.Logger
            A logger object to track warnings, errors, and info messages.

        Returns
        -------
        Plot
            A Plot object populated with the provided metadata.
        """
        # Validate enum fields
        plot_type = assert_enum_value(r.PlotType, component_data['plot_type'], logger)
        int_visualization_tool = (assert_enum_value(r.IntVisualizationTool, component_data.get('int_visualization_tool', ''), logger) 
                                  if component_data.get('int_visualization_tool') else None)
        csv_network_format = (assert_enum_value(r.CSVNetworkFormat, component_data.get('csv_network_format', ''), logger) 
                              if component_data.get('csv_network_format') else None)

        # Return the constructed Plot object
        return r.Plot(
            id=component_data['id'],
            name=component_data['name'],
            file_path=component_data['file_path'],
            plot_type=plot_type,
            int_visualization_tool=int_visualization_tool,
            title=component_data.get('title'),
            caption=component_data.get('caption'),
            csv_network_format=csv_network_format,
            logger = logger
        )

    def _create_dataframe_component(self, component_data: dict, logger: logging.Logger) -> r.DataFrame:
        """
        Creates a DataFrame component.

        Parameters
        ----------
        component_data : dict
            A dictionary containing dataframe component metadata.
        logger : logging.Logger
            A logger object to track warnings, errors, and info messages.

        Returns
        -------
        DataFrame
            A DataFrame object populated with the provided metadata.
        """        
        # Validate enum field and return dataframe
        file_format = assert_enum_value(r.DataFrameFormat, component_data['file_format'], logger)
        return r.DataFrame(
            id=component_data['id'],
            name=component_data['name'],
            file_path=component_data['file_path'],
            file_format=file_format,
            delimiter=component_data.get('delimiter'),
            title=component_data.get('title'),
            caption=component_data.get('caption'),
            logger = logger
        )

    def _create_markdown_component(self, component_data: dict, logger: logging.Logger) -> r.Markdown:
        """
        Creates a Markdown component.

        Parameters
        ----------
        component_data : dict
            A dictionary containing markdown component metadata.
        logger : logging.Logger
            A logger object to track warnings, errors, and info messages.

        Returns
        -------
        Markdown
            A Markdown object populated with the provided metadata.
        """
        return r.Markdown(
            id=component_data['id'],
            name=component_data['name'],
            file_path=component_data['file_path'],
            title=component_data.get('title'),
            caption=component_data.get('caption'),
            logger = logger
        )