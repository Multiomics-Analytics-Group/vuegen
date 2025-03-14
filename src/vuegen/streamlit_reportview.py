import os
import subprocess
import sys
from pathlib import Path
from typing import List

import pandas as pd
from streamlit.web import cli as stcli

from . import report as r
from .utils import create_folder, generate_footer, is_url


class StreamlitReportView(r.WebAppReportView):
    """
    A Streamlit-based implementation of the WebAppReportView abstract base class.
    """

    BASE_DIR = "streamlit_report"
    SECTIONS_DIR = Path(BASE_DIR) / "sections"
    STATIC_FILES_DIR = Path(BASE_DIR) / "static"
    REPORT_MANAG_SCRIPT = "report_manager.py"

    def __init__(
        self,
        report: r.Report,
        report_type: r.ReportType,
        streamlit_autorun: bool = False,
    ):
        super().__init__(report=report, report_type=report_type)
        self.streamlit_autorun = streamlit_autorun
        self.BUNDLED_EXECUTION = False
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            self.report.logger.info("running in a PyInstaller bundle")
            self.BUNDLED_EXECUTION = True
        else:
            self.report.logger.info("running in a normal Python process")

    def generate_report(
        self, output_dir: str = SECTIONS_DIR, static_dir: str = STATIC_FILES_DIR
    ) -> None:
        """
        Generates the Streamlit report and creates Python files for each section and its subsections and plots.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the generated report files will be saved (default is SECTIONS_DIR).
        static_dir : str, optional
            The folder where the static files will be saved (default is STATIC_FILES_DIR).
        """
        self.report.logger.debug(
            f"Generating '{self.report_type}' report in directory: '{output_dir}'"
        )

        # Create the output folder
        if create_folder(output_dir, is_nested=True):
            self.report.logger.info(f"Created output directory: '{output_dir}'")
        else:
            self.report.logger.info(f"Output directory already existed: '{output_dir}'")

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
            self.report.logger.debug("Processing app navigation code.")
            # Define the Streamlit imports and report manager content
            report_manag_content = []
            if self.report.logo:
                report_manag_content.append(
                    f"""import streamlit as st\n
st.set_page_config(layout="wide", page_title="{self.report.title}", page_icon="{self.report.logo}")
st.logo("{self.report.logo}")"""
                )
            else:
                report_manag_content.append(
                    f"""import streamlit as st\n
st.set_page_config(layout="wide", page_title="{self.report.title}")"""
                )
            report_manag_content.append(
                self._format_text(
                    text=self.report.title, type="header", level=1, color="#023858"
                )
            )

            # Initialize a dictionary to store the navigation structure
            report_manag_content.append("\nsections_pages = {}")

            # Generate the home page and update the report manager content
            self._generate_home_section(
                output_dir=output_dir, report_manag_content=report_manag_content
            )

            for section in self.report.sections:
                # Create a folder for each section
                subsection_page_vars = []
                section_name_var = section.title.replace(" ", "_")
                section_dir_path = Path(output_dir) / section_name_var

                if create_folder(section_dir_path):
                    self.report.logger.debug(
                        f"Created section directory: {section_dir_path}"
                    )
                else:
                    self.report.logger.debug(
                        f"Section directory already existed: {section_dir_path}"
                    )

                for subsection in section.subsections:
                    subsection_name_var = subsection.title.replace(" ", "_")
                    subsection_file_path = (
                        Path(section_name_var) / f"{subsection_name_var}.py"
                    ).as_posix()  # Make sure it's Posix Paths

                    # Create a Page object for each subsection and add it to the home page content
                    report_manag_content.append(
                        f"{subsection_name_var} = st.Page('{subsection_file_path}', title='{subsection.title}')"
                    )
                    subsection_page_vars.append(subsection_name_var)

                # Add all subsection Page objects to the corresponding section
                report_manag_content.append(
                    f"sections_pages['{section.title}'] = [{', '.join(subsection_page_vars)}]\n"
                )

            # Add navigation object to the home page content
            report_manag_content.append(
                f"""report_nav = st.navigation(sections_pages)
report_nav.run()"""
            )

            # Write the navigation and general content to a Python file
            with open(Path(output_dir) / self.REPORT_MANAG_SCRIPT, "w") as nav_manager:
                nav_manager.write("\n".join(report_manag_content))
                self.report.logger.info(
                    f"Created app navigation script: {self.REPORT_MANAG_SCRIPT}"
                )

            # Create Python files for each section and its subsections and plots
            self._generate_sections(output_dir=output_dir, static_dir=static_dir)
        except Exception as e:
            self.report.logger.error(
                f"An error occurred while generating the report: {str(e)}"
            )
            raise

    def run_report(self, output_dir: str = SECTIONS_DIR) -> None:
        """
        Runs the generated Streamlit report.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the report was generated (default is SECTIONS_DIR).
        """
        if self.streamlit_autorun:
            self.report.logger.info(
                f"Running '{self.report.title}' {self.report_type} report."
            )
            self.report.logger.debug(
                f"Running Streamlit report from directory: {output_dir}"
            )
            # ! using pyinstaller: vuegen main script as executable, not the Python Interpreter
            msg = f"{sys.executable = }"
            self.report.logger.debug(msg)
            try:
                # ! streamlit  command option is not known in packaged app
                target_file = os.path.join(output_dir, self.REPORT_MANAG_SCRIPT)
                self.report.logger.debug(
                    f"Running Streamlit report from file: {target_file}"
                )
                if self.BUNDLED_EXECUTION:
                    args = [
                        "streamlit",
                        "run",
                        target_file,
                        "--global.developmentMode=false",
                    ]
                    sys.argv = args

                    sys.exit(stcli.main())
                else:
                    self.report.logger.debug("Run using subprocess.")
                    subprocess.run(
                        [sys.executable, "-m", "streamlit", "run", target_file],
                        check=True,
                    )
            except KeyboardInterrupt:
                print("Streamlit process interrupted.")
            except subprocess.CalledProcessError as e:
                self.report.logger.error(f"Error running Streamlit report: {str(e)}")
                raise
        else:
            # If autorun is False, print instructions for manual execution
            self.report.logger.info(
                f"All the scripts to build the Streamlit app are available at {output_dir}"
            )
            self.report.logger.info(
                f"To run the Streamlit app, use the following command:"
            )
            self.report.logger.info(
                f"streamlit run {Path(output_dir) / self.REPORT_MANAG_SCRIPT}"
            )
            msg = (
                f"\nAll the scripts to build the Streamlit app are available at: {output_dir}\n\n"
                f"To run the Streamlit app, use the following command:\n\n"
                f"\tstreamlit run {Path(output_dir) / self.REPORT_MANAG_SCRIPT}"
            )
            print(msg)

    def _format_text(
        self,
        text: str,
        type: str,
        level: int = 1,
        color: str = "#000000",
        text_align: str = "center",
    ) -> str:
        """
        Generates a Streamlit markdown text string with the specified level and color.

        Parameters
        ----------
        text : str
            The text to be formatted.
        type : str
            The type of the text (e.g., 'header', 'paragraph').
        level : int, optional
            If the text is a header, the level of the header (e.g., 1 for h1, 2 for h2, etc.).
        color : str, optional
            The color of the header text.
        text_align : str, optional
            The text alignment.

        Returns
        -------
        str
            A formatted markdown string for the specified text.
        """
        if type == "header":
            tag = f"h{level}"
        elif type == "paragraph":
            tag = "p"

        return f"""st.markdown('''<{tag} style='text-align: {text_align}; color: {color};'>{text}</{tag}>''', unsafe_allow_html=True)"""

    def _generate_home_section(
        self, output_dir: str, report_manag_content: list
    ) -> None:
        """
        Generates the homepage for the report and updates the report manager content.

        Parameters
        ----------
        output_dir : str
            The folder where the homepage files will be saved.
        report_manag_content : list
            A list to store the content that will be written to the report manager file.
        """
        self.report.logger.debug("Processing home section.")

        try:
            # Create folder for the home page
            home_dir_path = Path(output_dir) / "Home"
            if create_folder(home_dir_path):
                self.report.logger.debug(f"Created home directory: {home_dir_path}")
            else:
                self.report.logger.debug(
                    f"Home directory already existed: {home_dir_path}"
                )

            # Create the home page content
            home_content = []
            home_content.append(f"import streamlit as st")
            if self.report.description:
                home_content.append(
                    self._format_text(text=self.report.description, type="paragraph")
                )
            if self.report.graphical_abstract:
                home_content.append(
                    f"\nst.image('{self.report.graphical_abstract}', use_column_width=True)"
                )

            # Define the footer variable and add it to the home page content
            home_content.append("footer = '''" + generate_footer() + "'''\n")
            home_content.append("st.markdown(footer, unsafe_allow_html=True)\n")

            # Write the home page content to a Python file
            home_page_path = Path(home_dir_path) / "Homepage.py"
            with open(home_page_path, "w") as home_page:
                home_page.write("\n".join(home_content))
            self.report.logger.info(f"Home page content written to '{home_page_path}'.")

            # Add the home page to the report manager content
            report_manag_content.append(
                f"homepage = st.Page('Home/Homepage.py', title='Homepage')"  # ! here Posix Path is hardcoded
            )
            report_manag_content.append(f"sections_pages['Home'] = [homepage]\n")
            self.report.logger.info("Home page added to the report manager content.")
        except Exception as e:
            self.report.logger.error(f"Error generating the home section: {str(e)}")
            raise

    def _generate_sections(self, output_dir: str, static_dir: str) -> None:
        """
        Generates Python files for each section in the report, including subsections and its components (plots, dataframes, markdown).

        Parameters
        ----------
        output_dir : str
            The folder where section files will be saved.
        static_dir : str
            The folder where the static files will be saved.
        """
        self.report.logger.info("Starting to generate sections for the report.")

        try:
            for section in self.report.sections:
                section_name_var = section.title.replace(" ", "_")
                self.report.logger.debug(
                    f"Processing section '{section.id}': '{section.title}' - {len(section.subsections)} subsection(s)"
                )

                if section.subsections:
                    # Iterate through subsections and integrate them into the section file
                    for subsection in section.subsections:
                        self.report.logger.debug(
                            f"Processing subsection '{subsection.id}': '{subsection.title} - {len(subsection.components)} component(s)'"
                        )
                        try:
                            # Create subsection file
                            subsection_file_path = (
                                Path(output_dir)
                                / section_name_var
                                / f"{subsection.title.replace(' ', '_')}.py"
                            )

                            # Generate content and imports for the subsection
                            subsection_content, subsection_imports = (
                                self._generate_subsection(
                                    subsection, static_dir=static_dir
                                )
                            )

                            # Flatten the subsection_imports into a single list
                            flattened_subsection_imports = [
                                imp for sublist in subsection_imports for imp in sublist
                            ]

                            # Remove duplicated imports
                            unique_imports = list(set(flattened_subsection_imports))

                            # Write everything to the subsection file
                            with open(subsection_file_path, "w") as subsection_file:
                                # Write imports at the top of the file
                                subsection_file.write(
                                    "\n".join(unique_imports) + "\n\n"
                                )

                                # Write the subsection content (descriptions, plots)
                                subsection_file.write("\n".join(subsection_content))

                            self.report.logger.info(
                                f"Subsection file created: '{subsection_file_path}'"
                            )
                        except Exception as subsection_error:
                            self.report.logger.error(
                                f"Error processing subsection '{subsection.id}' '{subsection.title}' in section  '{section.id}' '{section.title}': {str(subsection_error)}"
                            )
                            raise
                else:
                    self.report.logger.warning(
                        f"No subsections found in section: '{section.title}'. To show content in the report, add subsections to the section."
                    )
        except Exception as e:
            self.report.logger.error(f"Error generating sections: {str(e)}")
            raise

    def _generate_subsection(
        self, subsection, static_dir
    ) -> tuple[List[str], List[str]]:
        """
        Generate code to render components (plots, dataframes, markdown) in the given subsection,
        creating imports and content for the subsection based on the component type.

        Parameters
        ----------
        subsection : Subsection
            The subsection containing the components.
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
        subsection_content.append(
            self._format_text(
                text=subsection.title, type="header", level=3, color="#023558"
            )
        )
        if subsection.description:
            subsection_content.append(
                self._format_text(text=subsection.description, type="paragraph")
            )

        for component in subsection.components:
            # Write imports if not already done
            component_imports = self._generate_component_imports(component)
            subsection_imports.append(component_imports)

            # Handle different types of components
            if component.component_type == r.ComponentType.PLOT:
                subsection_content.extend(
                    self._generate_plot_content(component, static_dir=static_dir)
                )
            elif component.component_type == r.ComponentType.DATAFRAME:
                subsection_content.extend(self._generate_dataframe_content(component))
            # If md files is called "description.md", do not include it in the report
            elif (
                component.component_type == r.ComponentType.MARKDOWN
                and component.title.lower() != "description"
            ):
                subsection_content.extend(self._generate_markdown_content(component))
            elif component.component_type == r.ComponentType.HTML:
                subsection_content.extend(self._generate_html_content(component))
            elif component.component_type == r.ComponentType.APICALL:
                subsection_content.extend(self._generate_apicall_content(component))
            elif component.component_type == r.ComponentType.CHATBOT:
                subsection_content.extend(self._generate_chatbot_content(component))
            else:
                self.report.logger.warning(
                    f"Unsupported component type '{component.component_type}' in subsection: {subsection.title}"
                )

        # Define the footer variable and add it to the home page content
        subsection_content.append("footer = '''" + generate_footer() + "'''\n")
        subsection_content.append("st.markdown(footer, unsafe_allow_html=True)\n")

        self.report.logger.info(
            f"Generated content and imports for subsection: '{subsection.title}'"
        )
        return subsection_content, subsection_imports

    def _generate_plot_content(self, plot, static_dir: str) -> List[str]:
        """
        Generate content for a plot component based on the plot type (static or interactive).

        Parameters
        ----------
        plot : Plot
            The plot component to generate content for.

        Returns
        -------
        list : List[str]
            The list of content lines for the plot.
        static_dir : str
            The folder where the static files will be saved.
        """
        plot_content = []
        # Add title
        plot_content.append(
            self._format_text(text=plot.title, type="header", level=4, color="#2b8cbe")
        )

        # Add content for the different plot types
        try:
            if plot.plot_type == r.PlotType.STATIC:
                plot_content.append(
                    f"\nst.image('{plot.file_path}', caption='{plot.caption}', use_column_width=True)\n"
                )
            elif plot.plot_type == r.PlotType.PLOTLY:
                plot_content.append(self._generate_plot_code(plot))
            elif plot.plot_type == r.PlotType.ALTAIR:
                plot_content.append(self._generate_plot_code(plot))
            elif plot.plot_type == r.PlotType.INTERACTIVE_NETWORK:
                networkx_graph = plot.read_network()
                if isinstance(networkx_graph, tuple):
                    # If network_data is a tuple, separate the network and html file path
                    networkx_graph, html_plot_file = networkx_graph
                else:
                    # Otherwise, create and save a new pyvis network from the netowrkx graph
                    html_plot_file = (
                        Path(static_dir) / f"{plot.title.replace(' ', '_')}.html"
                    )
                    pyvis_graph = plot.create_and_save_pyvis_network(
                        networkx_graph, html_plot_file
                    )

                # Add number of nodes and edges to the plor conetnt
                num_nodes = networkx_graph.number_of_nodes()
                num_edges = networkx_graph.number_of_edges()

                # Determine whether the file path is a URL or a local file
                if is_url(html_plot_file):
                    plot_content.append(
                        f"""
