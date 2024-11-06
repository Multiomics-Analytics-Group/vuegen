import os
import subprocess
import report as r
from enum import StrEnum, auto
from typing import List, Optional

class ReportFormat(StrEnum):
    HTML = auto()
    PDF = auto()
    DOCX = auto()
    ODT = auto()
    REVEALJS = auto()
    PPTX = auto()
    JUPYTER = auto()

class QuartoReportView(r.ReportView):
    """
    A ReportView subclass for generating Quarto reports.

    Methods
    -------
    generate_report(output_dir)
        Generates the qmd file of the quarto report. It creates code for rendering each section and its subsections with all components.
    run_report(output_dir)
        Runs the generated quarto report.
    """

    def __init__(self, identifier: int, name: str, report: r.Report, report_type: r.ReportType, 
                columns: Optional[List[str]], report_format: ReportFormat):
        super().__init__(identifier, name=name, report=report, report_type = report_type, columns=columns)
        self.report_format = report_format

    def generate_report(self, output_dir: str = 'quarto_report/') -> None:
        """
        Generates the qmd file of the quarto report. It creates code for rendering each section and its subsections with all components.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the generated report files will be saved (default is 'quarto_report/').
        """
        # Create the output folder if it does not exist
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # Create variable to check if the report is static or revealjs
        is_report_static = self.report_format in {ReportFormat.PDF, ReportFormat.DOCX, ReportFormat.ODT, ReportFormat.PPTX}
        is_report_revealjs = self.report_format == ReportFormat.REVEALJS
        
        # Define the YAML header for the quarto report
        yaml_header = self._create_yaml_header()
        
        # Create qmd content for the report
        qmd_content = []
        imports_report = []

        # Add the title and description of the report
        qmd_content.append(f'''{self.report.description}\n''')

        # If available add the graphical abstract
        if self.report.graphical_abstract:
            qmd_content.append(self._generate_image_content(self.report.graphical_abstract, f"Graphical abstract for the {self.report.title} report"))
        # Add the sections and subsections to the report
        for section in self.report.sections:
            # Add section header and description
            qmd_content.append(f'# {section.title}')
            qmd_content.append(f'''{section.description}''')
            
            if section.subsections:
                # Iterate through subsections and integrate them into the section file
                for subsection in section.subsections:                    
                    # Generate content for the subsection
                    subsection_content, imports_subsection = self._generate_subsection(subsection, is_report_static, is_report_revealjs)
                    qmd_content.extend(subsection_content)
                    imports_report.extend(imports_subsection) 
        
        # Remove duplicated imports
        unique_imports = set()

        # Split each string by newlines and update the set
        for imp in imports_report:
            unique_imports.update(imp.split('\n'))

        formatted_imports = "\n".join(unique_imports)
        
        # Write the navigation and general content to a Python file
        with open(os.path.join(output_dir, "quarto_report.qmd"), 'w') as quarto_report:
            quarto_report.write(yaml_header)
            quarto_report.write(f"""```{{python}}
#| label: 'Imports'
#| echo: false
{formatted_imports}
```\n\n""")
            quarto_report.write("\n".join(qmd_content))

    def run_report(self, output_dir: str = 'quarto_report') -> None:
        """
        Runs the generated quarto report.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the report was generated (default is 'sections').
        """
        subprocess.run(["quarto", "render", os.path.join(output_dir, "quarto_report.qmd")], check=True)

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
format:"""

        # Define format-specific YAML configurations
        format_configs = {
            (r.ReportType.DOCUMENT, ReportFormat.HTML): """
  html:
    toc: true
    toc-location: left
    toc-depth: 3
    page-layout: full
    self-contained: true""",
            (r.ReportType.DOCUMENT, ReportFormat.PDF): """
  pdf:
    toc: false""",
            (r.ReportType.DOCUMENT, ReportFormat.DOCX): """
  docx:
    toc: false""",
            (r.ReportType.DOCUMENT, ReportFormat.ODT): """
  odt:
    toc: false""",
            (r.ReportType.PRESENTATION, ReportFormat.REVEALJS): """
  revealjs:
    toc: false
    smaller: true
    controls: true
    navigation-mode: vertical
    controls-layout: bottom-right
    output-file: quarto_report_revealjs.html""",
            (r.ReportType.PRESENTATION, ReportFormat.PPTX): """
  pptx:
    toc: false
    output: true""",
            (r.ReportType.NOTEBOOK, ReportFormat.JUPYTER): """
  jupyter:
    kernel: python3"""
        }

        # Create a key based on the report type and format
        key = (self.report_type, self.report_format)

        # Retrieve the configuration if it exists, or raise an error
        if key in format_configs:
            config = format_configs[key]
        else:
            raise ValueError(f"Unsupported report type or format: {self.report_type}, {self.report_format}")

        # Add the specific configuration to the YAML header
        yaml_header += config
        yaml_header += "\n---\n"

        return yaml_header

    def _generate_subsection(self, subsection, is_report_static, is_report_revealjs) -> List[str]:
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
        imports_written_subsection = []

        # Add subsection header and description
        subsection_content.append(f'## {subsection.title}')
        subsection_content.append(f'''{subsection.description}''')

        if is_report_revealjs:
            subsection_content.append(f'::: {{.panel-tabset}}\n')

        for component in subsection.components:
            imports_component = component.generate_imports()
            imports_written_subsection.append(imports_component)

            if component.component_type == r.ComponentType.PLOT:
                subsection_content.extend(self._generate_plot_content(component, is_report_static))
            
            elif component.component_type == r.ComponentType.DATAFRAME:
                subsection_content.extend(self._generate_dataframe_content(component, is_report_static))
            
            elif component.component_type == r.ComponentType.MARKDOWN:
                subsection_content.extend(self._generate_markdown_content(component))
        
        if is_report_revealjs:
            subsection_content.append(':::\n')
        
        return subsection_content, imports_written_subsection

    def _generate_plot_content(self, plot, is_report_static) -> List[str]:
        """
        Generate content for a plot component based on the report type.

        Parameters
        ----------
        plot : Plot
            The plot component to generate content for.
        is_report_static : bool
            A boolean indicating whether the report is static or interactive.
        
        Returns
        -------
        list : List[str]
            The list of content lines for the plot.
        """
        plot_content = []
        plot_content.append(f'### {plot.title}')
        if plot.plot_type == r.PlotType.INTERACTIVE:
            if plot.visualization_tool == r.VisualizationTool.PLOTLY:
                plot_content.append(f"""```{{python}}
#| label: {plot.name}
#| echo: false
with open('{os.path.join("..", plot.file_path)}', 'r') as plot_file:
    plot_data = plot_file.read()
fig_plotly = pio.from_json(plot_data)
fig_plotly.update_layout(width=950, height=500)""")
                if is_report_static:
                    # Define the output file name
                    plotly_plot_static = f"quarto_report/{plot.name.replace(' ', '_')}.png"
                    plot_content.append(f"""fig_plotly.write_image("{os.path.join("..", plotly_plot_static)}")\n```\n""")
                    plot_content.append(self._generate_image_content(plotly_plot_static, plot.name))
                else:
                    plot_content.append(f"""fig_plotly.show()\n```\n""")
            elif plot.visualization_tool == r.VisualizationTool.ALTAIR:
                plot_content.append(f"""```{{python}}
