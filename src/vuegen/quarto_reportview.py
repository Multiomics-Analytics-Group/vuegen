import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import List

import networkx as nx
import pandas as pd

from . import report as r
from .utils import create_folder, is_url, sort_imports


class QuartoReportView(r.ReportView):
    """
    A ReportView subclass for generating Quarto reports.
    """

    BASE_DIR = Path("quarto_report")
    STATIC_FILES_DIR = BASE_DIR / "static"

    def __init__(self, report: r.Report, report_type: r.ReportType):
        super().__init__(report=report, report_type=report_type)
        self.BUNDLED_EXECUTION = False
        self.quarto_path = "quarto"
        # self.env_vars = os.environ.copy()
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            self.report.logger.info("running in a PyInstaller bundle")
            self.BUNDLED_EXECUTION = True
            self.report.logger.debug(f"sys._MEIPASS: {sys._MEIPASS}")
        else:
            self.report.logger.info("running in a normal Python process")

        self.report.logger.debug("env_vars (QuartoReport): %s", os.environ)
        self.report.logger.debug(f"PATH: {os.environ['PATH']}")
        self.report.logger.debug(f"sys.path: {sys.path}")

    def generate_report(
        self, output_dir: Path = BASE_DIR, static_dir: Path = STATIC_FILES_DIR
    ) -> None:
        """
        Generates the qmd file of the quarto report. It creates code for rendering each section and its subsections with all components.

        Parameters
        ----------
        output_dir : Path, optional
            The folder where the generated report files will be saved (default is BASE_DIR).
        static_dir : Path, optional
            The folder where the static files will be saved (default is STATIC_FILES_DIR).
        """
        self.report.logger.debug(
            f"Generating '{self.report_type}' report in directory: '{output_dir}'"
        )

        # Create the output folder
        if create_folder(output_dir):
            self.report.logger.debug(f"Created output directory: '{output_dir}'")
        else:
            self.report.logger.debug(
                f"Output directory already existed: '{output_dir}'"
            )

        # Create the static folder
        if create_folder(static_dir):
            self.report.logger.info(
                f"Created output directory for static content: '{static_dir}'"
            )
        else:
            self.report.logger.info(
                f"Output directory for static content already existed: '{static_dir}'"
            )

        try:
            # Create variable to check if the report is static or revealjs
            is_report_static = self.report_type in {
                r.ReportType.PDF,
                r.ReportType.DOCX,
                r.ReportType.ODT,
                r.ReportType.PPTX,
            }
            is_report_revealjs = self.report_type == r.ReportType.REVEALJS

            # Define the YAML header for the quarto report
            yaml_header = self._create_yaml_header()

            # Create qmd content and imports for the report
            qmd_content = []
            report_imports = []

            # Add description of the report
            if self.report.description:
                qmd_content.append(f"""{self.report.description}""")

            # If available add the graphical abstract
            if self.report.graphical_abstract:
                qmd_content.append(
                    self._generate_image_content(self.report.graphical_abstract)
                )
            # Add the sections and subsections to the report
            self.report.logger.info("Starting to generate sections for the report.")
            for section in self.report.sections:
                self.report.logger.debug(
                    f"Processing section: '{section.title}' - {len(section.subsections)} subsection(s)"
                )
                # Add section header and description
                qmd_content.append(f"# {section.title}")
                if section.description:
                    qmd_content.append(f"""{section.description}\n""")

                if section.subsections:
                    # Iterate through subsections and integrate them into the section file
                    for subsection in section.subsections:
                        self.report.logger.debug(
                            f"Processing subsection: '{subsection.title}' - {len(subsection.components)} component(s)"
                        )
                        # Generate content for the subsection
                        subsection_content, subsection_imports = (
                            self._generate_subsection(
                                subsection,
                                is_report_static,
                                is_report_revealjs,
                                static_dir=static_dir,
                            )
                        )
                        qmd_content.extend(subsection_content)
                        report_imports.extend(subsection_imports)
                else:
                    self.report.logger.warning(
                        f"No subsections found in section: '{section.title}'. To show content in the report, add subsections to the section."
                    )

            # Flatten the subsection_imports into a single list
            flattened_report_imports = [
                imp for sublist in report_imports for imp in sublist
            ]

            # Remove duplicated imports
            report_unique_imports = set(flattened_report_imports)

            # ! set leads to random import order
            # ! separate and sort import statements, separate from setup code

            report_unique_imports, setup_statements = sort_imports(
                report_unique_imports
            )
            report_unique_imports += os.linesep
            report_unique_imports.extend(setup_statements)

            # Format imports
            report_formatted_imports = "\n".join(report_unique_imports)

            # Write the navigation and general content to a Python file
            with open(Path(output_dir) / f"{self.BASE_DIR}.qmd", "w") as quarto_report:
                quarto_report.write(yaml_header)
                quarto_report.write(
                    f"""\n```{{python}}
#| label: 'Imports'
{report_formatted_imports}
```\n\n"""
                )
                quarto_report.write("\n".join(qmd_content))
                self.report.logger.info(
                    f"Created qmd script to render the app: {self.BASE_DIR}.qmd"
                )

        except Exception as e:
            self.report.logger.error(
                f"An error occurred while generating the report: {str(e)}"
            )
            raise

    def run_report(self, output_dir: str = BASE_DIR) -> None:
        """
        Runs the generated quarto report.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the report was generated (default is 'sections').
        """
        # from quarto_cli import run_quarto # entrypoint of quarto-cli not in module?

        file_path_to_qmd = Path(output_dir) / f"{self.BASE_DIR}.qmd"
        args = [self.quarto_path, "render", str(file_path_to_qmd)]
        self.report.logger.info(
            f"Running '{self.report.title}' '{self.report_type}' report with {args!r}"
        )
        if self.report_type in [
            r.ReportType.PDF,
            r.ReportType.DOCX,
            r.ReportType.ODT,
        ]:
            subprocess.run(
                [self.quarto_path, "install", "tinytex", "--no-prompt"],
                check=True,
            )
            subprocess.run(
                [self.quarto_path, "install", "chromium", "--no-prompt"],
                check=True,
            )
        try:
            subprocess.run(
                args,
                check=True,
            )
            out_path = file_path_to_qmd.with_suffix(f".{self.report_type.lower()}")
            if self.report_type in [r.ReportType.REVEALJS, r.ReportType.JUPYTER]:
                out_path = file_path_to_qmd.with_suffix(".html")
            if not out_path.exists():
                raise FileNotFoundError(f"Report file could not be created: {out_path}")
            if self.report_type == r.ReportType.JUPYTER:
                args = [self.quarto_path, "convert", str(file_path_to_qmd)]
                subprocess.run(
                    args,
                    check=True,
                )
                self.report.logger.info(
                    f"Converted '{self.report.title}' '{self.report_type}' report to Jupyter Notebook after execution"
                )
            self.report.logger.info(
                f"'{self.report.title}' '{self.report_type}' report rendered"
            )
        except subprocess.CalledProcessError as e:
            self.report.logger.error(
                f"Error running '{self.report.title}' {self.report_type} report: {str(e)}"
            )
            raise
        # except FileNotFoundError as e:
        #     self.report.logger.error(
        #         f"Quarto is not installed. Please install Quarto to run the report: {str(e)}"
        #     )
        #     raise

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
jupyter: python3
format:"""

        # Define format-specific YAML configurations
        format_configs = {
            r.ReportType.HTML: """
  html:
    toc: true
    toc-location: left
    toc-depth: 3
    page-layout: full
    self-contained: true
