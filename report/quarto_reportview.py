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

        # Define the YAML header for the quarto report
        yaml_header = self._create_yaml_header()
        
        # Create qmd content for the report
        qmd_content = []
        imports_report = []

        # Add the title and description of the report
        qmd_content.append(f'''{self.report.description}\n''')

        # If available add the graphical abstract
        if self.report.graphical_abstract:
            qmd_content.append(f'''::: {{style="text-align: center;"}}
![Graphical abstract for the {self.report.title} report]({os.path.join('..', self.report.graphical_abstract)}){{ width=650px }}
:::\n''')
        # Add the sections and subsections to the report
        for section in self.report.sections:
            # Add section header and description
            qmd_content.append(f'# {section.title}')
            qmd_content.append(f'''{section.description}''')
            
            if section.subsections:
                # Iterate through subsections and integrate them into the section file
                for subsection in section.subsections:
                    # Add subsection header and description
                    subsection_header = f'## {subsection.title}'
                    qmd_content.append(subsection_header)
                    subsection_desc = f'''{subsection.description}'''
                    qmd_content.append(subsection_desc)
                    
                    # Generate plots for the subsection
                    imports_subsection = self._generate_subsection(subsection, qmd_content)
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
        Creates a YAML header for the Quarto report based on the specified eport type and output formats.

        Returns
        -------
        str
            A formatted YAML header string customized for the specified output format.
        """
        yaml_header = f"""---
title: {self.report.title}
format:"""
        # Check the report type
        if self.report_type == r.ReportType.DOCUMENT:
            # Add specific format settings
            if ReportFormat.HTML == self.report_format:
                yaml_header += f"""
  html:
    page-layout: full
    self-contained: true
    toc-location: left
    toc-depth: 3"""
            if ReportFormat.PDF == self.report_format:
                yaml_header += f"""
  pdf:
    toc: false
                """
            if ReportFormat.DOCX == self.report_format:
                yaml_header += f"""
  docx:
    toc: false
                """
            if ReportFormat.ODT == self.report_format:
                yaml_header += f"""
  odt:
    toc: false
                """
        elif self.report_type == r.ReportType.PRESENTATION:
            if ReportFormat.REVEALJS == self.report_format:
                yaml_header += f"""
  revealjs:
    toc: false
                """
            if ReportFormat.PPTX == self.report_format:
                yaml_header += f"""
  pptx:
    toc: false
                """
        elif self.report_type == r.ReportType.NOTEBOOK:
            if ReportFormat.JUPYTER == self.report_format:
                yaml_header += f"""
  jupyter:
    kernel: python3
                """
        else:
            raise ValueError(f"Unsupported report type: {self.report_type}")

        yaml_header += "\n---\n"
        return yaml_header

    def _generate_subsection(self, subsection, content) -> List[str]:
        """
        Generate code to render components (plots, dataframes, markdown) in the given subsection, 
        creating imports and content for the subsection based on the component type.

        Parameters
        ----------
        subsection : Subsection
            The subsection containing the components.
        imports_written : set
            A set of already written imports.
        content : list
            A list to which the generated content will be appended.

        Returns
        -------
        list
            A list of imports for the subsection.
        """
        imports_written_subsection = []
        is_report_static = self.report_format in {ReportFormat.PDF, ReportFormat.DOCX, ReportFormat.ODT}

        for component in subsection.components:
            imports_component = component.generate_imports()
            imports_written_subsection.append(imports_component)

            if component.component_type == r.ComponentType.PLOT:
                self._add_plot_to_content(component, content, is_report_static)
            
            elif component.component_type == r.ComponentType.DATAFRAME:
                self._add_dataframe_to_content(component, content, is_report_static)
            
            elif component.component_type == r.ComponentType.MARKDOWN:
                self._add_markdown_to_content(component, content)
        
        return imports_written_subsection

    def _add_plot_to_content(self, plot, content, is_report_static):
        """
        Adds plot content based on whether the report type is static or interactive.

        Parameters
        ----------
        plot : Plot
            The plot component to add to content.
        content : list
            The list to append content to.
        is_report_static : bool
            A boolean indicating whether the report is static or interactive.
        """
        content.append(f'### {plot.title}')
        if plot.plot_type == r.PlotType.INTERACTIVE:
            if plot.visualization_tool == r.VisualizationTool.PLOTLY:
                content.append(f"""```{{python}}
#| label: {plot.name}
#| echo: false
with open('{os.path.join("..", plot.file_path)}', 'r') as plot_file:
    plot_data = plot_file.read()
fig_plotly = pio.from_json(plot_data)""")
                if is_report_static:
                    # Define the output file name
                    plotly_plot_static = f"quarto_report/{plot.name.replace(' ', '_')}.png"
                    content.append(f"""fig_plotly.write_image("{os.path.join("..", plotly_plot_static)}")\n```\n""")
                    self._add_image_content(content, plotly_plot_static, plot.name)
                else:
                    content.append(f"""fig_plotly.show()\n```\n""")
            elif plot.visualization_tool == r.VisualizationTool.ALTAIR:
                content.append(f"""```{{python}}
#| label: {plot.name}
#| echo: false
with open('{os.path.join("..", plot.file_path)}', 'r') as plot_file:
    plot_data = plot_file.read()
