import os
import sys
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import altair as alt
from streamlit.web import cli as stcli
import networkx as nx
from pyvis.network import Network
import pandas as pd

class ComponentType(Enum):
    PLOT = 'plot'
    DATAFRAME = 'dataframe'
    MARKDOWN = 'markdown'

class PlotType(Enum):
    INTERACTIVE = 'interactive'
    STATIC = 'static'

class VisualizationTool(Enum):
    PLOTLY = 'plotly'
    ALTAIR = 'altair'
    PYVIS = 'pyvis'

class CSVNetworkFormat(Enum):
    EDGELIST = 'edgelist'
    ADJLIST = 'adjlist'

class DataFrameFormat(Enum):
    CSV = 'csv'
    TXT = 'txt'
    PARQUET = 'parquet'

@dataclass
class Component(ABC):
    """
    Abstract base class for different components in a report subsection.

    Attributes
    ----------
    identifier : int
        A unique identifier for the component.
    name : str
        The name of the component.
    file_path : str
        The file path for the component (e.g., plot JSON file, image file, csv file, etc.).
    component_type : ComponentType
        The type of the component (PLOT, DATAFRAME, MARKDOWN).
    title : Optional[str]
        The title of the component (default is None). 
    caption : Optional[str]
        A caption for the component (default is None).
    """
    identifier: int
    name: str
    file_path: str 
    component_type: ComponentType
    title: Optional[str] = None
    caption: Optional[str] = None

    @abstractmethod
    def load_from_file(self):
        """
        Read and parse a component from a file.
        """
        pass
    
    @abstractmethod
    def generate_imports(self) -> str:
        """
        Generate the import statements required for the component.

        Returns
        -------
        str
            A string representing the import statements needed for the component.
        """
        pass

