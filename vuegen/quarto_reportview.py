import os
import subprocess
import report as r
from typing import List
from utils import create_folder

class QuartoReportView(r.ReportView):
    """
    A ReportView subclass for generating Quarto reports.
    """

    BASE_DIR = 'quarto_report'
    STATIC_FILES_DIR = os.path.join(BASE_DIR, 'static')

    def __init__(self, report: r.Report, report_type: r.ReportType):
        super().__init__(report = report, report_type = report_type)

    def generate_report(self, output_dir: str = BASE_DIR, static_dir: str = STATIC_FILES_DIR) -> None:
        """
        Generates the qmd file of the quarto report. It creates code for rendering each section and its subsections with all components.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the generated report files will be saved (default is BASE_DIR).
        static_dir : str, optional
            The folder where the static files will be saved (default is STATIC_FILES_DIR).
        """
        self.report.logger.debug(f"Generating '{self.report_type}' report in directory: '{output_dir}'")

        # Create the output folder
        if create_folder(output_dir):
            self.report.logger.debug(f"Created output directory: '{output_dir}'")
        else:
            self.report.logger.debug(f"Output directory already existed: '{output_dir}'")

        # Create the static folder
        if create_folder(static_dir):
            self.report.logger.info(f"Created output directory for static content: '{static_dir}'")
        else:
            self.report.logger.info(f"Output directory for static content already existed: '{static_dir}'")
        
        try:
            # Create variable to check if the report is static or revealjs
            is_report_static = self.report_type in {r.ReportType.PDF, r.ReportType.DOCX, r.ReportType.ODT, r.ReportType.PPTX}
            is_report_revealjs = self.report_type == r.ReportType.REVEALJS
            
            # Define the YAML header for the quarto report
            yaml_header = self._create_yaml_header()
            
            # Create qmd content and imports for the report 
            qmd_content = []
            report_imports = []

            # Add description of the report
            if self.report.description:
                qmd_content.append(f'''{self.report.description}''')

            # If available add the graphical abstract
            if self.report.graphical_abstract:
                qmd_content.append(self._generate_image_content(self.report.graphical_abstract))
            # Add the sections and subsections to the report
            self.report.logger.info("Starting to generate sections for the report.")
            for section in self.report.sections:
                self.report.logger.debug(f"Processing section: '{section.title}' - {len(section.subsections)} subsection(s)")
                # Add section header and description
                qmd_content.append(f'# {section.title}')
                if section.description:
                    qmd_content.append(f'''{section.description}\n''')
                
                if section.subsections:
                    # Iterate through subsections and integrate them into the section file
                    for subsection in section.subsections:
                        self.report.logger.debug(f"Processing subsection: '{subsection.title}' - {len(subsection.components)} component(s)")                    
                        # Generate content for the subsection
                        subsection_content, subsection_imports = self._generate_subsection(subsection, is_report_static, is_report_revealjs)
                        qmd_content.extend(subsection_content)
                        report_imports.extend(subsection_imports) 
            
            # Flatten the subsection_imports into a single list
            flattened_report_imports = [imp for sublist in report_imports for imp in sublist]
            
            # Remove duplicated imports
            report_unique_imports = list(set(flattened_report_imports))

            # Format imports
            report_formatted_imports = "\n".join(report_unique_imports)
            
            # Write the navigation and general content to a Python file
            with open(os.path.join(output_dir, f"{self.BASE_DIR}.qmd"), 'w') as quarto_report:
                quarto_report.write(yaml_header)
                quarto_report.write(f"""\n```{{python}}
#| label: 'Imports'
{report_formatted_imports}
```\n\n""")
                quarto_report.write("\n".join(qmd_content))
                self.report.logger.info(f"Created qmd script to render the app: {self.BASE_DIR}.qmd")
        
        except Exception as e:
            self.report.logger.error(f"An error occurred while generating the report: {str(e)}")
            raise

    def run_report(self, output_dir: str = BASE_DIR) -> None:
        """
        Runs the generated quarto report.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the report was generated (default is 'sections').
        """
        try:
            subprocess.run(["quarto", "render", os.path.join(output_dir, f"{self.BASE_DIR}.qmd")], check=True)
            self.report.logger.info(f"'{self.report.title}' '{self.report_type}' report rendered")
        except subprocess.CalledProcessError as e:
            self.report.logger.error(f"Error running '{self.report.title}' {self.report_type} report: {str(e)}")
            raise

    def _create_yaml_header(self) -> str:
        """
        Creates a YAML header for the Quarto report based on the specified eport type and output format.

        Returns
        -------
        str
            A formatted YAML header string customized for the specified output format.
        """
        # Base YAML header with title
        yaml_header = f"""---
title: {self.report.title}
fig-align: center
execute:
  echo: false
  output: asis
format:"""

        # Define format-specific YAML configurations
        format_configs = {
            r.ReportType.HTML: """
  html:
    toc: true
    toc-location: left
    toc-depth: 3
    page-layout: full
    self-contained: true""",
            r.ReportType.PDF: """
  pdf:
    toc: false""",
            r.ReportType.DOCX: """
  docx:
    toc: false""",
            r.ReportType.ODT: """
  odt:
    toc: false""",
            r.ReportType.REVEALJS: """
  revealjs:
    toc: false
    smaller: true
    controls: true
    navigation-mode: vertical
    controls-layout: bottom-right
    output-file: quarto_report_revealjs.html""",
            r.ReportType.PPTX: """
  pptx:
    toc: false
    output: true""",
r.ReportType.JUPYTER: """
  jupyter:
    kernel: python3"""
        }

        # Create a key based on the report type and format
        key = self.report_type

        # Retrieve the configuration if it exists, or raise an error
        if key in format_configs:
            config = format_configs[key]
        else:
            raise ValueError(f"Unsupported report type: {self.report_type}")

        # Add the specific configuration to the YAML header
        yaml_header += config
        yaml_header += "\n---\n"

        return yaml_header

    def _generate_subsection(self, subsection, is_report_static, is_report_revealjs) -> tuple[List[str], List[str]]:
        """
        Generate code to render components (plots, dataframes, markdown) in the given subsection, 
        creating imports and content for the subsection based on the component type.

        Parameters
        ----------
        subsection : Subsection
            The subsection containing the components.
        is_report_static : bool
            A boolean indicating whether the report is static or interactive.
        is_report_revealjs : bool
            A boolean indicating whether the report is in revealjs format.
        Returns
        -------
        tuple : (List[str], List[str])
            - list of subsection content lines (List[str])
            - list of imports for the subsection (List[str])
        """
        subsection_content = []
        subsection_imports = []

        # Add subsection header and description
        subsection_content.append(f'## {subsection.title}')
        if subsection.description: 
            subsection_content.append(f'''{subsection.description}\n''')

        if is_report_revealjs:
            subsection_content.append(f'::: {{.panel-tabset}}\n')

        for component in subsection.components:
            component_imports = self._generate_component_imports(component)
            subsection_imports.append(component_imports)

            if component.component_type == r.ComponentType.PLOT:
                subsection_content.extend(self._generate_plot_content(component, is_report_static))
            
            elif component.component_type == r.ComponentType.DATAFRAME:
                subsection_content.extend(self._generate_dataframe_content(component, is_report_static))
            
            elif component.component_type == r.ComponentType.MARKDOWN:
                subsection_content.extend(self._generate_markdown_content(component))
            else:
                self.report.logger.warning(f"Unsupported component type '{component.component_type}' in subsection: {subsection.title}")
        
        if is_report_revealjs:
            subsection_content.append(':::\n')

        self.report.logger.info(f"Generated content and imports for subsection: '{subsection.title}'")
        return subsection_content, subsection_imports

    def _generate_plot_content(self, plot, is_report_static, static_dir: str = STATIC_FILES_DIR) -> List[str]:
        """
        Generate content for a plot component based on the report type.

        Parameters
        ----------
        plot : Plot
            The plot component to generate content for.
        static_dir : str, optional
            The folder where the static files will be saved (default is STATIC_FILES_DIR).
        
        Returns
        -------
        list : List[str]
            The list of content lines for the plot.
        """
        plot_content = []
        # Add title
        plot_content.append(f'### {plot.title}')
        
        # Define plot path
        if is_report_static:
            static_plot_path  = os.path.join(static_dir, f"{plot.title.replace(' ', '_')}.png")
        else:
            html_plot_file  = os.path.join(static_dir, f"{plot.title.replace(' ', '_')}.html")

        # Add content for the different plot types
        try:
            if plot.plot_type == r.PlotType.STATIC:
                plot_content.append(self._generate_image_content(plot.file_path, width=950))
            elif plot.plot_type == r.PlotType.PLOTLY:
                plot_content.append(self._generate_plot_code(plot))
                if is_report_static:
                    plot_content.append(f"""fig_plotly.write_image("{os.path.join("..", static_plot_path)}")\n```\n""")
                    plot_content.append(self._generate_image_content(static_plot_path))
                else:
                    plot_content.append(f"""fig_plotly.show()\n```\n""")
            elif plot.plot_type == r.PlotType.ALTAIR:
                plot_content.append(self._generate_plot_code(plot))
                if is_report_static:
                    plot_content.append(f"""fig_altair.save("{os.path.join("..", static_plot_path)}")\n```\n""")
                    plot_content.append(self._generate_image_content(static_plot_path))
                else:
                    plot_content.append(f"""fig_altair\n```\n""")
            elif plot.plot_type == r.PlotType.INTERACTIVE_NETWORK:
                network_data = plot.read_network()
                if is_report_static:
                    plot.save_netwrok_image(G, static_plot_path, "png")
                    plot_content.append(self._generate_image_content(static_plot_path))
                else:
                    if isinstance(network_data, str) and network_data.endswith('.html'):
                        # If network_data is the path to an HTML file, just visualize it
                        html_plot_file = network_data
                    else:
                        num_nodes = network_data.number_of_nodes()
                        num_edges = network_data.number_of_edges()
                        plot_content.append(f'**Number of nodes:** {num_nodes}\n')
                        plot_content.append(f'**Number of edges:** {num_edges}\n')
                        # Get the Network object
                        net = plot.create_and_save_pyvis_network(network_data, html_plot_file)

                    plot_content.append(self._generate_plot_code(plot, html_plot_file))
            else:
                    self.report.logger.warning(f"Unsupported plot type: {plot.plot_type}")
        except Exception as e:
            self.report.logger.error(f"Error generating content for '{plot.plot_type}' plot '{plot.id}' '{plot.title}': {str(e)}")
            raise
        
        # Add caption if available
        if plot.caption:
            plot_content.append(f'>{plot.caption}\n')

        self.report.logger.info(f"Successfully generated content for plot: '{plot.title}'")
        return plot_content

    def _generate_plot_code(self, plot, output_file = "") -> str:
        """
        Create the plot code based on its visualization tool. 

        Parameters
        ----------
        plot : Plot
            The plot component to generate the code template for.
        output_file: str, optional
            The output html file name to be displayed with a pyvis plot.
        Returns
        -------
        str
            The generated plot code as a string.
        """
        # Start with the common data loading code
        plot_code = f"""```{{python}}
#| label: '{plot.title}'
#| fig-cap: ""
with open('{os.path.join("..", plot.file_path)}', 'r') as plot_file:
    plot_data = plot_file.read()
    """
        # Add specific code for each visualization tool
        if plot.plot_type == r.PlotType.PLOTLY:
            plot_code += """fig_plotly = pio.from_json(plot_data)
fig_plotly.update_layout(width=950, height=500)
    """
        elif plot.plot_type == r.PlotType.ALTAIR:
            plot_code += """fig_altair = alt.Chart.from_json(plot_data).properties(width=900, height=400)"""
        elif plot.plot_type == r.PlotType.INTERACTIVE_NETWORK:
            plot_code = f"""<div style="text-align: center;">
<iframe src="{os.path.join("..", output_file)}" alt="{plot.title} plot" width="800px" height="630px"></iframe>
</div>\n"""
        return plot_code

    def _generate_dataframe_content(self, dataframe, is_report_static) -> List[str]:
        """
        Generate content for a DataFrame component based on the report type.

        Parameters
        ----------
        dataframe : DataFrame
            The dataframe component to add to content.
        is_report_static : bool
            A boolean indicating whether the report is static or interactive.
        
        Returns
        -------
        list : List[str]
            The list of content lines for the DataFrame.
        """
        datframe_content = []
        # Add title
        datframe_content.append(f'### {dataframe.title}')

        # Append header for DataFrame loading
        datframe_content.append(f"""```{{python}}
#| label: '{dataframe.title}'
#| fig-cap: ""
""")
        try:
            if dataframe.file_format == r.DataFrameFormat.CSV:
                if dataframe.delimiter:
                    datframe_content.append(f"""df = pd.read_csv('{os.path.join("..", dataframe.file_path)}', delimiter='{dataframe.delimiter}')""")
                    datframe_content.extend(self._show_dataframe(dataframe, is_report_static))
                else:
                    datframe_content.append(f"""df = pd.read_csv('{os.path.join("..", dataframe.file_path)}')""")
                    datframe_content.extend(self._show_dataframe(dataframe, is_report_static))
            elif dataframe.file_format == r.DataFrameFormat.PARQUET:
                datframe_content.append(f"""df = pd.read_parquet('{os.path.join("..", dataframe.file_path)}')""")
                datframe_content.extend(self._show_dataframe(dataframe, is_report_static))
            elif dataframe.file_format == r.DataFrameFormat.TXT:
                datframe_content.append(f"""df = pd.read_csv('{os.path.join("..", dataframe.file_path)}', sep='\\t')""")
                datframe_content.extend(self._show_dataframe(dataframe, is_report_static))
            elif dataframe.file_format == r.DataFrameFormat.EXCEL:
                datframe_content.append(f"""df = pd.read_excel('{os.path.join("..", dataframe.file_path)}')""")
                datframe_content.extend(self._show_dataframe(dataframe, is_report_static))
            else:
                self.report.logger.error(f"Unsupported DataFrame file format: {dataframe.file_format}")
                raise ValueError(f"Unsupported DataFrame file format: {dataframe.file_format}")
        
        except Exception as e:
            self.report.logger.error(f"Error generating content for DataFrame: {dataframe.title}. Error: {str(e)}")
            raise

        # Add caption if available
        if dataframe.caption:
            datframe_content.append(f'>{dataframe.caption}\n')

        self.report.logger.info(f"Successfully generated content for DataFrame: '{dataframe.title}'")
        return datframe_content

    def _generate_markdown_content(self, markdown) -> List[str]:
        """
        Adds markdown content to the report.

        Parameters
        ----------
        markdown : Markdown
            The markdown component to add to content.
        
        Returns
        -------
        list : List[str]
            The list of content lines for the markdown.
        """            
        markdown_content = []
        # Add title
        markdown_content.append(f'### {markdown.title}')
        
        try:
            markdown_content.append(f"""```{{python}}
#| label: '{markdown.title}'
#| fig-cap: ""
with open('{os.path.join("..", markdown.file_path)}', 'r') as markdown_file:
    markdown_content = markdown_file.read()
display.Markdown(markdown_content)
```\n""")
        except Exception as e:
            self.report.logger.error(f"Error generating content for Markdown: {markdown.title}. Error: {str(e)}")
            raise
        
        # Add caption if available
        if markdown.caption:
            markdown_content.append(f'>{markdown.caption}\n')
        
        self.report.logger.info(f"Successfully generated content for Markdown: '{markdown.title}'")
        return markdown_content

    def _generate_image_content(self, image_path: str, alt_text: str = "", width: int = 650, height: int = 400) -> str:
        """
        Adds an image to the content list in a centered format with a specified width.

        Parameters
        ----------
        image_path : str
            Path to the image file.
        width : int, optional
            Width of the image in pixels (default is 650).
        height : int, optional
            Height of the image in pixels (default is 500).
        alt_text : str, optional
            Alternative text for the image (default is an empty string).
        
        Returns
        -------
        str
            The formatted image content.
        """
        return f"""
![{alt_text}]({os.path.join('..', image_path)}){{ width={width}px height={height}px fig-align="center"}}\n"""
    
    def _show_dataframe(self, dataframe, is_report_static, static_dir: str = STATIC_FILES_DIR) -> List[str]:
        """
        Appends either a static image or an interactive representation of a DataFrame to the content list.

        Parameters
        ----------
        dataframe : DataFrame
            The DataFrame object containing the data to display.
        is_report_static : bool
            Determines if the report is in a static format (e.g., PDF) or interactive (e.g., HTML).
        static_dir : str, optional
            The folder where the static files will be saved (default is STATIC_FILES_DIR).
        
        Returns
        -------
        list : List[str]
            The list of content lines for the DataFrame.
        """
        dataframe_content = []
        if is_report_static:
            # Generate path for the DataFrame image
            df_image = os.path.join(static_dir, f"{dataframe.title.replace(' ', '_')}.png")
            dataframe_content.append(f"dfi.export(df, '{os.path.join('..', df_image)}', max_rows=10, max_cols=5)\n```\n")
            # Use helper method to add centered image content
            dataframe_content.append(self._generate_image_content(df_image))
        else:
            # Append code to display the DataFrame interactively
            dataframe_content.append(f"""show(df, classes="display nowrap compact", lengthMenu=[3, 5, 10])\n```\n""")
        
        return dataframe_content
    
    def _generate_component_imports(self, component: r.Component) -> List[str]:
        """
        Generate necessary imports for a component of the report.

        Parameters
        ----------
        component : r.Component
            The component for which to generate the required imports. The component can be of type:
            - PLOT
            - DATAFRAME
            - MARKDOWN
        
        Returns
        -------
        list : List[str]
            A list of import statements for the component.
        """
        # Dictionary to hold the imports for each component type
        components_imports = {
            'plot': {
                r.PlotType.ALTAIR: ['import altair as alt'],
                r.PlotType.PLOTLY: ['import plotly.io as pio']
            },
            'dataframe': ['import pandas as pd', 'from itables import show', 'import dataframe_image as dfi'],
            'markdown': ['import IPython.display as display']
        }

        # Iterate over sections and subsections to determine needed imports 
        component_type = component.component_type
        component_imports = []

        # Add relevant imports based on component type and visualization tool
        if component_type == r.ComponentType.PLOT:
            plot_type = getattr(component, 'plot_type', None)
            if plot_type in components_imports['plot']:
                component_imports.extend(components_imports['plot'][plot_type])
        elif component_type == r.ComponentType.DATAFRAME:
            component_imports.extend(components_imports['dataframe'])
        elif component_type == r.ComponentType.MARKDOWN:
            component_imports.extend(components_imports['markdown'])

        # Return the list of import statements
        return component_imports
