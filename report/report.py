import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import List, Optional, NamedTuple
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from pyvis.network import Network

class ReportType(StrEnum):
    STREAMLIT = auto()
    DOCUMENT = auto()
    PRESENTATION = auto()
    NOTEBOOK = auto()

class ComponentType(StrEnum):
    PLOT = auto()
    DATAFRAME = auto()
    MARKDOWN = auto()

class PlotType(StrEnum):
    INTERACTIVE = auto()
    STATIC = auto()

class IntVisualizationTool(StrEnum):
    PLOTLY = auto()
    ALTAIR = auto()
    PYVIS = auto()

class CSVNetworkFormat(StrEnum):
    EDGELIST = auto()
    ADJLIST = auto()

class DataFrameFormat(StrEnum):
    CSV = auto()
    TXT = auto()
    PARQUET = auto()
    EXCEL = auto()

@dataclass
class Component():
    """
    Base class for different components in a report subsection. The attributes are inmutable 
    because they are loaded from a config file and should not be changed after initialization.

    Attributes
    ----------
    id : int
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
    id: int
    name: str
    file_path: str 
    component_type: ComponentType
    title: Optional[str] = None
    caption: Optional[str] = None

class Plot(Component):
    """
    A plot within a subsection of a report.

    Attributes
    ----------
    plot_type : PlotType
        The type of the plot (INTERACTIVE or STATIC).
    int_visualization_tool : IntVisualizationTool, optional
        The tool for rendering interactive plots (PLOTLY, ALTAIR, or PYVIS) (default is None).
        It is not required for STATIC plots (default is None).
    csv_network_format : CSVNetworkFormat, optional
        The format of the CSV file for network plots (EDGELIST or ADJLIST) (default is None).
    """
    def __init__(self, id: int, name: str, file_path: str, plot_type: PlotType, 
                int_visualization_tool: Optional[IntVisualizationTool]=None, title: str=None, 
                caption: str=None, csv_network_format: Optional[CSVNetworkFormat]=None):
        """
        Initializes a Plot object.
        """
        # Call the constructor of the parent class (Component) to set common attributes
        super().__init__(id, name, file_path, component_type = ComponentType.PLOT, title=title, caption=caption)

        # Set specific attributes for the Plot class
        self.plot_type = plot_type
        self.int_visualization_tool = int_visualization_tool
        self.csv_network_format = csv_network_format
    
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
        }

        # Check if the file exists
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"The file at {self.file_path} was not found or cannot be accessed.")

        # Determine the file extension and check if it is supported
        file_extension = os.path.splitext(self.file_path)[-1].lower()

        # Check if the file extension is supported
        if file_extension not in file_extension_map:
            raise ValueError(f"Unsupported file extension: {file_extension}. Supported extensions are: .gml, .graphml, .gexf, .csv, .txt.")

        # Handle .csv and .txt files with custom delimiters based on format (edgelist or adjlist)
        try:
            if file_extension in ['.csv', '.txt'] and self.csv_network_format:
                delimiter = ',' if file_extension == '.csv' else '\\t'
                try:
                    df_net = pd.read_csv(self.file_path, delimiter=delimiter)
                except pd.errors.ParserError:
                    raise ValueError(f"Error parsing the file {self.file_path}. Please check the file format or delimiter.")

                if self.csv_network_format == CSVNetworkFormat.EDGELIST:
                    # Assert that "source" and "target" columns are present in the DataFrame
                    required_columns = {"source", "target"}
                    assert required_columns.issubset(df_net.columns), f"CSV must contain columns named {required_columns} to name the source and target nodes."
                    
                    # Use additional columns as edge attributes, excluding "source" and "target"
                    edge_attributes = [col for col in df_net.columns if col not in required_columns]
                    
                    # Return a NetworkX graph object from the edgelist
                    return nx.from_pandas_edgelist(df_net, source="source", target="target", edge_attr=edge_attributes)
                elif self.csv_network_format == CSVNetworkFormat.ADJLIST:
                    return nx.from_pandas_adjacency(df_net)
                else:
                    raise ValueError(f"Unsupported format for CSV/TXT file: {self.csv_network_format}")
            
            # Return the NetworkX graph object created from the specified network file
            G = file_extension_map[file_extension](self.file_path)
            G = self._add_size_attribute(G)
            return G
        except Exception as e:
            raise RuntimeError(f"An error occurred while reading the network file: {str(e)}")
    
    def save_netwrok_image(self, G: nx.Graph, output_file: str, format: str, dpi: int=300) -> None:
        """
        Saves a NetworkX graph as an image file in the specified format and resolution.
        
        Parameters
        ----------
        G : networkx.Graph
            A NetworkX graph object.
        output_file : str
            The file path where the image should be saved.
        format : str
            The format of the image file (e.g., 'png', 'jpg', 'svg').
        dpi : int, optional
            The resolution of the image in dots per inch (default is 300).
        """
        # Check if the output file path is valid
        if not os.path.isdir(os.path.dirname(output_file)):
            raise FileNotFoundError(f"The directory for saving the file does not exist: {os.path.dirname(output_file)}.")
        
        # Validate image format
        valid_formats = ['png', 'jpg', 'jpeg', 'svg']
        if format.lower() not in valid_formats:
            raise ValueError(f"Invalid format: {format}. Supported formats are: {', '.join(valid_formats)}.")
        
        try:
            # Draw the graph and save it as an image file
            nx.draw(G, with_labels=True)
            plt.savefig(output_file, format=format, dpi=dpi)
            plt.clf()
        except Exception as e:
            raise RuntimeError(f"Failed to save the network image: {str(e)}")

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
        # Check if the network object and output file path are valid
        if not isinstance(G, nx.Graph):
            raise TypeError(f"The provided object is not a valid NetworkX graph: {type(G)}.")
        if not os.path.isdir(os.path.dirname(output_file)):
            raise FileNotFoundError(f"The directory for saving the file does not exist: {os.path.dirname(output_file)}.")
        
        try:
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
        
        except Exception as e:
            raise RuntimeError(f"Failed to create and save the PyVis network: {str(e)}")
    
    def _add_size_attribute(self, G: nx.Graph) -> nx.Graph:
        """
        Adds a 'size' attribute to the nodes of a NetworkX graph based on their degree centrality.
        
        Parameters
        ----------
        G : networkx.Graph
            A NetworkX graph object.

        Returns
        -------
        networkx.Graph
            A NetworkX graph object with the 'size' attribute added to the nodes.
        """
        # Clean up edge attributes to avoid conflicts
        for u, v, data in G.edges(data=True):
            data.pop('source', None)
            data.pop('target', None)

        # Assign node labels as their IDs
        for node in G.nodes(data=True):
            G.nodes[node[0]]['label'] = G.nodes[node[0]].get('name', node[0]) 

            # Obtain and set degree values for nodes
            degrees = {node: G.degree(node) for node in G.nodes()}
            
            # Assign sizes based on degrees
            min_size = 5  
            max_size = 30 
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
                
                G.nodes[node]['size'] = size 

        return G

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
    def __init__(self, id: int, name: str, file_path: str, file_format: DataFrameFormat, 
                 delimiter: Optional[str]=None, title: str=None, caption: str=None):
        """
        Initializes a DataFrame object.
        """
        super().__init__(id, name, file_path, component_type=ComponentType.DATAFRAME, title=title, caption=caption)
        self.file_format = file_format
        self.delimiter = delimiter

class Markdown(Component):
    """
    A Markdown text component within a subsection of a report.
    """
    component_type = ComponentType.MARKDOWN
    
@dataclass
class Subsection:
    """
    A subsection within a section, containing multiple components (plots, DataFrames, Markdown text, etc).

    Attributes
    ----------
    id : int
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
    id: int
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    components: List['Component'] = field(default_factory=list)

@dataclass
class Section:
    """
    A section within a report, containing multiple subsections.

    Attributes
    ----------
    id : int
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
    id: int
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
    id : int
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
    id: int
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    graphical_abstract: Optional[str] = None
    logo: Optional[str] = None
    sections: List['Section'] = field(default_factory=list)

class ReportView(ABC):
    """
    An abstract base class for report view implementations.

    Attributes
    ----------
    id : int
        A unique identifier for the report view ABC.
    name : str
        The name of the view.
    report : Report
        The report that this ABC is associated with.
    columns : List[str], optional
        Column names used in the report view ABC (default is None).
    
    """
    def __init__(self, id: int, name: str, report: 'Report', report_type: 'ReportType', columns: Optional[List[str]] = None):
        self.id = id
        self.name = name
        self.report = report
        self.report_type = report_type
        self.columns = columns or []

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
    def _generate_component_imports(self) -> str:
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
        str
            A str of import statements for the component.
        """
        pass 

class WebAppReportView(ReportView):
    """
    An abstract class for web application report views.
    """

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
    def _generate_subsection(self, subsection: Subsection) -> List[str]:
        """
        Generate code to render components (plots, dataframes, markdown) in the given subsection, 
        creating imports and content for the subsection based on the component type.

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
        pass