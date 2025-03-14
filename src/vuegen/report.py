import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import auto

try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum

from typing import ClassVar, List, Optional

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import requests
from pyvis.network import Network

from .utils import cyjs_to_networkx, fetch_file_stream, pyvishtml_to_networkx


class ReportType(StrEnum):
    STREAMLIT = auto()
    HTML = auto()
    PDF = auto()
    DOCX = auto()
    ODT = auto()
    REVEALJS = auto()
    PPTX = auto()
    JUPYTER = auto()


class ComponentType(StrEnum):
    PLOT = auto()
    DATAFRAME = auto()
    MARKDOWN = auto()
    HTML = auto()
    APICALL = auto()
    CHATBOT = auto()


class PlotType(StrEnum):
    STATIC = auto()
    PLOTLY = auto()
    ALTAIR = auto()
    INTERACTIVE_NETWORK = auto()


class NetworkFormat(StrEnum):
    GML = auto()
    GRAPHML = auto()
    GEXF = auto()
    CSV = auto()
    TXT = auto()
    CYJS = auto()
    HTML = auto()
    PNG = auto()
    JPG = auto()
    JPEG = auto()
    SVG = auto()

    @property
    def value_with_dot(self):
        """Return the file extension with the dot."""
        return f".{self.name.lower()}"


class CSVNetworkFormat(StrEnum):
    EDGELIST = auto()
    ADJLIST = auto()


class DataFrameFormat(StrEnum):
    CSV = auto()
    TXT = auto()
    PARQUET = auto()
    XLS = auto()
    XLSX = auto()

    @property
    def value_with_dot(self):
        """Return the file extension with the dot."""
        return f".{self.name.lower()}"


@dataclass
class Component:
    """
    Base class for different components in a report subsection. It encapsulates elements like
    plots, dataframes, markdown, or apicalls, providing a consistent structure for report generation.

    Attributes
    ----------
    _id_counter : ClassVar[int]
        Class-level counter for unique IDs.
    id : int
        Unique identifier for the component, assigned automatically when an object is created.
    title : str
        Title of the component.
    component_type : ComponentType
        Type of the component (e.g., PLOT, DATAFRAME, MARKDOWN, APICALL).
    logger : logging.Logger
        Logger object for tracking warnings, errors, and info messages.
    file_path : Optional[str]
        Path to the file associated with the component (e.g., plot JSON file, image file, csv file, etc.).
    caption : Optional[str]
        Caption providing additional context about the component (default: None).
    """

    _id_counter: ClassVar[int] = 0
    id: int = field(init=False)
    title: str
    component_type: ComponentType
    logger: logging.Logger
    file_path: Optional[str] = None
    caption: Optional[str] = None

    def __post_init__(self):
        self.id = self._generate_id()

    @classmethod
    def _generate_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter


