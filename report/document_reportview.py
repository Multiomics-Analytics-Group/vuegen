import report as r
import os
import sys
from typing import List, Optional
import subprocess

class DocumentReportView(r.ReportView):
    """
    A ReportView subclass for generating document reports using quarto.

    Methods
    -------
    generate_report(output_dir)
        Generates the qmd file of the quarto report. It creates code for rendering each section and its subsections with all components.
    run_report(output_dir)
        Runs the generated quarto report.
    """

    def __init__(self, identifier: int, name: str, columns: Optional[List[str]], output_format: str, report: r.Report):
        super().__init__(identifier, name=name, columns=columns, report=report)
        self.output_format = output_format

    def generate_report(self, output_dir: str = 'document_report/') -> None:
        """
        Generates the qmd file of the quarto report. It creates code for rendering each section and its subsections with all components.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the generated report files will be saved (default is 'document_report/').
        """
        # Create the output folder if it does not exist
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # Define the YAML header for the quarto report
        yaml_header = f'''---
title: {self.report.title}
toc: true
toc-depth: 4
format:
  html:
    page-layout: full
    self-contained: true
    toc-location: left
  pdf:
    toc: false
jupyter: python3
---
'''
        # Create qmd content for the report
        qmd_content = []
        imports_report = []

        # Add the title and description of the report
        #qmd_content.append(f'# {self.report.title}')
        qmd_content.append(f'''{self.report.description}\n''')

        # If available add the graphical abstract
        if self.report.graphical_abstract:
            qmd_content.append(f'''::: {{style="text-align: center;"}}
![Graphical abstract for the {self.report.title} report]({os.path.join('..', self.report.graphical_abstract)}){{ width=650px }}
:::\n''')
        # Add the sections and subsections to the report
        for section in self.report.sections:
            # Add section header and description
            qmd_content.append(f'## {section.title}')
            qmd_content.append(f'''{section.description}''')
            
            if section.subsections:
                # Iterate through subsections and integrate them into the section file
                for subsection in section.subsections:
                    subsection_name_var = subsection.name.replace(" ", "_")
                    
                    # Add subsection header and description
                    subsection_header = f'### {subsection.title}'
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
        with open(os.path.join(output_dir, "document_report_script.qmd"), 'w') as document_report:
            document_report.write(yaml_header)
            document_report.write(f"""```{{python}}
#| label: 'Imports'
#| echo: false
{formatted_imports}
```\n\n""")
            document_report.write("\n".join(qmd_content))

    def run_report(self, output_dir: str = 'document_report') -> None:
        """
        Runs the generated quarto report.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the report was generated (default is 'sections').
        """
        # sys.argv = ["streamlit", "run", os.path.join(output_dir, "report_manager.py")]
        subprocess.run(["quarto", "render", os.path.join(output_dir, "document_report_script.qmd")], check=True)

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
        for component in subsection.components:
            # Write imports if not already done
            imports_component = component.generate_imports()
            imports_written_subsection.append(imports_component)

            # Handle different types of components
            if component.component_type == r.ComponentType.PLOT:
                # Cast component to Plot
                plot = component 
                if plot.plot_type == r.PlotType.INTERACTIVE:
                    if plot.visualization_tool == r.VisualizationTool.PLOTLY:
                        # Add the plot title as a header
                        content.append(f'#### {plot.title}')
                        content.append(f"""```{{python}}
#| label: {plot.name}
#| echo: false
with open('{os.path.join("..", plot.file_path)}', 'r') as plot_file:
    plot_data = plot_file.read()
fig_plotly = pio.from_json(plot_data)
fig_plotly.show()
```\n""")
                    elif plot.visualization_tool == r.VisualizationTool.ALTAIR:
                        content.append(f'#### {plot.title}')
                        content.append(f"""```{{python}}
#| label: {plot.name}
#| echo: false
with open('{os.path.join("..", plot.file_path)}', 'r') as plot_file:
    plot_data = plot_file.read()
fig_altair = alt.Chart.from_json(plot_data)
fig_altair
```\n""")
                    elif plot.visualization_tool == r.VisualizationTool.PYVIS:
                        G = plot.read_network()
                        # Define the output file name
                        output_file = f"example_data/{plot.name.replace(' ', '_')}.html"
                        # Get the Network object
                        net = plot.create_and_save_pyvis_network(G, output_file)
                        num_nodes = len(net.nodes)
                        num_edges = len(net.edges)
                        content.append(f'#### {plot.title}')
                        content.append(f'**Number of nodes:** {num_nodes}')
                        content.append(f'**Number of edges:** {num_edges}')

                        content.append(f"""<div style="text-align: center;">
  <iframe src="{os.path.join("..", output_file)}" alt="{plot.name} plot" width="800px" height="630px"></iframe>
</div>\n""")

                elif plot.plot_type == r.PlotType.STATIC:
                    content.append(f'#### {plot.title}')
                    content.append(f"""::: {{style="text-align: center;"}}
![{plot.name}]({os.path.join('..', plot.file_path)}){{ width=650px }}
:::\n""")

            elif component.component_type == r.ComponentType.DATAFRAME:
                # Cast component to DataFrame
                dataframe = component 
                if dataframe.file_format == r.DataFrameFormat.CSV:
                    content.append(f'#### {dataframe.title}')
                    if dataframe.delimiter:
                        content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_csv('{os.path.join("..", dataframe.file_path)}', delimiter='{dataframe.delimiter}')
show(df)
```\n""")
                    else:
                        content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_csv('{os.path.join("..", dataframe.file_path)}')
show(df)
```\n""")
                elif dataframe.file_format == r.DataFrameFormat.PARQUET:
                    content.append(f'#### {dataframe.title}')
                    content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_parquet('{os.path.join("..", dataframe.file_path)}')
show(df)
```\n""")
                elif dataframe.file_format == r.DataFrameFormat.TXT:
                    content.append(f'#### {dataframe.title}')
                    content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_csv('{os.path.join("..", dataframe.file_path)}', sep='\\t')
show(df)
```\n""")
                elif dataframe.file_format == r.DataFrameFormat.EXCEL:
                    content.append(f'#### {dataframe.title}')
                    content.append(f"""```{{python}}
#| label: {dataframe.name}
#| echo: false
df = pd.read_excel('{os.path.join("..", dataframe.file_path)}')
show(df)
```\n""")
                else:
                    raise ValueError(f"Unsupported DataFrame file format: {dataframe.file_format}")
            elif component.component_type == r.ComponentType.MARKDOWN:
                # Cast component to Markdown
                markdown = component 
                content.append(f'#### {markdown.title}')
                content.append(f"""```{{python}}
#| label: {markdown.name}
#| table-cap: "MD file"
#| table-type: "md"
#| echo: false
with open('{os.path.join("..", markdown.file_path)}', 'r') as markdown_file:
    markdown_content = markdown_file.read()
display.Markdown(markdown_content)
```\n""")
        return imports_written_subsection