#| label: {plot.name}
#| echo: false
with open('{os.path.join("..", plot.file_path)}', 'r') as plot_file:
    plot_data = plot_file.read()
fig_altair = alt.Chart.from_json(plot_data).properties(width=900, height=400)""")
                if is_report_static:
                    # Define the output file name
                    altair_plot_static = f"quarto_report/{plot.name.replace(' ', '_')}.png"
                    plot_content.append(f"""fig_altair.save("{os.path.join("..", altair_plot_static)}")\n```\n""")
                    plot_content.append(self._generate_image_content(altair_plot_static, plot.name))
                else:
                    plot_content.append(f"""fig_altair\n```\n""")
            elif plot.visualization_tool == r.VisualizationTool.PYVIS:
                G = plot.read_network()
                num_nodes = G.number_of_nodes()
                num_edges = G.number_of_edges()
                plot_content.append(f'**Number of nodes:** {num_nodes}\n')
                plot_content.append(f'**Number of edges:** {num_edges}\n')
                if is_report_static:
                    # Define the output file name
                    net_static = f"quarto_report/{plot.name.replace(' ', '_')}.png"
                    plot.save_netwrok_image(G, net_static, "png")
                    plot_content.append(self._generate_image_content(net_static, plot.name))
                else:
                    # Define the output file name
                    output_file = f"quarto_report/{plot.name.replace(' ', '_')}.html"
                    # Get the Network object
                    net = plot.create_and_save_pyvis_network(G, output_file)

                    plot_content.append(f"""<div style="text-align: center;">