class Plot(Component):
    """
    A plot within a subsection of a report.

    Attributes
    ----------
    plot_type : PlotType
        The type of the plot (INTERACTIVE or STATIC).
    visualization_tool : VisualizationTool, optional
        The tool for rendering interactive plots (PLOTLY, ALTAIR, or PYVIS) (default is None).
        It is not required for STATIC plots (default is None).
    csv_network_format : CSVNetworkFormat, optional
        The format of the CSV file for network plots (EDGELIST or ADJLIST) (default is None).
    """
    def __init__(self, identifier: int, name: str, file_path: str, plot_type: PlotType, 
                visualization_tool: Optional[VisualizationTool]=None, title: str=None, 
                caption: str=None, csv_network_format: Optional[CSVNetworkFormat]=None):
        """
        Initializes a Plot object.
        """
        # Call the constructor of the parent class (Component) to set common attributes
        super().__init__(identifier, name, file_path, component_type = ComponentType.PLOT, title=title, caption=caption)

        # Set specific attributes for the Plot class
        self.plot_type = plot_type
        self.visualization_tool = visualization_tool
        self.csv_network_format = csv_network_format

    def load_from_file(self) -> str:
        """
        Reads and parses the JSON representation of the plot. 

        Returns
        -------
        str
            A string representation of the parsed plot code.
        """
        if self.plot_type == PlotType.INTERACTIVE:
            with open(self.file_path, 'r') as plot_file:
                plot_json = plot_file.read()
            plot_dict = json.loads(plot_json) if plot_json else {}
            if self.visualization_tool == VisualizationTool.ALTAIR:
                altair_plot = alt.Chart.from_dict(plot_dict)
                return altair_plot.to_dict()
            return str(plot_dict)
        return ""

    def generate_imports(self) -> str:
        """
        Generate the import statements required for the visualization tool.

        Returns
        -------
        str
            A string representing the import statements needed for the plot.
        """
        imports = []
        if self.visualization_tool == VisualizationTool.ALTAIR:
            imports.append('import altair as alt')
            imports.append('import json')
        return "\n".join(imports)
    
    def read_network(self) -> nx.Graph:
        """
        Reads the network file and returns a NetworkX graph object.
        
        Returns
        -------
        G : networkx.Graph
            A NetworkX graph object created from the specified network file.
        """
        # Mapping of file extensions to NetworkX loading functions
        file_extension_map = {
            '.gml': nx.read_gml,
            '.graphml': nx.read_graphml,
            '.gexf': nx.read_gexf,
            '.csv': nx.read_edgelist,
            '.txt': nx.read_edgelist,
            # Add more mappings as needed
        }

        # Determine the file extension
        file_extension = os.path.splitext(self.file_path)[-1].lower()

        if file_extension in file_extension_map:
            # Call the corresponding loading function
            if file_extension in ['.csv', '.txt'] and self.csv_network_format:
                if self.csv_network_format == CSVNetworkFormat.EDGELIST:
                    G = nx.read_edgelist(self.file_path, delimiter=',')
                elif self.csv_network_format == CSVNetworkFormat.ADJLIST:
                    G = nx.read_adjlist(self.file_path)
                else:
                    raise ValueError(f"Unsupported format for CSV/TXT file: {self.csv_network_format}")
            else:
                G = file_extension_map[file_extension](self.file_path)

                    # Clean up edge attributes to avoid conflicts
            for u, v, data in G.edges(data=True):
                data.pop('source', None)
                data.pop('target', None)

            # Assign node labels as their IDs
            for node in G.nodes(data=True):
                G.nodes[node[0]]['label'] = G.nodes[node[0]].get('name', node[0])  # Set node label to its name or ID

            # Obtain and set degree values for nodes
            degrees = {node: G.degree(node) for node in G.nodes()}

            # Assign sizes based on degrees
            min_size = 5  # Define minimum node size
            max_size = 30  # Define maximum node size
            min_degree = min(degrees.values())
            max_degree = max(degrees.values())

            for node in G.nodes():
                degree = degrees[node]
                if degree == min_degree:
                    size = min_size
                elif degree == max_degree:
                    size = max_size
                else:
                    size = min_size + (max_size - min_size) * ((degree - min_degree) / (max_degree - min_degree))
                
                G.nodes[node]['size'] = size  # Assign size based on degree

            return G
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")

    def create_and_save_pyvis_network(self, G: nx.Graph, output_file: str) -> Network:
        """
        Creates a PyVis network from a NetworkX graph object and saves it as an HTML file.
        
        Parameters
        ----------
        G : networkx.Graph
            A NetworkX graph object.
        output_file : str
            The file path where the HTML should be saved.

        Returns
        -------
        net : pyvis.network.Network
            A PyVis network object.
        """
        # Create a PyVis network object
        net = Network(height='600px', width='100%', bgcolor='white', font_color='black')
        net.from_nx(G)

        # Customize the network visualization of nodes
        for node in net.nodes:
            node_id = node['id']
            node_data = G.nodes[node_id]
            node['font'] = {'size': 12}
            node_data.get('name', node_id)
            node['borderWidth'] = 2
            node['borderWidthSelected'] = 2.5

        # Apply the force_atlas_2based layout and show panel to control layout
        net.force_atlas_2based(gravity=-30, central_gravity=0.005, spring_length=100, spring_strength=0.1, damping=0.4)
        net.show_buttons(filter_=['physics'])
            
        # Save the network as an HTML file
        net.save_graph(output_file)

        return net
    