class Plot(Component):
    """
    A plot within a subsection of a report.

    Attributes
    ----------
    plot_type : PlotType
        The type of the plot (INTERACTIVE or STATIC).
    csv_network_format : CSVNetworkFormat, optional
        The format of the CSV file for network plots (EDGELIST or ADJLIST) (default is None).
    """

    def __init__(
        self,
        title: str,
        logger: logging.Logger,
        plot_type: PlotType,
        file_path: str = None,
        caption: str = None,
        csv_network_format: Optional[CSVNetworkFormat] = None,
    ):
        """
        Initializes a Plot object.
        """
        # Call the constructor of the parent class (Component) to set common attributes
        super().__init__(
            title=title,
            logger=logger,
            component_type=ComponentType.PLOT,
            file_path=file_path,
            caption=caption,
        )

        # Set specific attributes for the Plot class
        self.plot_type = plot_type
        self.csv_network_format = csv_network_format

    def read_network(self) -> nx.Graph:
        """
        Reads the network file and returns a NetworkX graph object.

        Returns
        -------
        G : networkx.Graph
            A NetworkX graph object created from the specified network file.

        Raises
        ------
        ValueError
            If the file format is unsupported.
        FileNotFoundError
            If the file cannot be accessed or is missing.
        RuntimeError
            If there is an error while reading the network file.
        """
        # Mapping of file extensions to NetworkX and custom loading functions
        file_extension_map = {
            NetworkFormat.GML.value_with_dot: nx.read_gml,
            NetworkFormat.GRAPHML.value_with_dot: nx.read_graphml,
            NetworkFormat.GEXF.value_with_dot: nx.read_gexf,
            NetworkFormat.CYJS.value_with_dot: cyjs_to_networkx,
        }

        # Handle .csv and .txt files with custom delimiters based on the text format (edgelist or adjlist)
        try:
            # Fetch the file stream (local or URL) using fetch_file_stream
            file_stream = fetch_file_stream(self.file_path)

            # Determine the file extension and check if it is supported
            file_extension = os.path.splitext(self.file_path)[-1].lower()

            # Check if the file extension matches any Enum value
            if not any(file_extension == fmt.value_with_dot for fmt in NetworkFormat):
                self.logger.error(
                    f"Unsupported file extension: {file_extension}. Supported extensions are: {', '.join(fmt.value for fmt in NetworkFormat)}."
                )

            # Handle HTML files for pyvis interactive networks
            if file_extension == NetworkFormat.HTML.value_with_dot:
                G = pyvishtml_to_networkx(file_stream)
                return (G, self.file_path)

            # Handle CSV and TXT files with custom delimiters based on the text format (edgelist or adjlist)
            if (
                file_extension
                in [NetworkFormat.CSV.value_with_dot, NetworkFormat.TXT.value_with_dot]
                and self.csv_network_format
            ):
                delimiter = "," if file_extension == ".csv" else "\\t"
                try:
                    df_net = pd.read_csv(file_stream, delimiter=delimiter)
                except pd.errors.ParserError:
                    self.logger.error(
                        f"Error parsing CSV/TXT file {self.file_path}. Please check the file format or delimiter."
                    )

                if self.csv_network_format == CSVNetworkFormat.EDGELIST:
                    # Assert that "source" and "target" columns are present in the DataFrame
                    required_columns = {"source", "target"}
                    if not required_columns.issubset(df_net.columns):
                        missing_cols = ", ".join(
                            required_columns.difference(df_net.columns)
                        )
                        self.logger.error(
                            f"CSV network file must contain 'source' and 'target' columns. Missing columns: {missing_cols}."
                        )

                    # Use additional columns as edge attributes, excluding "source" and "target"
                    edge_attributes = [
                        col for col in df_net.columns if col not in required_columns
                    ]

                    # Return a NetworkX graph object from the edgelist
                    if edge_attributes:
                        G = nx.from_pandas_edgelist(
                            df_net,
                            source="source",
                            target="target",
                            edge_attr=edge_attributes,
                        )
                    else:
                        G = nx.from_pandas_edgelist(
                            df_net, source="source", target="target"
                        )

                    self.logger.info(
                        f"Successfully read network from file: {self.file_path}."
                    )
                    return G
                elif self.csv_network_format == CSVNetworkFormat.ADJLIST:
                    G = nx.from_pandas_adjacency(df_net)
                    self.logger.info(
                        f"Successfully read network from file: {self.file_path}."
                    )
                    return G
                else:
                    self.logger.error(
                        f"Unsupported format for CSV/TXT file: {self.csv_network_format}."
                    )

            # Handle other formats using the mapping and return the NetworkX graph object from the specified network file
            G = file_extension_map[file_extension](file_stream)
            G = self._add_size_attribute(G)
            self.logger.info(f"Successfully read network from file: {self.file_path}.")
            return G
        except Exception as e:
            self.logger.error(f"Error occurred while reading network file: {str(e)}.")
            raise RuntimeError(
                f"An error occurred while reading the network file: {str(e)}"
            )

    def save_network_image(
        self, G: nx.Graph, output_file: str, format: str, dpi: int = 300
    ) -> None:
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
        self.logger.debug("Try to save network as PyVis network: %s.", output_file)
        # Check if the output file path is valid
        if not os.path.isdir(os.path.dirname(output_file)):
            self.logger.error(
                f"Directory for saving image does not exist: {os.path.dirname(output_file)}."
            )
            raise FileNotFoundError(
                f"The directory for saving the file does not exist: {os.path.dirname(output_file)}."
            )

        # Validate image format
        valid_formats = ["png", "jpg", "jpeg", "svg"]
        if format.lower() not in valid_formats:
            self.logger.error(
                f"Invalid image format: {format}. Supported formats are: {', '.join(valid_formats)}."
            )
            raise ValueError(
                f"Invalid format: {format}. Supported formats are: {', '.join(valid_formats)}."
            )

        try:
            # Draw the graph and save it as an image file
            nx.draw(G, with_labels=False)
            plt.savefig(output_file, format=format, dpi=dpi)
            plt.clf()
            self.logger.info(f"Network image saved successfully at: {output_file}.")
        except Exception as e:
            self.logger.error(f"Failed to save the network image: {str(e)}.")
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
        self.logger.debug("Try to save network as PyVis network: %s.", output_file)
        # Check if the network object and output file path are valid
        if not isinstance(G, nx.Graph):
            self.logger.error(
                f"Provided object is not a valid NetworkX graph: {type(G)}."
            )
            raise TypeError(
                f"The provided object is not a valid NetworkX graph: {type(G)}."
            )
        if not os.path.isdir(os.path.dirname(output_file)):
            self.logger.error(
                f"Directory for saving PyVis network does not exist: {os.path.dirname(output_file)}."
            )
            raise FileNotFoundError(
                f"The directory for saving the file does not exist: {os.path.dirname(output_file)}."
            )

        try:
            # Create a PyVis network object
            net = Network(
                height="600px", width="100%", bgcolor="white", font_color="black"
            )
            net.from_nx(G)

            # Customize the network visualization of nodes
            for node in net.nodes:
                node_id = node["id"]
                node_data = G.nodes[node_id]
                node["label"] = node_data.get("name", node_id)
                node["font"] = {"size": 12}
                node["borderWidth"] = 2
                node["borderWidthSelected"] = 2.5

            # Apply the force_atlas_2based layout and show panel to control layout
            net.force_atlas_2based(
                gravity=-30,
                central_gravity=0.005,
                spring_length=100,
                spring_strength=0.1,
                damping=0.4,
            )
            net.show_buttons(filter_=["physics"])

            # Save the network as an HTML file
            net.save_graph(str(output_file))
            self.logger.info(f"PyVis network created and saved as: {output_file}.")
            return net

        except Exception as e:
            self.logger.error(f"Failed to create and save PyVis network: {str(e)}.")
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
            data.pop("source", None)
            data.pop("target", None)

        # Assign node labels as their IDs
        for node in G.nodes(data=True):
            G.nodes[node[0]]["label"] = G.nodes[node[0]].get("name", node[0])

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
                    size = min_size + (max_size - min_size) * (
                        (degree - min_degree) / (max_degree - min_degree)
                    )

                G.nodes[node]["size"] = size
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

    def __init__(
        self,
        title: str,
        logger: logging.Logger,
        file_format: DataFrameFormat,
        file_path: str = None,
        caption: str = None,
        delimiter: Optional[str] = None,
    ):
        """
        Initializes a DataFrame object.
        """
        super().__init__(
            title=title,
            logger=logger,
            component_type=ComponentType.DATAFRAME,
            file_path=file_path,
            caption=caption,
        )
        self.file_format = file_format
        self.delimiter = delimiter