<iframe src="{os.path.join("..", output_file)}" alt="{plot.name} plot" width="800px" height="630px"></iframe>
</div>\n""")
        elif plot.plot_type == r.PlotType.STATIC:
            plot_content.append(self._generate_image_content(plot.file_path, width=950))
        
        return plot_content

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
        datframe_content.append(f'### {dataframe.title}')
        if dataframe.file_format == r.DataFrameFormat.CSV:
            if dataframe.delimiter:
                datframe_content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_csv('{os.path.join("..", dataframe.file_path)}', delimiter='{dataframe.delimiter}')""")
                datframe_content.extend(self._show_dataframe(dataframe, is_report_static))
            else:
                datframe_content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_csv('{os.path.join("..", dataframe.file_path)}')""")
                datframe_content.extend(self._show_dataframe(dataframe, is_report_static))
        elif dataframe.file_format == r.DataFrameFormat.PARQUET:
            datframe_content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_parquet('{os.path.join("..", dataframe.file_path)}')""")
            datframe_content.extend(self._show_dataframe(dataframe, is_report_static))
        elif dataframe.file_format == r.DataFrameFormat.TXT:
            datframe_content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_csv('{os.path.join("..", dataframe.file_path)}', sep='\\t')""")
            datframe_content.extend(self._show_dataframe(dataframe, is_report_static))
        elif dataframe.file_format == r.DataFrameFormat.EXCEL:
            datframe_content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_excel('{os.path.join("..", dataframe.file_path)}')""")
            datframe_content.extend(self._show_dataframe(dataframe, is_report_static))
        else:
            raise ValueError(f"Unsupported DataFrame file format: {dataframe.file_format}")

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
        markdown_content.append(f'### {markdown.title}')
        markdown_content.append(f"""```{{python}}
#| label: {markdown.name}
#| table-cap: "MD file"
#| table-type: "md"
#| echo: false
with open('{os.path.join("..", markdown.file_path)}', 'r') as markdown_file:
    markdown_content = markdown_file.read()
display.Markdown(markdown_content)
```\n""")
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
    
    def _show_dataframe(self, dataframe, is_report_static) -> List[str]:
        """
        Appends either a static image or an interactive representation of a DataFrame to the content list.

        Parameters
        ----------
        dataframe : DataFrame
            The DataFrame object containing the data to display.
        is_report_static : bool
            Determines if the report is in a static format (e.g., PDF) or interactive (e.g., HTML).
        
        Returns
        -------
        list : List[str]
            The list of content lines for the DataFrame.
        """
        dataframe_content = []
        if is_report_static:
            # Generate path for the DataFrame image
            df_image = f"quarto_report/{dataframe.name.replace(' ', '_')}.png"
            dataframe_content.append(f"dfi.export(df, '{os.path.join('..', df_image)}', max_rows=10, max_cols=5)\n```\n")
            # Use helper method to add centered image content
            dataframe_content.append(self._generate_image_content(df_image, dataframe.name))
        else:
            # Append code to display the DataFrame interactively
            dataframe_content.append(f"""show(df, classes="display nowrap compact", lengthMenu=[3, 5, 10])\n```\n""")
        
        return dataframe_content