response = requests.get('{html_plot_file}')
response.raise_for_status()
html_data = response.text\n"""
                    )
                else:
                    plot_content.append(
                        f"""
with open('{html_plot_file}', 'r') as f:
    html_data = f.read()\n"""
                    )

                # Append the code for additional information (nodes and edges count)
                plot_content.append(
                    f"""
st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of nodes:</b> {num_nodes} </p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of relationships:</b> {num_edges} </p>", unsafe_allow_html=True)\n"""
                )

                # Add the specific code for visualization
                plot_content.append(self._generate_plot_code(plot))
            else:
                self.report.logger.warning(f"Unsupported plot type: {plot.plot_type}")
        except Exception as e:
            self.report.logger.error(
                f"Error generating content for '{plot.plot_type}' plot '{plot.id}' '{plot.title}': {str(e)}"
            )
            raise

        self.report.logger.info(
            f"Successfully generated content for plot '{plot.id}': '{plot.title}'"
        )
        return plot_content

    def _generate_plot_code(self, plot) -> str:
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
        # If the file path is a URL, generate code to fetch content via requests
        if is_url(plot.file_path):
            plot_code = f"""
response = requests.get('{plot.file_path}')
response.raise_for_status()
plot_json = json.loads(response.text)\n"""
        else:  # If it's a local file
            plot_code = f"""
with open('{Path(plot.file_path).as_posix()}', 'r') as plot_file:
    plot_json = json.load(plot_file)\n"""

        # Add specific code for each visualization tool
        if plot.plot_type == r.PlotType.PLOTLY:
            plot_code += "st.plotly_chart(plot_json, use_container_width=True)\n"

        elif plot.plot_type == r.PlotType.ALTAIR:
            plot_code += """
altair_plot = alt.Chart.from_dict(plot_json)
st.vega_lite_chart(json.loads(altair_plot.to_json()), use_container_width=True)\n"""

        elif plot.plot_type == r.PlotType.INTERACTIVE_NETWORK:
            plot_code = """# Streamlit checkbox for controlling the layout
control_layout = st.checkbox('Add panel to control layout', value=True)
net_html_height = 1200 if control_layout else 630
# Load HTML into HTML component for display on Streamlit
st.components.v1.html(html_data, height=net_html_height)\n"""
        return plot_code

    def _generate_dataframe_content(self, dataframe) -> List[str]:
        """
        Generate content for a DataFrame component.

        Parameters
        ----------
        dataframe : DataFrame
            The dataframe component to generate content for.

        Returns
        -------
        list : List[str]
            The list of content lines for the DataFrame.
        """
        dataframe_content = []
        # Add title
        dataframe_content.append(
            self._format_text(
                text=dataframe.title, type="header", level=4, color="#2b8cbe"
            )
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

            # Load the DataFrame using the correct function
            read_function = read_function_mapping[file_extension]
            dataframe_content.append(
                f"""df = pd.{read_function.__name__}('{dataframe.file_path}')\n"""
            )

            # Displays a DataFrame using AgGrid with configurable options.
            dataframe_content.append(
                """
# Displays a DataFrame using AgGrid with configurable options.
grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_builder.configure_default_column(editable=True, groupable=True)
grid_builder.configure_side_bar(filters_panel=True, columns_panel=True)
grid_builder.configure_selection(selection_mode="multiple")
grid_builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=20)
grid_options = grid_builder.build()

AgGrid(df, gridOptions=grid_options)

# Button to download the df
df_csv = df.to_csv(sep=',', header=True, index=False).encode('utf-8')
st.download_button(
    label="Download dataframe as CSV",
    data=df_csv,
    file_name=f"dataframe_{df_index}.csv",
    mime='text/csv',
    key=f"download_button_{df_index}")
df_index += 1"""
            )
        except Exception as e:
            self.report.logger.error(
                f"Error generating content for DataFrame: {dataframe.title}. Error: {str(e)}"
            )
            raise

        # Add caption if available
        if dataframe.caption:
            dataframe_content.append(
                self._format_text(
                    text=dataframe.caption, type="caption", text_align="left"
                )
            )

        self.report.logger.info(
            f"Successfully generated content for DataFrame: '{dataframe.title}'"
        )
        return dataframe_content

    def _generate_markdown_content(self, markdown) -> List[str]:
        """
        Generate content for a Markdown component.

        Parameters
        ----------
        markdown : MARKDOWN
            The markdown component to generate content for.

        Returns
        -------
        list : List[str]
            The list of content lines for the markdown.
        """
        markdown_content = []

        # Add title
        markdown_content.append(
            self._format_text(
                text=markdown.title, type="header", level=4, color="#2b8cbe"
            )
        )
        try:
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
            markdown_content.append(
                "st.markdown(markdown_content, unsafe_allow_html=True)\n"
            )
        except Exception as e:
            self.report.logger.error(
                f"Error generating content for Markdown: {markdown.title}. Error: {str(e)}"
            )
            raise

        # Add caption if available
        if markdown.caption:
            markdown_content.append(
                self._format_text(
                    text=markdown.caption, type="caption", text_align="left"
                )
            )

        self.report.logger.info(
            f"Successfully generated content for Markdown: '{markdown.title}'"
        )
        return markdown_content

    def _generate_html_content(self, html) -> List[str]:
        """
        Generate content for an HTML component in a Streamlit app.

        Parameters
        ----------
        html : HTML
            The HTML component to generate content for.

        Returns
        -------
        list : List[str]
            The list of content lines for the HTML display.
        """
        html_content = []

        # Add title
        html_content.append(
            self._format_text(text=html.title, type="header", level=4, color="#2b8cbe")
        )

        try:
            if is_url(html.file_path):
                # If it's a URL, fetch content dynamically
                html_content.append(
                    f"""
response = requests.get('{html.file_path}')
response.raise_for_status()
html_content = response.text\n"""
                )
            else:
                # If it's a local file
                html_content.append(
                    f"""
with open('{(Path("..") / html.file_path).as_posix()}', 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()\n"""
                )

            # Display HTML content using Streamlit
            html_content.append(
                "st.components.v1.html(html_content, height=600, scrolling=True)\n"
            )

        except Exception as e:
            self.report.logger.error(
                f"Error generating content for HTML: {html.title}. Error: {str(e)}"
            )
            raise

        # Add caption if available
        if html.caption:
            html_content.append(
                self._format_text(text=html.caption, type="caption", text_align="left")
            )

        self.report.logger.info(
            f"Successfully generated content for HTML: '{html.title}'"
        )
        return html_content

    def _generate_apicall_content(self, apicall) -> List[str]:
        """
        Generate content for a Markdown component.

        Parameters
        ----------
        apicall : APICall
            The apicall component to generate content for.

        Returns
        -------
        list : List[str]
            The list of content lines for the apicall.
        """
        apicall_content = []

        # Add tile
        apicall_content.append(
            self._format_text(
                text=apicall.title, type="header", level=4, color="#2b8cbe"
            )
        )
        try:
            apicall_response = apicall.make_api_request(method="GET")
            apicall_content.append(f"""st.write({apicall_response})\n""")
        except Exception as e:
            self.report.logger.error(
                f"Error generating content for APICall: {apicall.title}. Error: {str(e)}"
            )
            raise

        # Add caption if available
        if apicall.caption:
            apicall_content.append(
                self._format_text(
                    text=apicall.caption, type="caption", text_align="left"
                )
            )

        self.report.logger.info(
            f"Successfully generated content for APICall: '{apicall.title}'"
        )
        return apicall_content

    def _generate_chatbot_content(self, chatbot) -> List[str]:
        """
        Generate content for a ChatBot component.

        Parameters
        ----------
        chatbot : ChatBot
            The ChatBot component to generate content for.

        Returns
        -------
        list : List[str]
            The list of content lines for the ChatBot.
        """
        chatbot_content = []

        # Add title
        chatbot_content.append(
            self._format_text(
                text=chatbot.title, type="header", level=4, color="#2b8cbe"
            )
        )

        # Chatbot logic for embedding in the web application
        chatbot_content.append(
            f"""
def generate_query(messages):
    response = requests.post(
        "{chatbot.api_call.api_url}",
        json={{"model": "{chatbot.model}", "messages": messages, "stream": True}},
    )
    response.raise_for_status()
    return response               

def parse_api_response(response):
    try:
        output = ""
        for line in response.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(f"API error: {{body['error']}}")
            if body.get("done", False):
                return {{"role": "assistant", "content": output}}
            output += body.get("message", {{}}).get("content", "")
    except Exception as e:
        return {{"role": "assistant", "content": f"Error while processing API response: {{str(e)}}"}}

def response_generator(msg_content):
    for word in msg_content.split():
        yield word + " "
        time.sleep(0.1)
    yield "\\n"

# Chatbot interaction in the app
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Display chat history
for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.write(message['content'])

# Handle new input from the user
if prompt := st.chat_input("Enter your prompt here:"):
    # Add user's question to the session state                           
    st.session_state.messages.append({{"role": "user", "content": prompt}})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Retrieve question and generate answer
    combined = "\\n".join(msg["content"] for msg in st.session_state.messages if msg["role"] == "user")
    messages = [{{"role": "user", "content": combined}}]
    with st.spinner('Generating answer...'):                       
        response = generate_query(messages)
        parsed_response = parse_api_response(response)
                               
    # Add the assistant's response to the session state and display it
    st.session_state.messages.append(parsed_response)
    with st.chat_message("assistant"):
        st.write_stream(response_generator(parsed_response["content"]))
    """
        )

        # Add caption if available
        if chatbot.caption:
            chatbot_content.append(
                self._format_text(
                    text=chatbot.caption, type="caption", text_align="left"
                )
            )

        self.report.logger.info(
            f"Successfully generated content for ChatBot: '{chatbot.title}'"
        )
        return chatbot_content

    def _generate_component_imports(self, component: r.Component) -> List[str]:
        """
        Generate necessary imports for a component of the report.

        Parameters
        ----------
        component : r.Component
            The component for which to generate the required imports. The component can be of type:
            - PLOT
            - DATAFRAME

        Returns
        -------
        list : List[str]
            A list of import statements for the component.
        """
        # Dictionary to hold the imports for each component type
        components_imports = {
            "plot": {
                r.PlotType.ALTAIR: [
                    "import json",
                    "import altair as alt",
                    "import requests",
                ],
                r.PlotType.PLOTLY: ["import json", "import requests"],
                r.PlotType.INTERACTIVE_NETWORK: ["import requests"],
            },
            "dataframe": [
                "import pandas as pd",
                "from st_aggrid import AgGrid, GridOptionsBuilder",
            ],
            "markdown": ["import requests"],
            "chatbot": ["import time", "import json", "import requests"],
        }

        component_type = component.component_type
        component_imports = ["import streamlit as st"]

        # Add relevant imports based on component type and visualization tool
        if component_type == r.ComponentType.PLOT:
            plot_type = getattr(component, "plot_type", None)
            if plot_type in components_imports["plot"]:
                component_imports.extend(components_imports["plot"][plot_type])
        elif component_type == r.ComponentType.MARKDOWN:
            component_imports.extend(components_imports["markdown"])
        elif component_type == r.ComponentType.CHATBOT:
            component_imports.extend(components_imports["chatbot"])
        elif component_type == r.ComponentType.DATAFRAME:
            component_imports.extend(components_imports["dataframe"])
            component_imports.append("df_index = 1")

        # Return the list of import statements
        return component_imports

        return component_imports