class Markdown(Component):
    """
    A Markdown text component within a subsection of a report.
    """

    def __init__(
        self,
        title: str,
        logger: logging.Logger,
        file_path: str = None,
        caption: str = None,
    ):
        """
        Initializes a Markdown object.
        """
        super().__init__(
            title=title,
            logger=logger,
            component_type=ComponentType.MARKDOWN,
            file_path=file_path,
            caption=caption,
        )


class Html(Component):
    """
    An html component within a subsection of a report.
    """

    def __init__(
        self,
        title: str,
        logger: logging.Logger,
        file_path: str = None,
        caption: str = None,
    ):
        """
        Initializes an html object.
        """
        super().__init__(
            title=title,
            logger=logger,
            component_type=ComponentType.HTML,
            file_path=file_path,
            caption=caption,
        )


class APICall(Component):
    """
    A component for interacting with APIs in a report.

    Attributes
    ----------
    api_url : str
        The URL of the API to interact with.
    headers : Optional[dict]
        Headers to include in the API request (default is None).
    params : Optional[dict]
        Query parameters to include in the API request (default is None).
    """

    def __init__(
        self,
        title: str,
        logger: logging.Logger,
        api_url: str,
        caption: str = None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
    ):
        super().__init__(
            title=title,
            logger=logger,
            component_type=ComponentType.APICALL,
            caption=caption,
        )
        self.api_url = api_url
        self.headers = headers or {}
        self.params = params or {}

    def make_api_request(
        self, method: str, request_body: Optional[dict] = None
    ) -> Optional[dict]:
        """
        Sends an HTTP request to the specified API and returns the JSON response.

        Parameters
        ----------
        method : str
            HTTP method to use for the request.
        request_body : Optional[dict], optional
            The request body for POST or PUT methods (default is None).

        Returns
        -------
        response : Optional[dict]
            The JSON response from the API, or None if the request fails.
        """
        try:
            self.logger.info(f"Making {method} request to API: {self.api_url}")
            response = requests.request(
                method,
                self.api_url,
                headers=self.headers,
                params=self.params,
                json=request_body,
            )
            response.raise_for_status()
            self.logger.info(
                f"Request successful with status code {response.status_code}."
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            return None


class ChatBot(Component):
    """
    A component for creating a ChatBot that interacts with an API.
    This component uses an APICall instance to send requests to the chatbot API and receive responses.

    Attributes
    ----------
    model : str
        The language model to use for the chatbot.
    api_call : APICall
        An instance of the APICall class used to interact with the API for fetching chatbot responses.
    headers : Optional[dict]
        Headers to include in the API request (default is None).
    params : Optional[dict]
        Query parameters to include in the API request (default is None).
    """

    def __init__(
        self,
        title: str,
        logger: logging.Logger,
        api_url: str,
        model: str,
        caption: str = None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
    ):
        super().__init__(
            title=title,
            logger=logger,
            component_type=ComponentType.CHATBOT,
            caption=caption,
        )
        self.model = model
        self.api_call = APICall(
            title=title,
            logger=logger,
            api_url=api_url,
            caption=caption,
            headers=headers,
            params=params,
        )


@dataclass
class Subsection:
    """
    A subsection within a section, containing multiple components (plots, dataFrames,
    markdown text, apicals, etc).

    Attributes
    ----------
    _id_counter : ClassVar[int]
        Class-level counter for unique IDs.
    id : int
        Unique identifier for the subsection, assigned automatically when an object is created.
    title : str
        Title of the subsection.
    components : List[Component]
        A list of components within the subsection.
    description : str, optional
        A description of the subsection (default is None).
    """

    _id_counter: ClassVar[int] = 0
    id: int = field(init=False)
    title: str
    components: List["Component"] = field(default_factory=list)
    description: Optional[str] = None

    def __post_init__(self):
        self.id = self._generate_id()

    @classmethod
    def _generate_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter


@dataclass
class Section:
    """
    A section within a report, containing multiple subsections.

    Attributes
    ----------
    _id_counter : ClassVar[int]
        Class-level counter for unique IDs.
    id : int
        Unique identifier for the section, assigned automatically when an object is created.
    title : str
        Title of the section.
    subsections : List[Subsection]
        A list of subsections within the section.
    description : str, optional
        A description of the section (default is None).
    """

    _id_counter: ClassVar[int] = 0
    id: int = field(init=False)
    title: str
    subsections: List["Subsection"] = field(default_factory=list)
    description: Optional[str] = None

    def __post_init__(self):
        self.id = self._generate_id()

    @classmethod
    def _generate_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter


@dataclass
class Report:
    """
    A report consisting of multiple sections and subsections.

    Attributes
    ----------
    title : str
        Title of the report.
    logger : logging.Logger
        Logger object for tracking warnings, errors, and info messages.
    sections : List[Section]
        A list of sections that belong to the report.
    description : str, optional
        Description of the report (default is None).
    graphical_abstract : str, optional
        Path to the graphical abstract image (default is None).
    logo : str, optional
        The file path to the logo image (default is None).
    """

    title: str
    logger: logging.Logger
    sections: List["Section"] = field(default_factory=list)
    description: Optional[str] = None
    graphical_abstract: Optional[str] = None
    logo: Optional[str] = None


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
    report_type : ReportType
        The report type. It should be one of the values of the ReportType Enum.

    """

    def __init__(self, report: "Report", report_type: "ReportType"):
        self.report = report
        self.report_type = report_type

    @abstractmethod
    def generate_report(self, output_dir: str = "sections") -> None:
        """
        Generates the report and creates output files.

        Parameters
        ----------
        output_dir : str, optional
            The folder where the generated report files will be saved (default is 'sections').
        """
        pass

    @abstractmethod
    def run_report(self, output_dir: str = "sections") -> None:
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
    def _generate_subsection(
        self, subsection: Subsection
    ) -> tuple[List[str], List[str]]:
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
