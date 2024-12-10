import os
import report as r
from pathlib import Path
from typing import Dict, List, Union, Tuple
from utils import get_logger, assert_enum_value

class ConfigManager:
    """
    Class for handling metadata of reports from YAML config file and creating report objects.
    """
    def __init__(self, logger=None):
        """
        Initializes the ConfigManager with a logger.

        Parameters
        ----------
        logger : logging.Logger, optional
            A logger instance for the class. If not provided, a default logger will be created.
        """
        self.logger = logger or get_logger("report")

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
            title = config['report']['title'],
            logger = self.logger,
            sections = [],
            description = config['report'].get('description'),
            graphical_abstract = config['report'].get('graphical_abstract'),
            logo = config['report'].get('logo')
        )

        # Create sections and subsections
        for section_data in config.get('sections', []):
            section = self._create_section(section_data)
            report.sections.append(section)

        self.logger.info(f"Report '{report.title}' initialized with {len(report.sections)} sections.")
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
            title = section_data['title'],
            subsections = [],
            description = section_data.get('description')
        )

        # Create subsections
        for subsection_data in section_data.get('subsections', []):
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
            title = subsection_data['title'],
            components = [],
            description = subsection_data.get('description')
        )

        # Create components
        for component_data in subsection_data.get('components', []):
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
        component_type = assert_enum_value(r.ComponentType, component_data['component_type'], self.logger)

        # Dispatch to the corresponding creation method
        if component_type == r.ComponentType.PLOT:
            return self._create_plot_component(component_data)
        elif component_type == r.ComponentType.DATAFRAME:
            return self._create_dataframe_component(component_data)
        elif component_type == r.ComponentType.MARKDOWN:
            return self._create_markdown_component(component_data)
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
        plot_type = assert_enum_value(r.PlotType, component_data['plot_type'], self.logger)
        csv_network_format = (assert_enum_value(r.CSVNetworkFormat, component_data.get('csv_network_format', ''), self.logger) 
                              if component_data.get('csv_network_format') else None)

        return r.Plot(
            title = component_data['title'],
            logger = self.logger,
            file_path = component_data['file_path'],
            plot_type = plot_type,
            csv_network_format = csv_network_format,
            caption = component_data.get('caption')
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
        file_format = assert_enum_value(r.DataFrameFormat, component_data['file_format'], self.logger)
        
        return r.DataFrame(
            title = component_data['title'],
            logger = self.logger,
            file_path = component_data['file_path'],
            file_format = file_format,
            delimiter = component_data.get('delimiter'),
            caption = component_data.get('caption')
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
            title = component_data['title'],
            logger = self.logger,
            file_path = component_data['file_path'],
            caption = component_data.get('caption')
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
            title = component_data['title'],
            logger = self.logger,
            api_url = component_data['api_url'],
            caption = component_data.get('caption'),
            headers = component_data.get('headers'),
            params = component_data.get('params')
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
            title = component_data['title'],
            logger = self.logger,
            api_url = component_data['api_url'],
            model = component_data['model'],
            caption = component_data.get('caption'),
            headers = component_data.get('headers'),
            params = component_data.get('params')
        )