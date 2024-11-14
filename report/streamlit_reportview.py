import report as r
import os
import sys
from typing import List, Optional
from streamlit.web import cli as stcli

class StreamlitReportView(r.WebAppReportView):
    """
    A Streamlit-based implementation of a report view interface.

    Methods
    -------
    generate_report(output_dir)
        Generates the Streamlit report and saves the report files to the specified folder.
    run_report(output_dir)
        Runs the generated Streamlit report.
    _fornat_text(text, type, level, color)
        Generates a Streamlit markdown text string with the specified type (header, paragraph), level and color.
    _generate_home_section(output_dir, report_manag_content)
        Generates the homepage for the report and updates the report manager content.
    _generate_sections(output_dir)
        Generates Python files for each section in the report, including subsections and its components (plots, dataframes, markdown).
    _generate_subsection(subsection, imports_written, content)
        Creates components (plots, dataframes, markdown, etc) for a given subsection. 
    """

    def __init__(self, identifier: int, name: str, report: r.Report, report_type: r.ReportType, columns: Optional[List[str]]):
        super().__init__(identifier, name=name, report=report, report_type = r.ReportType.STREAMLIT, columns=columns)

    def generate_report(self, output_dir: str = 'streamlit_report/sections') -> None:
        """
        Generates the Streamlit report and creates Python files for each section and its subsections and plots.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the generated report files will be saved (default is 'streamlit_report/sections').
        """
        # Create the output folder if it does not exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Define the Streamlit imports and report manager content
        report_manag_content = []
        report_manag_content.append(f"""import streamlit as st\n
st.set_page_config(layout="wide", page_title="{self.report.name}", page_icon="{self.report.logo}")
st.logo("{self.report.logo}")""")
        report_manag_content.append(self._format_text(text=self.report.title, type = 'header', level=1, color='#023858'))

        # Initialize a dictionary to store the navigation structure
        report_manag_content.append("\nsections_pages = {}")

        # Generate the home page and update the report manager content
        self._generate_home_section(output_dir=output_dir, report_manag_content=report_manag_content)

        for section in self.report.sections:
            # Create a folder for each section
            subsection_page_vars = []
            section_name_var = section.name.replace(" ", "_")
            if not os.path.exists(os.path.join(output_dir, section_name_var)):
                os.mkdir(os.path.join(output_dir, section_name_var))
            
            for subsection in section.subsections:
                subsection_name_var = subsection.name.replace(" ", "_")
                subsection_file_path = os.path.join(section_name_var, section_name_var + "_" + subsection_name_var + ".py")

                # Create a Page object for each subsection and add it to the home page content
                report_manag_content.append(f"{subsection_name_var} = st.Page('{subsection_file_path}', title='{subsection.name}')")
                subsection_page_vars.append(subsection_name_var)
            
            # Add all subsection Page objects to the corresponding section
            report_manag_content.append(f"sections_pages['{section.name}'] = [{', '.join(subsection_page_vars)}]\n")

        # Add navigation object to the home page content
        report_manag_content.append(f"""report_nav = st.navigation(sections_pages)
report_nav.run()""")
        
        # Write the navigation and general content to a Python file
        with open(os.path.join(output_dir, "report_manager.py"), 'w') as nav_manager:
            nav_manager.write("\n".join(report_manag_content))

        # Create Python files for each section and its subsections and plots
        self._generate_sections(output_dir=output_dir)

    def run_report(self, output_dir: str = 'sections') -> None:
        """
        Runs the generated Streamlit report.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the report was generated (default is 'sections').
        """
        sys.argv = ["streamlit", "run", os.path.join(output_dir, "report_manager.py")]
        sys.exit(stcli.main())

    def _format_text(self, text: str, type: str, level: int = 1, color: str = '#000000') -> str:
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

        Returns
        -------
        str
            A formatted markdown string for the specified text.
        """
        if type == 'header':
            tag = f"h{level}"
        elif type == 'paragraph':
            tag = 'p'

        return f"""st.markdown('''<{tag} style='text-align: center; color: {color};'>{text}</{tag}>''', unsafe_allow_html=True)"""

    def _generate_home_section(self, output_dir: str, report_manag_content: list) -> None:
        """
        Generates the homepage for the report and updates the report manager content.

        Parameters
        ----------
        output_dir : str
            The folder where the homepage files will be saved.
        report_manag_content : list
            A list to store the content that will be written to the report manager file.
        """
        # Create folder for the home page
        if not os.path.exists(os.path.join(output_dir, "Home")):
            os.mkdir(os.path.join(output_dir, "Home"))

        # Create the home page content
        home_content = []
        home_content.append(f"import streamlit as st")
        home_desc = self._format_text(text=self.report.description, type='paragraph')
        home_content.append(home_desc)
        if self.report.graphical_abstract:
            home_content.append(f"\nst.image('{self.report.graphical_abstract}', use_column_width=True)")

        # Write the home page content to a Python file
        with open(os.path.join(output_dir, "Home", "Homepage.py"), 'w') as home_page:
            home_page.write("\n".join(home_content))

        # Add the home page to the report manager content
        report_manag_content.append(f"homepage = st.Page('Home/Homepage.py', title='Homepage')")
        report_manag_content.append(f"sections_pages['Home'] = [homepage]\n")

    def _generate_sections(self, output_dir: str) -> None:
        """
        Generates Python files for each section in the report, including subsections and its components (plots, dataframes, markdown).
        
        Parameters
        ----------
        output_dir : str
            The folder where section files will be saved.
        """
        for section in self.report.sections:
            section_name_var = section.name.replace(" ", "_")

            if section.subsections:
                # Iterate through subsections and integrate them into the section file
                for subsection in section.subsections:
                    # Create subsection file
                    subsection_file_path = os.path.join(output_dir, section_name_var, section_name_var + "_" + subsection.name.replace(" ", "_") + ".py")
                    
                    # Generate content and imports for the subsection
                    subsection_content, subsection_imports = self._generate_subsection(subsection)

                    # Flatten the subsection_imports into a single list
                    flattened_subsection_imports = [imp for sublist in subsection_imports for imp in sublist]
                    
                    # Remove duplicated imports
                    unique_imports = list(set(flattened_subsection_imports))

                    # Write everything to the subsection file
                    with open(subsection_file_path, 'w') as subsection_file:
                        # Write imports at the top of the file
                        subsection_file.write("\n".join(unique_imports) + "\n\n")

                        # Write the subsection content (descriptions, plots)
                        subsection_file.write("\n".join(subsection_content))

    def _generate_subsection(self, subsection) -> List[str]:
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
        tuple : (List[str], List[str])
            - list of subsection content lines (List[str])
            - list of imports for the subsection (List[str])
        """
        subsection_content = []
        subsection_imports = []
        
        # Add subsection header and description
        subsection_content.append(self._format_text(text=subsection.name, type='header', level=3, color='#023558'))
        subsection_content.append(self._format_text(text=subsection.description, type='paragraph'))

        for component in subsection.components:
            # Write imports if not already done
            component_imports = self._generate_component_imports(component)
            subsection_imports.append(component_imports)

            # Handle different types of components
            if component.component_type == r.ComponentType.PLOT:
                subsection_content.extend(self._generate_plot_content(component))
            elif component.component_type == r.ComponentType.DATAFRAME:
                subsection_content.extend(self._generate_dataframe_content(component))
            elif component.component_type == r.ComponentType.MARKDOWN:
                subsection_content.extend(self._generate_markdown_content(component))
        return subsection_content, subsection_imports
    
    def _generate_plot_content(self, plot) -> List[str]:
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
        """
        plot_content = []
        plot_content.append(self._format_text(text=plot.title, type='header', level=4, color='#2b8cbe'))

        if plot.plot_type == r.PlotType.INTERACTIVE:
            # Handle interactive plot
            if plot.visualization_tool == r.VisualizationTool.PLOTLY:
                plot_content.append(self._generate_plot_code(plot))
            elif plot.visualization_tool == r.VisualizationTool.ALTAIR:
                plot_content.append(self._generate_plot_code(plot))
            elif plot.visualization_tool == r.VisualizationTool.PYVIS:
                # For PyVis, handle the network visualization
                G = plot.read_network()
                html_plot_file = f"streamlit_report/{plot.name.replace(' ', '_')}.html"
                net = plot.create_and_save_pyvis_network(G, html_plot_file)
                num_nodes = len(net.nodes)
                num_edges = len(net.edges)
                plot_content.append(f"""with open('{html_plot_file}', 'r') as f:
    html_data = f.read()