class DataFrame(Component):
    """
    A DataFrame within a subsection of a report.

    Attributes
    ----------
    file_format : DataFrameFormat
        The format of the file from which the DataFrame is loaded (e.g., CSV, TXT, PARQUET).
    delimiter : Optional[str]
        The delimiter to use if the file is a delimited text format (e.g., ';', '\t', etc).
    """
    def __init__(self, identifier: int, name: str, file_path: str, file_format: DataFrameFormat, 
                 delimiter: Optional[str]=None, title: str=None, caption: str=None):
        """
        Initializes a DataFrame object.
        """
        super().__init__(identifier, name, file_path, component_type=ComponentType.DATAFRAME, title=title, caption=caption)
        self.file_format = file_format
        self.delimiter = delimiter

    def load_from_file(self) -> pd.DataFrame:
        """
        Load and parse the DataFrame from a file based on its format.
        
        Returns
        -------
        pd.DataFrame
            The loaded DataFrame object.
        """
        if self.file_format == DataFrameFormat.CSV:
            return pd.read_csv(self.file_path, delimiter=self.delimiter) if self.delimiter else pd.read_csv(self.file_path)
        elif self.file_format == DataFrameFormat.TXT:
            return pd.read_csv(self.file_path, delimiter=self.delimiter) if self.delimiter else pd.read_csv(self.file_path, sep='\t')
        elif self.file_format == DataFrameFormat.PARQUET:
            return pd.read_parquet(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {self.file_format}")

    def generate_imports(self) -> str:
        """
        Generate the import statements required for handling DataFrames.
        
        Returns
        -------
        str
            A string representing the import statements needed for the DataFrame.
        """
        return "import pandas as pd"


@dataclass
class Markdown(Component):
    component_type = ComponentType.MARKDOWN
    """
    A Markdown text component within a subsection of a report.
    """
    
    def load_from_file(self) -> str:
        """
        Load and return the markdown content from the file.
        
        Returns
        -------
        str
            A string containing the markdown content.
        """
        with open(self.file_path, 'r') as markdown_file:
            return markdown_file.read()

    def generate_imports(self) -> str:
        """
        Generate the import statements required for Markdown rendering.
        
        Returns
        -------
        str
            A string representing the import statements needed for rendering Markdown.
        """
        return "import markdown"
    
@dataclass
class Subsection:
    """
    A subsection within a section, containing multiple components (plots, DataFrames, Markdown text, etc).

    Attributes
    ----------
    identifier : int
        A unique identifier for the subsection.
    name : str
        The name of the subsection.
    title : str, optional
        The title of the subsection (default is None).
    description : str, optional
        A description of the subsection (default is None).
    components : List[Component]
        A list of components within this subsection.
    """
    identifier: int
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    components: List['Component'] = field(default_factory=list)

    def add_component(self, component: Component) -> None:
        """
        Adds a component (Plot, DataFrame, Markdown) to the subsection.
        
        Parameters
        ----------
        component : Component
            The component to add to the subsection.
        """
        self.components.append(component)

    def get_component_by_id(self, identifier: int) -> Optional[Component]:
        """
        Retrieves a component by its unique identifier.

        Parameters
        ----------
        identifier : int
            The unique identifier of the component.

        Returns
        -------
        Optional[Component]
            The component with the given identifier, or None if not found.
        """
        for component in self.components:
            if component.identifier == identifier:
                return component
        return None
    
    def remove_component_by_id(self, identifier: int) -> bool:
        """
        Removes a component by its unique identifier.
        
        Parameters
        ----------
        identifier : int
            The unique identifier of the component to remove.
            
        Returns
        -------
        bool
            True if the component was successfully removed, False otherwise.
        """
        for i, component in enumerate(self.components):
            if component.identifier == identifier:
                del self.components[i]
                return True
        return False

@dataclass
class Section:
    """
    A section within a report, containing multiple subsections.

    Attributes
    ----------
    identifier : int
        A unique identifier for the section.
    name : str
        The name of the section.
    title : str, optional
        The title of the section (default is None).
    description : str, optional
        A description of the section (default is None).
    subsections : List[Subsection]
        A list of subsections within this section.
    """
    identifier: int
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    subsections: List['Subsection'] = field(default_factory=list)

@dataclass
class Report:
    """
    A report consisting of multiple sections and subsections.

    Attributes
    ----------
    identifier : int
        A unique identifier for the report.
    name : str
        The name of the report.
    title : str, optional
        The title of the report (default is None).
    description : str, optional
        A description of the report (default is None).
    graphical_abstract : str, optional
        The file path to the graphical abstract image (default is None).
    logo : str, optional
        The file path to the logo image (default is None).
    sections : List[Section]
        A list of sections that belong to the report.
    """
    identifier: int
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    graphical_abstract: Optional[str] = None
    logo: Optional[str] = None
    sections: List['Section'] = field(default_factory=list)

@dataclass
class ReportView(ABC):
    """
    An abstract base class for report view implementations.

    Attributes
    ----------
    identifier : int
        A unique identifier for the report view ABC.
    name : str
        The name of the view.
    report : Report
        The report that this ABC is associated with.
    columns : List[str], optional
        Column names used in the report view ABC (default is None).
    interface_type : str, optional
        The type of the ABC (e.g., 'WebAppReportView', 'DocumentReportView', PresentReportView, 'WikiReportView', 'NotebookReportView') (default is None).
    """
    identifier: int
    name: str
    report: Report
    columns: Optional[List[str]] = None
    interface_type: Optional[str] = None

    @abstractmethod
    def generate_report(self, output_dir: str = 'sections') -> None:
        """
        Generates the report and creates output files.
        
        Parameters
        ----------
        output_dir : str, optional
            The folder where the generated report files will be saved (default is 'sections').
        """
        pass

    @abstractmethod
    def _format_text(self, text: str, type: str, level: int, color: str) -> str:
        """
        Format text for the report view.
        
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
            The formatted text string.
        """
        pass

class WebAppReportView(ReportView):
    """
    An abstract class for web application report views.

    Attributes
    ----------
    report_framework : str
        The web app framework used to generate the report (e.g., 'Streamlit').

    Methods
    -------
    run_report(output_dir)
        Runs the generated web app report.
    _generate_sections(output_dir)
        Creates sections and subsections for the report.
    _generate_subsection(subsection, imports_written, content)
        Creates components (plots, dataframes, markdown, etc) for a given subsection. 
    """
    def __init__(self, identifier: int, name: str, columns: Optional[List[str]], report_framework: str, report: Report):
        super().__init__(identifier, name=name, columns=columns, interface_type='WebAppReportView', report=report)
        self.report_framework = report_framework

    @abstractmethod
    def run_report(self, output_dir: str = 'sections') -> None:
        """
        Runs the generated report.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the report was generated (default is 'sections').
        """
        pass

    @abstractmethod
    def _generate_sections(self, output_dir: str) -> None:
        """
        Creates sections and subsections for the report.
        
        Parameters
        ----------
        output_dir : str
            The folder where section files will be saved.

        Notes
        -----
        This method is intended to be used internally by the `generate_report` method.
        """
        pass

    @abstractmethod
    def _generate_subsection(self, subsection: Subsection, imports_written: set, content: list) -> List[str]:
        """
        Creates components (plots, dataframes, markdown, etc) for a given subsection. 
        
        Parameters
        ----------
        subsection : Subsection
            The subsection containing the plots.
        imports_written : set
            A set of already written imports.
        content : list
            A list to which the generated content will be appended.

        Returns
        -------
        list
            A list of imports for the subsection.
        """
        pass

class StreamlitReportView(WebAppReportView):
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

    def __init__(self, identifier: int, name: str, columns: Optional[List[str]], report: Report):
        super().__init__(identifier, name=name, columns=columns, report_framework='Streamlit', report=report)

    def generate_report(self, output_dir: str = 'sections') -> None:
        """
        Generates the Streamlit report and creates Python files for each section and its subsections and plots.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the generated report files will be saved (default is 'sections').
        """
        # Create the output folder if it does not exist
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # Define the Streamlit imports and report manager content
        streamlit_imports = f'''import streamlit as st
st.set_page_config(layout="wide", page_title="{self.report.name}", page_icon="{self.report.logo}")
st.logo("{self.report.logo}")
'''
        general_head = self._format_text(text=self.report.title, type = 'header', level=1, color='#023858')
        report_manag_content = [streamlit_imports, general_head]

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
        report_manag_content.append(f'''report_nav = st.navigation(sections_pages)
report_nav.run()''')
        
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
        with open(os.path.join(output_dir, "Home", "homepage.py"), 'w') as home_page:
            home_page.write("\n".join(home_content))

        # Add the home page to the report manager content
        report_manag_content.append(f"homepage = st.Page('home/homepage.py', title='Homepage')")
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
                    # Track imports to avoid duplication
                    imports_written_subsection = set()

                    # Collect imports and section content
                    imports = ['import streamlit as st']

                    # Create subsection file
                    subsection_file_path = os.path.join(output_dir, section_name_var, section_name_var + "_" + subsection.name.replace(" ", "_") + ".py")
                    
                    # Add subsection header and description
                    subsection_header = self._format_text(text=subsection.name, type='header', level=3, color='#023558')
                    subsection_desc = self._format_text(text=subsection.description, type='paragraph')
                    
                    # Collect subsection content
                    subsection_content = [subsection_header, subsection_desc]
                    
                    # Generate plots for the subsection
                    imports_subsection = self._generate_subsection(subsection, imports_written_subsection, subsection_content)

                    imports.extend(imports_subsection) 

                    # Write everything to the subsection file
                    with open(subsection_file_path, 'w') as subsection_file:
                        # Write imports at the top of the file
                        subsection_file.write("\n".join(imports) + "\n\n")

                        # Write the subsection content (descriptions, plots)
                        subsection_file.write("\n".join(subsection_content))

    def _generate_subsection(self, subsection, imports_written, content):
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
        imports = []
        
        for component in subsection.components:
            # Write imports if not already done
            imports_component = component.generate_imports()
            if imports_component and component.component_type not in imports_written:
                imports.append(imports_component)
                imports_written.add(component.component_type)

            # Handle different types of components
            if component.component_type == ComponentType.PLOT:
                # Cast component to Plot
                plot = component 
                if plot.plot_type == PlotType.INTERACTIVE:
                    if plot.visualization_tool == VisualizationTool.PLOTLY:
                        content.append(self._format_text(text=plot.title, type='header', level=4, color='#2b8cbe'))
                        content.append(f"\nst.plotly_chart({plot.load_from_file()}, use_container_width=True)\n")
                    elif plot.visualization_tool == VisualizationTool.ALTAIR:
                        content.append(self._format_text(text=plot.title, type='header', level=4, color='#2b8cbe'))
                        content.append(f"\nst.vega_lite_chart(json.loads(alt.Chart.from_dict({plot.load_from_file()}).to_json()), use_container_width=True)\n")
                    elif plot.visualization_tool == VisualizationTool.PYVIS:
                        G = plot.read_network()
                        # Define the output file name
                        output_file = f"example_data/{plot.name.replace(' ', '_')}.html"
                         # Get the Network object
                        net = plot.create_and_save_pyvis_network(G, output_file)
                        num_nodes = len(net.nodes)
                        num_edges = len(net.edges)
                        content.append(self._format_text(text=plot.title, type='header', level=4, color='#2b8cbe'))

                        content.append(f"""
with open('{output_file}', 'r') as f:
    html_data = f.read()

st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of nodes:</b> {num_nodes} </p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of relationships:</b> {num_edges} </p>", unsafe_allow_html=True)

# Streamlit checkbox for controlling the layout
control_layout = st.checkbox('Add panel to control layout', value=True)
net_html_height = 1200 if control_layout else 630

# Load HTML into HTML component for display on Streamlit
st.components.v1.html(html_data, height=net_html_height)""")

                elif plot.plot_type == PlotType.STATIC:
                    content.append(self._format_text(text=plot.title, type='header', level=4, color='#2b8cbe'))
                    content.append(f"\nst.image('{plot.file_path}', caption='{plot.caption}', use_column_width=True)\n")

            elif component.component_type == ComponentType.DATAFRAME:
                # Cast component to DataFrame
                dataframe = component 
                if dataframe.file_format == DataFrameFormat.CSV:
                    content.append(self._format_text(text=dataframe.title, type='header', level=4, color='#2b8cbe'))
                    content.append(f"""df = pd.read_csv('{dataframe.file_path}')
st.dataframe(df, use_container_width=True)\n""")
                elif dataframe.file_format == DataFrameFormat.PARQUET:
                    content.append(self._format_text(text=dataframe.title, type='header', level=4, color='#2b8cbe'))
                    content.append(f"""df = pd.read_parquet('{dataframe.file_path}')
st.dataframe(df, use_container_width=True)\n""")
                elif dataframe.file_format == DataFrameFormat.TXT:
                    content.append(self._format_text(text=dataframe.title, type='header', level=4, color='#2b8cbe'))
                    content.append(f"""df = pd.read_csv('{dataframe.file_path}', sep='\\t')
st.dataframe(df, use_container_width=True)\n""")

            elif component.component_type == ComponentType.MARKDOWN:
                # Cast component to Markdown
                markdown = component 
                content.append(self._format_text(text=markdown.title, type='header', level=4, color='#2b8cbe'))
                content.append(f"st.markdown('''{markdown.load_from_file()}''', unsafe_allow_html=True)\n")
        return imports