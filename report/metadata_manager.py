import yaml
from report import Report, Section, Subsection, Plot, PlotType, VisualizationTool
from abc import ABC, abstractmethod

class MetadataManager(ABC):
    """
    Abstract base class for managing metadata from various sources (e.g., YAML, JSON, etc).
    
    Methods
    -------
    load_report_metadata(file_path)
        Load and parse the metadata from a specified file and return a Report object.
    """
    
    @abstractmethod
    def load_report_metadata(self, file_path: str) -> Report:
        pass

class YAMLMetadataManager(MetadataManager):
    """
    Class for handling metadata from YAML files.
    """
    def load_report_metadata(self, file_path: str) -> Report:
        """
        Load and parse the metadata from a YAML file and return a Report object.

        Parameters
        ----------
        file_path : str
            The path to the YAML file containing the report metadata.
        
        Returns
        -------
        Report
            A Report object created from the metadata in the YAML file.
        """
        with open(file_path, 'r') as file:
            metadata = yaml.safe_load(file)
        
        # Create a Report object
        report = Report(
            identifier=metadata['report']['identifier'],
            name=metadata['report']['name'],
            title=metadata['report'].get('title'),
            description=metadata['report'].get('description'),
            graphical_abstract=metadata['report'].get('graphical_abstract'),
            logo=metadata['report'].get('logo'),
            sections=[]
        )

        # Create Sections
        for section_data in metadata['sections']:
            section = Section(
                identifier=section_data['identifier'],
                name=section_data['name'],
                title=section_data.get('title'),
                description=section_data.get('description'),
                subsections=[]
            )
            
            # Create Subsections
            for subsection_data in section_data['subsections']:
                subsection = Subsection(
                    identifier=subsection_data['identifier'],
                    name=subsection_data['name'],
                    title=subsection_data.get('title'),
                    description=subsection_data.get('description'),
                    plots=[]
                )
                
                # Create Plots
                for plot_data in subsection_data['plots']:
                    plot_file_path = plot_data['file_path']

                    # Convert plot_type from string to PlotType Enum
                    plot_type = PlotType[plot_data['plot_type'].upper()]

                    # Convert visualization_tool from string to VisualizationTool Enum, if provided
                    visualization_tool = (VisualizationTool[plot_data['visualization_tool'].upper()]
                                          if plot_data.get('visualization_tool') else None)
                    
                    # Create Plot object
                    plot = Plot(
                        identifier=plot_data['identifier'],
                        name=plot_data['name'],
                        plot_type=plot_type,
                        file_path=plot_file_path,
                        visualization_tool=visualization_tool,
                        title=plot_data.get('title'),
                        caption=plot_data.get('caption'),
                        csv_network_format=plot_data.get('csv_network_format')
                        )
                    subsection.plots.append(plot)
                
                section.subsections.append(subsection)
            
            report.sections.append(section)

        return report