st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of nodes:</b> {num_nodes} </p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of relationships:</b> {num_edges} </p>", unsafe_allow_html=True)""")
                plot_content.append(self._generate_plot_code(plot))
        elif plot.plot_type == r.PlotType.STATIC:
            # Handle static plot
            plot_content.append(f"\nst.image('{plot.file_path}', caption='{plot.caption}', use_column_width=True)\n")

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
        # Start with the common data loading code
        plot_code = f"""with open('{plot.file_path}', 'r') as plot_file:
    plot_json = json.load(plot_file)\n"""
        # Add specific code for each visualization tool
        if plot.visualization_tool == r.VisualizationTool.PLOTLY:
            plot_code += "st.plotly_chart(plot_json, use_container_width=True)\n"

        elif plot.visualization_tool == r.VisualizationTool.ALTAIR:
            plot_code += """altair_plot = alt.Chart.from_dict(plot_json)
st.vega_lite_chart(json.loads(altair_plot.to_json()), use_container_width=True)\n"""
        
        elif plot.visualization_tool == r.VisualizationTool.PYVIS:
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
        dataframe_content.append(self._format_text(text=dataframe.title, type='header', level=4, color='#2b8cbe'))
        
        if dataframe.file_format == r.DataFrameFormat.CSV:
            dataframe_content.append(f"df = pd.read_csv('{dataframe.file_path}')")
        elif dataframe.file_format == r.DataFrameFormat.PARQUET:
            dataframe_content.append(f"df = pd.read_parquet('{dataframe.file_path}')")
        elif dataframe.file_format == r.DataFrameFormat.TXT:
            dataframe_content.append(f"df = pd.read_csv('{dataframe.file_path}', sep='\\t')")
        elif dataframe.file_format == r.DataFrameFormat.EXCEL:
            dataframe_content.append(f"df = pd.read_excel('{dataframe.file_path}')")
        else:
            raise ValueError(f"Unsupported DataFrame file format: {dataframe.file_format}")
        
        dataframe_content.append("st.dataframe(df, use_container_width=True)")
        
        return dataframe_content
    
    def _generate_markdown_content(self, markdown) -> List[str]:
        """
        Generate content for a Markdown component.

        Parameters
        ----------
        markdown : Markdown
            The markdown component to generate content for.

        Returns
        -------
        list : List[str]
            The list of content lines for the markdown.
        """
        markdown_content = []
        markdown_content.append(self._format_text(text=markdown.title, type='header', level=4, color='#2b8cbe'))
        markdown_content.append(f"""with open('{markdown.file_path}', 'r') as markdown_file:
    markdown_content = markdown_file.read()
st.markdown(markdown_content, unsafe_allow_html=True)\n""")
        
        return markdown_content
    
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
            'plot': {
                r.VisualizationTool.ALTAIR: ['import json', 'import altair as alt'],
                r.VisualizationTool.PLOTLY: ['import json']
            },
            'dataframe': ['import pandas as pd']
        }

        component_type = component.component_type
        component_imports = ['import streamlit as st']

        # Add relevant imports based on component type and visualization tool
        if component_type == r.ComponentType.PLOT:
            visualization_tool = getattr(component, 'visualization_tool', None)
            if visualization_tool in components_imports['plot']:
                component_imports.extend(components_imports['plot'][visualization_tool])

        elif component_type == r.ComponentType.DATAFRAME:
            component_imports.extend(components_imports['dataframe'])

        # Return the list of import statements
        return component_imports