include-in-header:
    text: |
        <style type="text/css">
        .footer {
        position: relative;
        left: 0;
        width: 100%;
        text-align: center;
        margin-top: 20px;
        }
        </style>
include-after-body:
    text: |
        <footer class="footer">
            This report was generated with 
            <a href="https://github.com/Multiomics-Analytics-Group/vuegen" target="_blank">
                <img src="https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_logo.svg" alt="VueGen" width="65px">
            </a>
            | Copyright 2025 <a href="https://github.com/Multiomics-Analytics-Group" target="_blank">Multiomics Network Analytics Group (MoNA)</a>
        </footer>""",
            r.ReportType.PDF: """
  pdf:
    toc: false
    margin:
      - bottom=40mm
    include-in-header: 
        text: |
            \\usepackage{scrlayer-scrpage}
            \\usepackage{hyperref}
            \\clearpairofpagestyles
            \\lofoot{This report was generated with \\href{https://github.com/Multiomics-Analytics-Group/vuegen}{VueGen} | \\copyright{} 2025 \\href{https://github.com/Multiomics-Analytics-Group}{Multiomics Network Analytics Group}}
            \\rofoot{\\pagemark}""",
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
    output-file: quarto_report_revealjs.html
include-in-header:
    text: |
        <style type="text/css">
        .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        }
        </style>
include-after-body:
    text: |
        <footer class="footer">
            This report was generated with 
            <a href="https://github.com/Multiomics-Analytics-Group/vuegen" target="_blank">
                <img src="https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_logo.svg" alt="VueGen" width="65px">
            </a>
            | Copyright 2025 <a href="https://github.com/Multiomics-Analytics-Group" target="_blank">Multiomics Network Analytics Group (MoNA)</a>
        </footer>""",
            r.ReportType.PPTX: """
  pptx:
    toc: false
    output: true""",
            r.ReportType.JUPYTER: """
  html:
    toc: true
    toc-location: left
    toc-depth: 3
    page-layout: full
    self-contained: true
include-in-header:
    text: |
        <style type="text/css">
        .footer {
        position: relative;
        left: 0;
        width: 100%;
        text-align: center;
        margin-top: 20px;
        }
        </style>
include-after-body:
    text: |
        <footer class="footer">
            This report was generated with 
            <a href="https://github.com/Multiomics-Analytics-Group/vuegen" target="_blank">
                <img src="../docs/images/vuegen_logo.svg" alt="VueGen" width="65px">
            </a>
            | Copyright 2025 <a href="https://github.com/Multiomics-Analytics-Group" target="_blank">Multiomics Network Analytics Group (MoNA)</a>
        </footer>""",
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

    def _generate_subsection(
        self,
        subsection,
        is_report_static,
        is_report_revealjs,
        static_dir: str,
    ) -> tuple[List[str], List[str]]:
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
        static_dir : str
            The folder where the static files will be saved.
        Returns
        -------
        tuple : (List[str], List[str])
            - list of subsection content lines (List[str])
            - list of imports for the subsection (List[str])
        """
        subsection_content = []
        subsection_imports = []

        # Add subsection header and description
        subsection_content.append(f"## {subsection.title}")
        if subsection.description:
            subsection_content.append(f"""{subsection.description}\n""")

        if is_report_revealjs:
            subsection_content.append(f"::: {{.panel-tabset}}\n")

        for component in subsection.components:
            component_imports = self._generate_component_imports(component)
            subsection_imports.append(component_imports)

            if component.component_type == r.ComponentType.PLOT:
                subsection_content.extend(
                    self._generate_plot_content(
                        component, is_report_static, static_dir=static_dir
                    )
                )
            elif component.component_type == r.ComponentType.DATAFRAME:
                subsection_content.extend(
                    self._generate_dataframe_content(
                        component, is_report_static, static_dir=static_dir
                    )
                )
            elif (
                component.component_type == r.ComponentType.MARKDOWN
                and component.title.lower() != "description"
            ):
                subsection_content.extend(self._generate_markdown_content(component))
            elif (
                component.component_type == r.ComponentType.HTML
                and not is_report_static
            ):
                subsection_content.extend(self._generate_html_content(component))
            else:
                self.report.logger.warning(
                    f"Unsupported component type '{component.component_type}' in subsection: {subsection.title}"
                )

        if is_report_revealjs:
            subsection_content.append(":::\n")

        self.report.logger.info(
            f"Generated content and imports for subsection: '{subsection.title}'"
        )
        return subsection_content, subsection_imports

    def _generate_plot_content(
        self, plot, is_report_static, static_dir: str
    ) -> List[str]:
        """
        Generate content for a plot component based on the report type.

        Parameters
        ----------
        plot : Plot
            The plot component to generate content for.
        static_dir : str
            The folder where the static files will be saved.

        Returns
        -------
        list : List[str]
            The list of content lines for the plot.
        """
        plot_content = []
        # Add title
        plot_content.append(f"### {plot.title}")

        # Define plot path
        if is_report_static:
            static_plot_path = Path(static_dir) / f"{plot.title.replace(' ', '_')}.png"
        else:
            html_plot_file = Path(static_dir) / f"{plot.title.replace(' ', '_')}.html"

        # Add content for the different plot types
        try:
            if plot.plot_type == r.PlotType.STATIC:
                plot_content.append(
                    self._generate_image_content(plot.file_path, width=950)
                )
            elif plot.plot_type == r.PlotType.PLOTLY:
                plot_content.append(self._generate_plot_code(plot))
                if is_report_static:
                    plot_content.append(
                        f"""fig_plotly.write_image("{static_plot_path.resolve().as_posix()}")\n```\n"""
                    )
                    plot_content.append(self._generate_image_content(static_plot_path))
                else:
                    plot_content.append(f"""fig_plotly.show()\n```\n""")
            elif plot.plot_type == r.PlotType.ALTAIR:
                plot_content.append(self._generate_plot_code(plot))
                if is_report_static:
                    plot_content.append(
                        f"""fig_altair.save("{static_plot_path.resolve().as_posix()}")\n```\n"""
                    )
                    plot_content.append(self._generate_image_content(static_plot_path))
                else:
                    plot_content.append(f"""fig_altair\n```\n""")
            elif plot.plot_type == r.PlotType.INTERACTIVE_NETWORK:
                networkx_graph = plot.read_network()
                if isinstance(networkx_graph, tuple):
                    # If network_data is a tuple, separate the network and html file path
                    networkx_graph, html_plot_file = networkx_graph
                elif isinstance(networkx_graph, nx.Graph) and not is_report_static:
                    # Get the pyvis object and create html
                    pyvis_graph = plot.create_and_save_pyvis_network(
                        networkx_graph, html_plot_file
                    )

                # Add number of nodes and edges to the plor conetnt
                num_nodes = networkx_graph.number_of_nodes()
                num_edges = networkx_graph.number_of_edges()
                plot_content.append(f"**Number of nodes:** {num_nodes}\n")
                plot_content.append(f"**Number of edges:** {num_edges}\n")

                # Add code to generate network depending on the report type
                if is_report_static:
                    plot.save_network_image(networkx_graph, static_plot_path, "png")
                    plot_content.append(self._generate_image_content(static_plot_path))
                else:
                    plot_content.append(self._generate_plot_code(plot, html_plot_file))
            else:
                self.report.logger.warning(f"Unsupported plot type: {plot.plot_type}")
        except Exception as e:
            self.report.logger.error(
                f"Error generating content for '{plot.plot_type}' plot '{plot.id}' '{plot.title}': {str(e)}"
            )
            raise

        # Add caption if available
        if plot.caption:
            plot_content.append(f">{plot.caption}\n")

        self.report.logger.info(
            f"Successfully generated content for plot: '{plot.title}'"
        )
        return plot_content

    def _generate_plot_code(self, plot, output_file="") -> str:
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
        # Initialize plot code with common structure
        plot_code = f"""```{{python}}
#| label: '{plot.title} {plot.id}'
#| fig-cap: ""
"""
        # If the file path is a URL, generate code to fetch content via requests
        if is_url(plot.file_path):
            plot_code += f"""
response = requests.get('{plot.file_path}')
response.raise_for_status()
plot_json = response.text\n"""
        else:  # If it's a local file
            plot_code += f"""
with open('{(Path("..") / plot.file_path).as_posix()}', 'r') as plot_file:
    plot_json = plot_file.read()\n"""
        # Add specific code for each visualization tool
        if plot.plot_type == r.PlotType.PLOTLY:
            plot_code += """
fig_plotly = pio.from_json(plot_json)
fig_plotly.update_layout(width=950, height=500)\n"""
        elif plot.plot_type == r.PlotType.ALTAIR:
            plot_code += """fig_altair = alt.Chart.from_json(plot_json).properties(width=900, height=400)"""
        elif plot.plot_type == r.PlotType.INTERACTIVE_NETWORK:
            # Generate the HTML embedding for interactive networks
            if is_url(plot.file_path) and plot.file_path.endswith(".html"):
                iframe_src = output_file
            else:
                iframe_src = Path("..") / output_file

            # Embed the HTML file in an iframe
            plot_code = f"""
<div style="text-align: center;">
<iframe src="{iframe_src}" alt="{plot.title} plot" width="800px" height="630px"></iframe>
</div>\n"""
        return plot_code

    def _generate_dataframe_content(
        self, dataframe, is_report_static, static_dir: str
    ) -> List[str]:
        """
        Generate content for a DataFrame component based on the report type.

        Parameters
        ----------
        dataframe : DataFrame
            The dataframe component to add to content.
        is_report_static : bool
            A boolean indicating whether the report is static or interactive.
        static_dir : str
            The folder where the static files will be saved.

        Returns
        -------
        list : List[str]
            The list of content lines for the DataFrame.
        """
        dataframe_content = []
        # Add title
        dataframe_content.append(f"### {dataframe.title}")

        # Append header for DataFrame loading
        dataframe_content.append(
            f"""```{{python}}
#| label: '{dataframe.title} {dataframe.id}'
#| fig-cap: ""
"""
        )
        # Mapping of file extensions to read functions
        read_function_mapping = {
            r.DataFrameFormat.CSV.value_with_dot: pd.read_csv,
            r.DataFrameFormat.PARQUET.value_with_dot: pd.read_parquet,
            r.DataFrameFormat.TXT.value_with_dot: pd.read_table,
            r.DataFrameFormat.XLS.value_with_dot: pd.read_excel,
            r.DataFrameFormat.XLSX.value_with_dot: pd.read_excel,
        }
        try:
            # Check if the file extension matches any DataFrameFormat value
            file_extension = Path(dataframe.file_path).suffix.lower()
            if not any(
                file_extension == fmt.value_with_dot for fmt in r.DataFrameFormat
            ):
                self.report.logger.error(
                    f"Unsupported file extension: {file_extension}. Supported extensions are: {', '.join(fmt.value for fmt in r.DataFrameFormat)}."
                )

            # Build the file path (URL or local file)
            file_path = (
                dataframe.file_path
                if is_url(dataframe.file_path)
                else Path("..") / dataframe.file_path
            )

            # Load the DataFrame using the correct function
            read_function = read_function_mapping[file_extension]
            dataframe_content.append(
                f"""df = pd.{read_function.__name__}('{file_path.as_posix()}')\n"""
            )

            # Display the dataframe
            dataframe_content.extend(
                self._show_dataframe(dataframe, is_report_static, static_dir=static_dir)
            )

        except Exception as e:
            self.report.logger.error(
                f"Error generating content for DataFrame: {dataframe.title}. Error: {str(e)}"
            )
            raise
        # Add caption if available
        if dataframe.caption:
            dataframe_content.append(f">{dataframe.caption}\n")

        self.report.logger.info(
            f"Successfully generated content for DataFrame: '{dataframe.title}'"
        )
        return dataframe_content

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
        markdown_content.append(f"### {markdown.title}")

        try:
            # Initialize md code with common structure
            markdown_content.append(
                f"""
```{{python}}
#| label: '{markdown.title} {markdown.id}'
#| fig-cap: ""\n"""
            )
            # If the file path is a URL, generate code to fetch content via requests
            if is_url(markdown.file_path):
                markdown_content.append(
                    f"""
response = requests.get('{markdown.file_path}')
response.raise_for_status()
markdown_content = response.text\n"""
                )
            else:  # If it's a local file
                markdown_content.append(
                    f"""
with open('{(Path("..") / markdown.file_path).as_posix()}', 'r') as markdown_file:
    markdown_content = markdown_file.read()\n"""
                )

            # Code to display md content
            markdown_content.append(f"""display.Markdown(markdown_content)\n```\n""")

        except Exception as e:
            self.report.logger.error(
                f"Error generating content for Markdown: {markdown.title}. Error: {str(e)}"
            )
            raise

        # Add caption if available
        if markdown.caption:
            markdown_content.append(f">{markdown.caption}\n")

        self.report.logger.info(
            f"Successfully generated content for Markdown: '{markdown.title}'"
        )
        return markdown_content

    def _generate_html_content(self, html) -> List[str]:
        """
        Adds an HTML component to the report.

        Parameters
        ----------
        html : Html
            The HTML component to add to the report. This could be a local file path or a URL.

        Returns
        -------
        list : List[str]
            The list of content lines for embedding the HTML.
        """
        html_content = []

        # Add title
        html_content.append(f"### {html.title}")

        try:
            # Embed the HTML in an iframe
            iframe_src = (
                html.file_path
                if is_url(html.file_path)
                else Path("..") / html.file_path
            )
            iframe_code = f"""
<div style="text-align: center;">
<iframe src="{iframe_src}" alt="{html.title}" width="800px" height="630px"></iframe>
</div>\n"""
            html_content.append(iframe_code)

        except Exception as e:
            self.report.logger.error(
                f"Error generating content for HTML: {html.title}. Error: {str(e)}"
            )
            raise

        self.report.logger.info(
            f"Successfully generated content for HTML: '{html.title}'"
        )
        return html_content

    def _generate_image_content(
        self, image_path: str, alt_text: str = "", width: int = 650, height: int = 400
    ) -> str:
        """
        Adds an image to the content list in an HTML format with a specified width and height.

        Parameters
        ----------
        image_path : str
            Path to the image file or a URL to the image.
        width : int, optional
            Width of the image in pixels (default is 650).
        height : int, optional
            Height of the image in pixels (default is 400).
        alt_text : str, optional
            Alternative text for the image (default is an empty string).

        Returns
        -------
        str
            The formatted image content.
        """
        if is_url(image_path):
            src = image_path
            return (
                f"""![]({src}){{fig-alt={alt_text} width={width} height={height}}}\n"""
            )
        else:
            src = Path(image_path).resolve()
            return (
                f"""![](/{src}){{fig-alt={alt_text} width={width} height={height}}}\n"""
            )

    def _show_dataframe(
        self, dataframe, is_report_static, static_dir: str
    ) -> List[str]:
        """
        Appends either a static image or an interactive representation of a DataFrame to the content list.

        Parameters
        ----------
        dataframe : DataFrame
            The DataFrame object containing the data to display.
        is_report_static : bool
            Determines if the report is in a static format (e.g., PDF) or interactive (e.g., HTML).
        static_dir : str
            The folder where the static files will be saved.

        Returns
        -------
        list : List[str]
            The list of content lines for the DataFrame.
        """
        dataframe_content = []
        if is_report_static:
            # Generate path for the DataFrame image
            df_image = Path(static_dir) / f"{dataframe.title.replace(' ', '_')}.png"
            dataframe_content.append(
                f"df.dfi.export('{Path(df_image).resolve().as_posix()}', max_rows=10, max_cols=5)\n```\n"
            )
            # Use helper method to add centered image content
            dataframe_content.append(self._generate_image_content(df_image))
        else:
            # Append code to display the DataFrame interactively
            dataframe_content.append(
                f"""show(df, classes="display nowrap compact", lengthMenu=[3, 5, 10])\n```\n"""
            )

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
            "plot": {
                r.PlotType.ALTAIR: ["import altair as alt", "import requests"],
                r.PlotType.PLOTLY: ["import plotly.io as pio", "import requests"],
            },
            "dataframe": [
                "import pandas as pd",
                "from itables import show, init_notebook_mode",
                "import dataframe_image as dfi",
                "init_notebook_mode(all_interactive=True)",
            ],
            "markdown": ["import IPython.display as display", "import requests"],
        }

        # Iterate over sections and subsections to determine needed imports
        component_type = component.component_type
        component_imports = []

        # Add relevant imports based on component type and visualization tool
        if component_type == r.ComponentType.PLOT:
            plot_type = getattr(component, "plot_type", None)
            if plot_type in components_imports["plot"]:
                component_imports.extend(components_imports["plot"][plot_type])
        elif component_type == r.ComponentType.DATAFRAME:
            component_imports.extend(components_imports["dataframe"])
        elif component_type == r.ComponentType.MARKDOWN:
            component_imports.extend(components_imports["markdown"])

        # Return the list of import statements
        return component_imports
