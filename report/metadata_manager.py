import yaml
import report as r

class MetadataManager():
    """
    Class for handling metadata of reports from YAML files.
    """
    def load_report_metadata(self, file_path: str) -> r.Report:
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
        report = r.Report(
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
            section = r.Section(
                identifier=section_data['identifier'],
                name=section_data['name'],
                title=section_data.get('title'),
                description=section_data.get('description'),
                subsections=[]
            )
            
            # Create Subsections
            for subsection_data in section_data['subsections']:
                subsection = r.Subsection(
                    identifier=subsection_data['identifier'],
                    name=subsection_data['name'],
                    title=subsection_data.get('title'),
                    description=subsection_data.get('description'),
                    components=[]
                )
                
                # Create Components
                for component_data in subsection_data['components']:
                    component_type = r.ComponentType[component_data['component_type'].upper()]
                    file_path = component_data['file_path']
                    identifier = component_data['identifier']
                    name = component_data['name']
                    title = component_data.get('title')
                    caption = component_data.get('caption')

                    # Define a component based on its type
                    if component_type == r.ComponentType.PLOT:
                        plot_type = r.PlotType[component_data['plot_type'].upper()]
                        visualization_tool = (r.VisualizationTool[component_data['visualization_tool'].upper()]
                                              if component_data.get('visualization_tool') else None)
                        csv_network_format = (r.CSVNetworkFormat[component_data['csv_network_format'].upper()]
                                              if component_data.get('csv_network_format') else None)
                        # Create a Plot component
                        component = r.Plot(
                            identifier=identifier,
                            name=name,
                            file_path=file_path,
                            plot_type=plot_type,
                            visualization_tool=visualization_tool,
                            title=title,
                            caption=caption,
                            csv_network_format=csv_network_format
                        )

                    elif component_type == r.ComponentType.DATAFRAME:
                        file_format = r.DataFrameFormat[component_data['file_format'].upper()]
                        delimiter = component_data.get('delimiter')
                        # Create a DataFrame component
                        component = r.DataFrame(
                            identifier=identifier,
                            name=name,
                            file_path=file_path,
                            file_format=file_format,
                            delimiter=delimiter,
                            title=title,
                            caption=caption
                        )

                    elif component_type == r.ComponentType.MARKDOWN:
                        # Create a Markdown component
                        component = r.Markdown(
                            identifier=identifier,
                            name=name,
                            file_path=file_path,
                            component_type=component_type,
                            title=title,
                            caption=caption
                        )

                    subsection.components.append(component)
                
                section.subsections.append(subsection)
            
            report.sections.append(section)

        return report, metadata