"""
StreamlitReportView class for generating Streamlit reports
based on a configuration file.
"""

import os
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import List

from streamlit.web import cli as stcli

from . import report as r
from . import table_utils
from .utils import (
    create_folder,
    generate_footer,
    get_relative_file_path,
    is_url,
    sort_imports,
)
from .utils.variables import make_valid_identifier


def write_python_file(fpath: str, imports: list[str], contents: list[str]) -> None:
    """Write a Python file with the given imports and contents."""
    with open(fpath, "w", encoding="utf-8") as f:
        # Write imports at the top of the file
        f.write("\n".join(imports) + "\n\n")

        # Write the subsection content (descriptions, plots)
        f.write("\n".join(contents))


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
        static_dir: str = STATIC_FILES_DIR,
        sections_dir: str = SECTIONS_DIR,
    ):
        """Initialize ReportView with the report and report type.

        Parameters
        ----------
        report : r.Report
            Report dataclass with all the information to be included in the report.
            Contains sections data needed to write the report python files.
        report_type : r.ReportType
            Enum of report type as definded by the ReportType Enum.
        streamlit_autorun : bool, optional
            Wheather streamlit should be started after report generation,
            by default False
        static_dir : str, optional
            The folder where the static files will be saved,
            by default STATIC_FILES_DIR.
        """
        super().__init__(report=report, report_type=report_type)
        self.streamlit_autorun = streamlit_autorun
        self.bundled_execution = False
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            self.report.logger.info("running in a PyInstaller bundle")
            self.bundled_execution = True
        else:
            self.report.logger.info("running in a normal Python process")

        self.components_fct_map = {
            r.ComponentType.PLOT: self._generate_plot_content,
            r.ComponentType.DATAFRAME: self._generate_dataframe_content,
            r.ComponentType.MARKDOWN: self._generate_markdown_content,
            r.ComponentType.HTML: self._generate_html_content,
            r.ComponentType.APICALL: self._generate_apicall_content,
            r.ComponentType.CHATBOT: self._generate_chatbot_content,
        }

        self.static_dir = static_dir
        self.section_dir = sections_dir

    def generate_report(self, output_dir: str = None) -> None:
        """
        Generates the Streamlit report and creates Python files for each section
        and its subsections and plots.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the generated report files will be saved
            (default is SECTIONS_DIR).
        """
        if output_dir is not None:
            # ? does this imply changes to the static dir
            self.section_dir = Path(output_dir).resolve()
        output_dir = Path(self.section_dir)
        self.report.logger.debug(
            "Generating '%s' report in directory: '%s'", self.report_type, output_dir
        )

        # Create the output folder
        if create_folder(output_dir, is_nested=True):
            self.report.logger.info("Created output directory: '%s'", output_dir)
        else:
            self.report.logger.info(
                "Output directory already existed: '%s'", output_dir
            )

        # Create the static folder
        if create_folder(self.static_dir):
            self.report.logger.info(
                "Created output directory for static content: '%s'", self.static_dir
            )
        else:
            self.report.logger.info(
                "Output directory for static content already existed: '%s'",
                self.static_dir,
            )

        try:
            self.report.logger.debug("Processing app navigation code.")
            # Define the Streamlit imports and report manager content
            report_manag_content = []
            report_manag_content.append(
                textwrap.dedent(
                    """\
                    import os
                    import time

                    import psutil
                    import streamlit as st
                    """
                )
            )
            if self.report.logo:
                report_manag_content.append(
                    textwrap.dedent(
                        f"""\
                        st.set_page_config(layout="wide",
                                           page_title="{self.report.title}",
                                           page_icon="{self.report.logo}"
                        )
                        st.logo("{self.report.logo}")
                        """
                    )
                )
            else:
                report_manag_content.append(
                    textwrap.dedent(
                        f"""\
                        st.set_page_config(layout="wide",
                                           page_title="{self.report.title}")
                        """
                    )
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
                output_dir=output_dir,
                report_manag_content=report_manag_content,
            )

            for section in self.report.sections:
                # Create a folder for each section
                subsection_page_vars = []
                section_name_var = make_valid_identifier(
                    section.title.replace(" ", "_")
                )
                section_dir_path = Path(output_dir) / section_name_var

                if create_folder(section_dir_path):
                    self.report.logger.debug(
                        "Created section directory: %s", section_dir_path
                    )
                else:
                    self.report.logger.debug(
                        "Section directory already existed: %s", section_dir_path
                    )
                # add an overview page to section for it's section components
                # they will be written when the components are parsed
                # using `_generate_sections`
                if section.components:
                    _fname = (
                        f"0_overview_{make_valid_identifier(section.title).lower()}.py"
                    )
                    subsection_file_path = (
                        Path(section_name_var) / _fname
                    ).as_posix()  # Make sure it's Posix Paths
                    section.file_path = subsection_file_path
                    # Create a Page object for each subsection and
                    # add it to the home page content
                    report_manag_content.append(
                        f"{section_name_var}_overview = "
                        f"st.Page('{subsection_file_path}'"
                        f", title='Overview {section.title}')"
                    )
                    subsection_page_vars.append(f"{section_name_var}_overview")

                for subsection in section.subsections:
                    # ! could add a non-integer to ensure it's a valid identifier
                    subsection_name_var = make_valid_identifier(subsection.title)
                    if not subsection_name_var.isidentifier():
                        msg = (
                            "Subsection name is not a valid Python identifier: "
                            f"{subsection_name_var}"
                        )
                        self.report.logger.error(msg)
                        raise ValueError(
                            msg,
                        )
                    subsection_file_path = (
                        Path(section_name_var) / f"{subsection_name_var}.py"
                    ).as_posix()  # Make sure it's Posix Paths
                    subsection.file_path = subsection_file_path
                    # Create a Page object for each subsection and
                    # add it to the home page content
                    report_manag_content.append(
                        f"{subsection_name_var} = st.Page('{subsection_file_path}', "
                        f"title='{subsection.title}')"
                    )
                    subsection_page_vars.append(subsection_name_var)

                # Add all subsection Page objects to the corresponding section
                report_manag_content.append(
                    f"sections_pages['{section.title}'] = "
                    f"[{', '.join(subsection_page_vars)}]\n"
                )

            # Add navigation object to the home page content
            report_manag_content.append(
                textwrap.dedent(
                    """\
                    report_nav = st.navigation(sections_pages)

                    # Following https://discuss.streamlit.io/t/\
close-streamlit-app-with-button-click/35132/5
                    exit_app = st.sidebar.button("Shut Down App",
                                                 icon=":material/power_off:",
                                                 use_container_width=True)
                    if exit_app:
                        st.toast("Shutting down the app...")
                        time.sleep(1)
                        # Terminate streamlit python process
                        pid = os.getpid()
                        p = psutil.Process(pid)
                        p.terminate()


                    report_nav.run()
                    """
                )
            )

            # Write the navigation and general content to a Python file
            with open(
                Path(output_dir) / self.REPORT_MANAG_SCRIPT, "w", encoding="utf8"
            ) as nav_manager:
                nav_manager.write("\n".join(report_manag_content))
                self.report.logger.info(
                    "Created app navigation script: %s", self.REPORT_MANAG_SCRIPT
                )

            # Create Python files for each section and its subsections and plots
            self._generate_sections(output_dir=output_dir)

            # Save README.md to the output directory
            fpath = self.section_dir.parent / "README.md"
            with open(fpath, "w", encoding="utf-8") as f:

                f.write(
                    textwrap.dedent(
                        f"""\
                    # Streamlit Report

                    This report was generated using the Vuegen library:
                    https://github.com/Multiomics-Analytics-Group/vuegen

                    Executed from: `{Path.cwd()}`

                    Written to: `{self.section_dir.resolve()}`

                    Folder cannot be moved from above path, but can be executed
                    from anywhere on the system.
                    """
                    )
                )

        except Exception as e:
            self.report.logger.error(
                "An error occurred while generating the report: %s",
                e,
                exc_info=True,
            )
            raise

    def run_report(self, output_dir: str = None) -> None:
        """
        Runs the generated Streamlit report.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the report was generated (default is SECTIONS_DIR).
        """
        if output_dir is not None:
            self.report.logger.warning("The output_dir parameter is deprecated.")
        output_dir = Path(self.section_dir)
        if self.streamlit_autorun:
            self.report.logger.info(
                "Running '%s' %s report.", self.report.title, self.report_type
            )
            self.report.logger.debug(
                "Running Streamlit report from directory: %s", output_dir
            )
            # ! using pyinstaller: vuegen main script as executable,
            # ! not the Python Interpreter
            msg = f"{sys.executable = }"
            self.report.logger.debug(msg)
            try:
                # ! streamlit  command option is not known in packaged app
                target_file = os.path.join(output_dir, self.REPORT_MANAG_SCRIPT)
                self.report.logger.debug(
                    "Running Streamlit report from file: %s", target_file
                )
                if self.bundled_execution:
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
                self.report.logger.error(
                    "Error running Streamlit report: %s", e, exc_info=True
                )
                raise
        else:
            # If autorun is False, print instructions for manual execution
            self.report.logger.info(
                "All the scripts to build the Streamlit app are available at %s",
                output_dir,
            )
            self.report.logger.info(
                "To run the Streamlit app, use the following command:"
            )
            self.report.logger.info(
                "streamlit run %s", Path(output_dir) / self.REPORT_MANAG_SCRIPT
            )
            msg = (
                "\nAll the scripts to build the Streamlit app are available at: "
                f"{output_dir}\n\n"
                "To run the Streamlit app, use the following command:\n\n"
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
            If the text is a header, the level of the header
            (e.g., 1 for h1, 2 for h2, etc.).
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
        elif type == "paragraph" or type == "caption":
            tag = "p"
        else:
            raise ValueError(
                f"Unsupported text type: {type}. Supported types are 'header', "
                "'paragraph', and 'caption'."
            )

        text = text.strip()  # get rid of new lines
        text = textwrap.indent(text, "                ")
        ret = textwrap.dedent(
            f"""\
            st.markdown(
                '''
                <{tag} style='text-align: {text_align};
                color: {color};'>\n{text}
                </{tag}>
                ''',
                unsafe_allow_html=True)
            """
        )
        return ret

    def _generate_home_section(
        self,
        output_dir: str,
        report_manag_content: list,
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
                self.report.logger.debug("Created home directory: %s", home_dir_path)
            else:
                self.report.logger.debug(
                    "Home directory already existed: %s", home_dir_path
                )

            # Create the home page content
            home_content = []
            home_content.append("import streamlit as st")
            if self.report.description:
                home_content.append(
                    self._format_text(text=self.report.description, type="paragraph")
                )
            if self.report.graphical_abstract:
                home_content.append(
                    f"\nst.image('{self.report.graphical_abstract}', "
                    "use_column_width=True)"
                )

            # add components content to page (if any)

            # Define the footer variable and add it to the home page content
            home_content.append("footer = '''" + generate_footer() + "'''\n")
            home_content.append("st.markdown(footer, unsafe_allow_html=True)\n")

            # Write the home page content to a Python file
            home_page_path = Path(home_dir_path) / "Homepage.py"
            with open(home_page_path, "w", encoding="utf-8") as home_page:
                home_page.write("\n".join(home_content))
            self.report.logger.info(
                "Home page content written to '%s'.", home_page_path
            )

            # Add the home page to the report manager content
            report_manag_content.append(
                # ! here Posix Path is hardcoded
                "homepage = st.Page('Home/Homepage.py', title='Homepage')"
            )
            report_manag_content.append("sections_pages['Home'] = [homepage]\n")
            self.report.logger.info("Home page added to the report manager content.")
        except Exception as e:
            self.report.logger.error(
                "Error generating the home section: %s", e, exc_info=True
            )
            raise

    def _generate_sections(self, output_dir: str) -> None:
        """
        Generates Python files for each section in the report, including subsections
        and its components (plots, dataframes, markdown).

        Parameters
        ----------
        output_dir : str
            The folder where section files will be saved.
        """
        self.report.logger.info("Starting to generate sections for the report.")
        try:
            for section in self.report.sections:
                self.report.logger.debug(
                    # Continue
                    "Processing section '%s': '%s' - %s subsection(s)",
                    section.id,
                    section.title,
                    len(section.subsections),
                )
                if section.components:
                    # add an section overview page
                    section_content, section_imports, _ = self._combine_components(
                        section.components
                    )
                    assert (
                        section.file_path is not None
                    ), "Missing relative file path to overview page in section"
                    write_python_file(
                        fpath=Path(output_dir) / section.file_path,
                        imports=section_imports,
                        contents=section_content,
                    )

                if not section.subsections:
                    self.report.logger.debug(
                        "No subsections found in section: '%s'.", section.title
                    )
                    continue

                # Iterate through subsections and integrate them into the section file
                # ! subsection should have the subsection_file_path as file_path,
                # ! which is set when parsing the config in the main generate_sections
                # ! method
                for subsection in section.subsections:
                    self.report.logger.debug(
                        "Processing subsection '%s': '%s' - %s component(s)",
                        subsection.id,
                        subsection.title,
                        len(subsection.components),
                    )
                    try:
                        # Create subsection file
                        assert (
                            subsection.file_path is not None
                        ), "Missing relative file path to subsection"
                        subsection_file_path = Path(output_dir) / subsection.file_path
                        # Generate content and imports for the subsection
                        subsection_content, subsection_imports = (
                            self._generate_subsection(subsection)
                        )

                        write_python_file(
                            fpath=subsection_file_path,
                            imports=subsection_imports,
                            contents=subsection_content,
                        )
                        self.report.logger.info(
                            "Subsection file created: '%s'", subsection_file_path
                        )
                    except Exception as subsection_error:
                        self.report.logger.error(
                            "Error processing subsection '%s' '%s' "
                            "in section  '%s' '%s': %s",
                            subsection.id,
                            subsection.title,
                            section.id,
                            section.title,
                            str(subsection_error),
                        )
                        raise

        except Exception as e:
            self.report.logger.error("Error generating sections: %s", e, exc_info=True)
            raise

    def _combine_components(self, components: list[dict]) -> tuple[list, list, bool]:
        """combine a list of components."""

        all_contents = []
        all_imports = []
        has_chatbot = False

        for component in components:
            # Write imports if not already done
            component_imports = self._generate_component_imports(component)
            all_imports.extend(component_imports)

            # Handle different types of components
            fct = self.components_fct_map.get(component.component_type, None)
            if fct is None:
                self.report.logger.warning(
                    "Unsupported component type '%s' ", component.component_type
                )
            else:
                if component.component_type == r.ComponentType.CHATBOT:
                    has_chatbot = True
                content = fct(component)
                all_contents.extend(content)
        # remove duplicates
        all_imports = list(set(all_imports))
        all_imports, setup_statements = sort_imports(all_imports)
        all_imports.extend(setup_statements)
        return all_contents, all_imports, has_chatbot

    def _generate_subsection(self, subsection) -> tuple[List[str], List[str]]:
        """
        Generate code to render components (plots, dataframes, markdown) in the given
        subsection, creating imports and content for the subsection based on the
        component type.

        Parameters
        ----------
        subsection : Subsection
            The subsection containing the components.

        Returns
        -------
        tuple : (List[str], List[str])
            - list of subsection content lines (List[str])
            - list of imports for the subsection (List[str])
        """
        subsection_content = []

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
        all_components, subsection_imports, has_chatbot = self._combine_components(
            subsection.components
        )
        subsection_content.extend(all_components)

        if not has_chatbot:
            # Define the footer variable and add it to the home page content
            subsection_content.append("footer = '''" + generate_footer() + "'''\n")
            subsection_content.append("st.markdown(footer, unsafe_allow_html=True)\n")

        self.report.logger.info(
            "Generated content and imports for subsection: '%s'", subsection.title
        )
        return subsection_content, subsection_imports

    def _generate_plot_content(self, plot) -> List[str]:
        """
        Generate content for a plot component based on the plot type
        (static or interactive).

        Parameters
        ----------
        plot : Plot
            The plot component to generate content for.

        Returns
        -------
        list : List[str]
            The list of content lines for the plot.
        """
        plot_content = []
        # Add title
        plot_content.append(
            self._format_text(text=plot.title, type="header", level=4, color="#2b8cbe")
        )

        # Add content for the different plot types
        try:
            if plot.plot_type == r.PlotType.STATIC:
                # If the file path is a URL, keep the file path as is
                if is_url(plot.file_path):
                    plot_file_path = plot.file_path
                    plot_content.append(f"plot_file_path = '{plot_file_path}'")
                else:  # If it's a local file
                    plot_file_path = get_relative_file_path(
                        plot.file_path, relative_to=self.section_dir
                    ).as_posix()
                    plot_content.append(
                        f"plot_file_path = (section_dir / '{plot_file_path}')"
                        ".resolve().as_posix()"
                    )
                plot_content.append(
                    "st.image(plot_file_path,"
                    f" caption='{plot.caption}', use_column_width=True)\n"
                )
            elif plot.plot_type == r.PlotType.PLOTLY:
                plot_content.append(self._generate_plot_code(plot))
            elif plot.plot_type == r.PlotType.ALTAIR:
                plot_content.append(self._generate_plot_code(plot))
            elif plot.plot_type == r.PlotType.INTERACTIVE_NETWORK:
                networkx_graph = plot.read_network()
                if isinstance(networkx_graph, tuple):
                    # If network_data is a tuple, separate the network
                    # and html file path
                    networkx_graph, html_plot_file = networkx_graph
                else:
                    # Otherwise,
                    # create and save a new pyvis network from the netowrkx graph
                    html_plot_file = (
                        Path(self.static_dir) / f"{plot.title.replace(' ', '_')}.html"
                    ).resolve()
                    _ = plot.create_and_save_pyvis_network(
                        networkx_graph, html_plot_file
                    )

                # Add number of nodes and edges to the plot content
                num_nodes = networkx_graph.number_of_nodes()
                num_edges = networkx_graph.number_of_edges()

                # Determine whether the file path is a URL or a local file
                if is_url(html_plot_file):
                    plot_content.append(
                        textwrap.dedent(
                            f"""
                            response = requests.get('{html_plot_file}')
                            response.raise_for_status()
                            html_content = response.text
                            """
                        )
                    )
                else:
                    fpath = get_relative_file_path(
                        html_plot_file, relative_to=self.section_dir
                    ).as_posix()
                    plot_content.append(
                        textwrap.dedent(
                            f"""
                            file_path = (section_dir / '{fpath}').resolve().as_posix()
                            with open(file_path, 'r') as html_file:
                                html_content = html_file.read()
                            """
                        )
                    )

                # Append the code for additional information (nodes and edges count)
                plot_content.append(
                    textwrap.dedent(
                        f"""
                        st.markdown(("<p style='text-align: center; color: black;'> "
                                    "<b>Number of nodes:</b> {num_nodes} </p>"),
                                    unsafe_allow_html=True)
                        st.markdown(("<p style='text-align: center; color: black;'>"
                                     " <b>Number of relationships:</b> {num_edges}"
                                     " </p>"),
                                    unsafe_allow_html=True)
                        """
                    )
                )

                # Add the specific code for visualization
                plot_content.append(self._generate_plot_code(plot))
            else:
                self.report.logger.warning("Unsupported plot type: %s", plot.plot_type)
        except Exception as e:
            self.report.logger.error(
                "Error generating content for '%s' plot '%s' '%s': %s",
                plot.plot_type,
                plot.id,
                plot.title,
                e,
                exc_info=True,
            )
            raise

        self.report.logger.info(
            "Successfully generated content for plot '%s': '%s'",
            plot.id,
            plot.title,
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
            plot_code = textwrap.dedent(
                f"""
                response = requests.get('{plot.file_path}')
                response.raise_for_status()
                plot_json = json.loads(response.text)\n"""
            )
        else:  # If it's a local file
            plot_rel_path = get_relative_file_path(
                plot.file_path, relative_to=self.section_dir
            ).as_posix()
            plot_code = textwrap.dedent(
                f"""
                file_path = (section_dir / '{plot_rel_path}').resolve().as_posix()
                with open(file_path, 'r') as plot_file:
                    plot_json = json.load(plot_file)\n"""
            )

        # Add specific code for each visualization tool
        if plot.plot_type == r.PlotType.PLOTLY:
            plot_code += textwrap.dedent(
                """
                # Keep only 'data' and 'layout' sections
                plot_json = {key: plot_json[key] for key in plot_json
                                                 if key in ['data', 'layout']}

                # Remove 'frame' section in 'data'
                plot_json['data'] = [{k: v for k, v in entry.items() if k != 'frame'}
                                                for entry in plot_json.get('data', [])]
                st.plotly_chart(plot_json, use_container_width=True)\n"""
            )

        elif plot.plot_type == r.PlotType.ALTAIR:
            plot_code += textwrap.dedent(
                """
                altair_plot = alt.Chart.from_dict(plot_json)
                st.vega_lite_chart(json.loads(altair_plot.to_json()),
                                   use_container_width=True)\n"""
            )

        elif plot.plot_type == r.PlotType.INTERACTIVE_NETWORK:
            plot_code = textwrap.dedent(
                """\
                # Streamlit checkbox for controlling the layout
                control_layout = st.checkbox('Add panel to control layout', value=True)
                net_html_height = 1200 if control_layout else 630
                # Load HTML into HTML component for display on Streamlit
                st.components.v1.html(html_content, height=net_html_height)\n"""
            )
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
        read_function_mapping = table_utils.read_function_mapping

        try:
            # Check if the file extension matches any DataFrameFormat value
            file_extension = Path(dataframe.file_path).suffix.lower()
            if not any(
                file_extension == fmt.value_with_dot for fmt in r.DataFrameFormat
            ):
                self.report.logger.error(
                    "Unsupported file extension: %s. Supported extensions are: %s.",
                    file_extension,
                    ", ".join(fmt.value for fmt in r.DataFrameFormat),
                )
                # return []  # Skip execution if unsupported file extension
                # Should it not return here?
                # Can we even call the method with an unsupported file extension?

            # Build the file path (URL or local file)
            if is_url(dataframe.file_path):
                df_file_path = dataframe.file_path
            else:
                df_file_path = get_relative_file_path(dataframe.file_path)

            if file_extension in [
                r.DataFrameFormat.XLS.value_with_dot,
                r.DataFrameFormat.XLSX.value_with_dot,
            ]:
                dataframe_content.append("selected_sheet = 0")
                sheet_names = table_utils.get_sheet_names(df_file_path.as_posix())
                if len(sheet_names) > 1:
                    # If there are multiple sheets, ask the user to select one
                    fpath = get_relative_file_path(
                        dataframe.file_path, relative_to=self.section_dir
                    ).as_posix()
                    dataframe_content.append(
                        textwrap.dedent(
                            f"""\
                        file_path = (section_dir / '{fpath}').resolve().as_posix()
                        sheet_names = table_utils.get_sheet_names(file_path)
                        selected_sheet = st.selectbox("Select a sheet to display",
                                                      options=sheet_names,
                                        )
                        """
                        )
                    )

            # Load the DataFrame using the correct function
            df_file_path = get_relative_file_path(
                dataframe.file_path, relative_to=self.section_dir
            ).as_posix()
            read_function = read_function_mapping[file_extension].__name__
            if file_extension in [
                r.DataFrameFormat.XLS.value_with_dot,
                r.DataFrameFormat.XLSX.value_with_dot,
            ]:
                dataframe_content.append(
                    textwrap.dedent(
                        f"""\
                    file_path = (section_dir / '{df_file_path}').resolve()
                    df = pd.{read_function}(file_path, sheet_name=selected_sheet)
                    """
                    )
                )
            else:
                dataframe_content.append(
                    f"file_path = (section_dir / '{df_file_path}'"
                    ").resolve().as_posix()\n"
                    f"df = pd.{read_function}(file_path)\n"
                )
            # ! Alternative to select box: iterate over sheets in DataFrame
            # Displays a DataFrame using AgGrid with configurable options.
            dataframe_content.append(
                textwrap.dedent(
                    """
                    # Displays a DataFrame using AgGrid with configurable options.
                    grid_builder = GridOptionsBuilder.from_dataframe(df)
                    grid_builder.configure_default_column(editable=True,
                                                          groupable=True,
                                                          filter=True,
                    )
                    grid_builder.configure_side_bar(filters_panel=True,
                                                    columns_panel=True)
                    grid_builder.configure_selection(selection_mode="multiple")
                    grid_builder.configure_pagination(enabled=True,
                                                    paginationAutoPageSize=False,
                                                    paginationPageSize=20,
                    )
                    grid_options = grid_builder.build()

                    AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)

                    # Button to download the df
                    df_csv = df.to_csv(sep=',', header=True, index=False
                                      ).encode('utf-8')
                    st.download_button(
                        label="Download dataframe as CSV",
                        data=df_csv,
                        file_name=f"dataframe_{df_index}.csv",
                        mime='text/csv',
                        key=f"download_button_{df_index}")
                    df_index += 1"""
                )
            )
        except Exception as e:
            self.report.logger.error(
                "Error generating content for DataFrame: %s. Error: %s",
                dataframe.title,
                e,
                exc_info=True,
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
            "Successfully generated content for DataFrame: '%s'",
            dataframe.title,
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
                    textwrap.dedent(
                        f"""
                        response = requests.get('{markdown.file_path}')
                        response.raise_for_status()
                        markdown_content = response.text
                        """
                    )
                )
            else:  # If it's a local file
                md_rel_path = get_relative_file_path(
                    markdown.file_path, relative_to=self.section_dir
                ).as_posix()

                markdown_content.append(
                    textwrap.dedent(
                        f"""
                        file_path = (section_dir / '{md_rel_path}').resolve().as_posix()
                        with open(file_path, 'r') as markdown_file:
                            markdown_content = markdown_file.read()
                        """
                    )
                )
            # Code to display md content
            markdown_content.append(
                "st.markdown(markdown_content, unsafe_allow_html=True)\n"
            )
        except Exception as e:
            self.report.logger.error(
                "Error generating content for Markdown: %s. Error: %s",
                markdown.title,
                e,
                exc_info=True,
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
            "Successfully generated content for Markdown: '%s'",
            markdown.title,
        )
        return markdown_content

    def _generate_html_content(self, html) -> List[str]:
        """
        Generate content for an HTML component.

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
                textwrap.dedent(
                    html_content.append(
                        f"""
                        response = requests.get('{html.file_path}')
                        response.raise_for_status()
                        html_content = response.text
                        """
                    )
                )
            else:  # If it's a local file
                html_rel_path = get_relative_file_path(
                    html.file_path, relative_to=self.section_dir
                ).as_posix()
                html_content.append(
                    textwrap.dedent(
                        f"""\
                    file_path = (section_dir / '{html_rel_path}').resolve().as_posix()
                    with open(file_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    """
                    )
                )

            # Display HTML content using Streamlit
            html_content.append(
                "st.components.v1.html(html_content, height=600, scrolling=True)\n"
            )

        except Exception as e:
            self.report.logger.error(
                "Error generating content for HTML: %s. Error: %s",
                html.title,
                e,
                exc_info=True,
            )
            raise

        # Add caption if available
        if html.caption:
            html_content.append(
                self._format_text(text=html.caption, type="caption", text_align="left")
            )

        self.report.logger.info(
            "Successfully generated content for HTML: '%s'",
            html.title,
        )
        return html_content

    def _generate_apicall_content(self, apicall) -> List[str]:
        """
        Generate content for an API component. This method handles the API call and
        formats the response for display in the Streamlit app.

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
            apicall_response = apicall.make_api_request()
            apicall_content.append(f"""st.write({apicall_response})\n""")
        except Exception as e:
            self.report.logger.error(
                "Error generating content for APICall: %s. Error: %s",
                apicall.title,
                e,
                exc_info=True,
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
            "Successfully generated content for APICall '%s' using method '%s'",
            apicall.title,
            apicall.method,
        )
        return apicall_content

    def _generate_chatbot_content(self, chatbot) -> List[str]:
        """
        Generate content to render a ChatBot component, supporting standard and
        Ollama-style streaming APIs.

        This method builds and returns a list of strings, which are later executed to
        create the chatbot interface in a Streamlit app. It includes user input
        handling, API interaction logic, response parsing,
        and conditional rendering of text, source links, and HTML subgraphs.

        The function distinguishes between two chatbot modes:
        - **Ollama-style streaming API**: Identified by the presence of `chatbot.model`.
          Uses streaming JSON chunks from the server to simulate a real-time response.
        - **Standard API**: Assumes a simple POST request with a prompt and a full JSON
          response with text,
        and other fields like links, HTML graphs, etc.

        Parameters
        ----------
        chatbot : ChatBot
            The ChatBot component to generate content for, containing configuration such
            as title, model, API endpoint, headers, and caption.

        Returns
        -------
        list : List[str]
            The list of content lines for the ChatBot.
        """
        chatbot_content = []

        # Add chatbot title as header
        chatbot_content.append(
            self._format_text(
                text=chatbot.title, type="header", level=4, color="#2b8cbe"
            )
        )

        # --- Shared code blocks (as strings) ---
        init_messages_block = textwrap.indent(
            """
            # Init session state
            if 'messages' not in st.session_state:
                st.session_state['messages'] = []
            """,
            " " * 4,
        )

        render_messages_block = textwrap.indent(
            """
            # Display chat history
            for message in st.session_state['messages']:
                with st.chat_message(message['role']):
                    content = message['content']
                    if isinstance(content, dict):
                        st.markdown(content.get('text', ''), unsafe_allow_html=True)
                        if 'links' in content:
                            st.markdown("**Sources:**")
                            for link in content['links']:
                                st.markdown(f"- [{link}]({link})")
                        if 'subgraph_pyvis' in content:
                            st.components.v1.html(content['subgraph_pyvis'], height=600)
                    else:
                        st.write(content)
            """,
            " " * 4,
        )

        handle_prompt_block = textwrap.indent(
            """
            # Capture and append new user prompt
            if prompt := st.chat_input("Enter your prompt here:"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)
            """,
            " " * 4,
        )
        if chatbot.model:
            # --- Ollama-style streaming chatbot ---
            # all other codeblocks pasted in need to be on this indentation level
            code_block = textwrap.dedent(
                f"""
                {init_messages_block}
                # Function to send prompt to Ollama API
                def generate_query(messages):
                    response = requests.post(
                        "{chatbot.api_call.api_url}",
                        json={{"model": "{chatbot.model}",
                                "messages": messages,
                                "stream": True}},
                    )
                    response.raise_for_status()
                    return response

                # Parse streaming response from Ollama
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
                        return {{"role": "assistant", "content":
                                f"Error while processing API response: {{str(e)}}"}}

                # Simulated typing effect for responses
                def response_generator(msg_content):
                    for word in msg_content.split():
                        yield word + " "
                        time.sleep(0.1)
                    yield "\\n"
                {render_messages_block}
                {handle_prompt_block}
                    # Retrieve question and generate answer
                    combined = "\\n".join(msg["content"]
                                for msg in st.session_state.messages
                                if msg["role"] == "user")
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
            chatbot_content.append(code_block)

        else:
            # --- Standard (non-streaming) API chatbot ---
            code_block = textwrap.dedent(
                f"""
                {init_messages_block}

                # Function to send prompt to standard API
                def generate_query(prompt):
                    try:
                        response = requests.post(
                            "{chatbot.api_call.api_url}",
                            json={{"prompt": prompt}},
                            headers={chatbot.api_call.headers}
                        )
                        response.raise_for_status()
                        return response.json()
                    except requests.exceptions.RequestException as e:
                        st.error(f"API request failed: {{str(e)}}")
                        if hasattr(e, 'response') and e.response:
                            try:
                                error_details = e.response.json()
                                st.error(f"Error details: {{error_details}}")
                            except ValueError:
                                st.error(f"Response text: {{e.response.text}}")
                        return None

                {render_messages_block}

                {handle_prompt_block}

                    with st.spinner('Generating answer...'):
                        response = generate_query(prompt)

                        if response:
                            # Append and display assistant response
                            st.session_state.messages.append({{
                                "role": "assistant",
                                "content": response
                            }})
                            with st.chat_message("assistant"):
                                st.markdown(response.get('text', ''),
                                            unsafe_allow_html=True)
                                if 'links' in response:
                                    st.markdown("**Sources:**")
                                    for link in response['links']:
                                        st.markdown(f"- [{{link}}]({{link}})")
                                if 'subgraph_pyvis' in response:
                                    st.components.v1.html(
                                        response['subgraph_pyvis'],
                                        height=600
                                    )
                        else:
                            st.error("Failed to get response from API")
                    """
            )
            chatbot_content.append(code_block)

        if chatbot.caption:
            chatbot_content.append(
                self._format_text(
                    text=chatbot.caption, type="caption", text_align="left"
                )
            )

        return chatbot_content

    def _generate_component_imports(self, component: r.Component) -> List[str]:
        """
        Generate necessary imports for a component of the report.

        Parameters
        ----------
        component : r.Component
            The component for which to generate the required imports.
            The component can be of type:
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
                "from vuegen import table_utils",
            ],
            "markdown": ["import requests"],
            "chatbot": ["import time", "import json", "import requests"],
        }

        component_type = component.component_type
        component_imports = [
            "import streamlit as st",
            "from pathlib import Path",
            "section_dir = Path(__file__).resolve().parent.parent",
        ]

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