fig_altair = alt.Chart.from_json(plot_data)""")
                if is_report_static:
                    # Define the output file name
                    altair_plot_static = f"quarto_report/{plot.name.replace(' ', '_')}.png"
                    content.append(f"""fig_altair.save("{os.path.join("..", altair_plot_static)}")\n```\n""")
                    self._add_image_content(content, altair_plot_static, plot.name)
                else:
                    content.append(f"""fig_altair\n```\n""")
            elif plot.visualization_tool == r.VisualizationTool.PYVIS:
                G = plot.read_network()
                num_nodes = G.number_of_nodes()
                num_edges = G.number_of_edges()
                content.append(f'**Number of nodes:** {num_nodes}')
                content.append(f'**Number of edges:** {num_edges}\n')
                if is_report_static:
                    # Define the output file name
                    net_static = f"quarto_report/{plot.name.replace(' ', '_')}.png"
                    plot.save_netwrok_image(G, net_static, "png")
                    self._add_image_content(content, net_static, plot.name)
                else:
                    # Define the output file name
                    output_file = f"quarto_report/{plot.name.replace(' ', '_')}.html"
                    # Get the Network object
                    net = plot.create_and_save_pyvis_network(G, output_file)

                    content.append(f"""<div style="text-align: center;">
<iframe src="{os.path.join("..", output_file)}" alt="{plot.name} plot" width="800px" height="630px"></iframe>
</div>\n""")
        elif plot.plot_type == r.PlotType.STATIC:
            self._add_image_content(content, plot.file_path, plot.name)

    def _add_dataframe_to_content(self, dataframe, content, is_report_static):
        """
        Adds dataframe content based on the report type.

        Parameters
        ----------
        dataframe : DataFrame
            The dataframe component to add to content.
        content : list
            The list to append content to.
        is_report_static : bool
            A boolean indicating whether the report is static or interactive.
        """
        content.append(f'### {dataframe.title}')
        if dataframe.file_format == r.DataFrameFormat.CSV:
            if dataframe.delimiter:
                content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_csv('{os.path.join("..", dataframe.file_path)}', delimiter='{dataframe.delimiter}')""")
                if is_report_static:
                    df_image = f"quarto_report/{dataframe.name.replace(' ', '_')}.png"
                    content.append(f"""dfi.export(df, '{os.path.join("..", df_image)}', max_rows=10, max_cols=5)\n```\n""")
                    self._add_image_content(content, df_image, dataframe.name)
                else:
                    content.append(f"show(df)\n```\n")
            else:
                content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_csv('{os.path.join("..", dataframe.file_path)}')""")
                if is_report_static:
                    df_image = f"quarto_report/{dataframe.name.replace(' ', '_')}.png"
                    content.append(f"""dfi.export(df, '{os.path.join("..", df_image)}', max_rows=10, max_cols=5)\n```\n""")
                    self._add_image_content(content, df_image, dataframe.name)
                else:
                    content.append(f"show(df)\n```\n")
        elif dataframe.file_format == r.DataFrameFormat.PARQUET:
            content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_parquet('{os.path.join("..", dataframe.file_path)}')""")
            if is_report_static:
                df_image = f"quarto_report/{dataframe.name.replace(' ', '_')}.png"
                content.append(f"""dfi.export(df, '{os.path.join("..", df_image)}', max_rows=10, max_cols=5)\n```\n""")
                self._add_image_content(content, df_image, dataframe.name)
            else:
                content.append(f"show(df)\n```\n")
        elif dataframe.file_format == r.DataFrameFormat.TXT:
            content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_csv('{os.path.join("..", dataframe.file_path)}', sep='\\t')""")
            if is_report_static:
                df_image = f"quarto_report/{dataframe.name.replace(' ', '_')}.png"
                content.append(f"""dfi.export(df, '{os.path.join("..", df_image)}', max_rows=10, max_cols=5)\n```\n""")
                self._add_image_content(content, df_image, dataframe.name)
            else:
                content.append(f"show(df)\n```\n")
        elif dataframe.file_format == r.DataFrameFormat.EXCEL:
            content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_excel('{os.path.join("..", dataframe.file_path)}')""")
            if is_report_static:
                df_image = f"quarto_report/{dataframe.name.replace(' ', '_')}.png"
                content.append(f"""dfi.export(df, '{os.path.join("..", df_image)}', max_rows=10, max_cols=5)\n```\n""")
                self._add_image_content(content, df_image, dataframe.name)
            else:
                content.append(f"show(df)\n```\n")
        else:
            raise ValueError(f"Unsupported DataFrame file format: {dataframe.file_format}")

    def _add_markdown_to_content(self, markdown, content):
        """
        Adds markdown content to the report.

        Parameters
        ----------
        markdown : Markdown
            The markdown component to add to content.
        content : list
            The list to append content to.
        """
        content.append(f'### {markdown.title}')
        content.append(f"""```{{python}}
#| label: {markdown.name}
#| table-cap: "MD file"
#| table-type: "md"
#| echo: false
with open('{os.path.join("..", markdown.file_path)}', 'r') as markdown_file:
    markdown_content = markdown_file.read()
display.Markdown(markdown_content)
```\n""")

    def _add_image_content(self, content: list, image_path: str, alt_text: str, width: int = 650) -> None:
        """
        Adds an image to the content list in a centered format with a specified width.

        Parameters
        ----------
        content : list
            The list to which the image markdown will be appended.
        image_path : str
            Path to the image file.
        alt_text : str
            Alternative text for the image.
        width : int, optional
            Width of the image in pixels (default is 650).
        """
        content.append(f"""::: {{style="text-align: center;"}}
![{alt_text}]({os.path.join('..', image_path)}){{ width={width}px }}
:::\n""")