import os
import sys
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
import altair as alt
from streamlit.web import cli as stcli
import networkx as nx
from pyvis.network import Network

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
    sections : List[Section]
        A list of sections that belong to the report.
    """
    identifier: int
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    sections: List['Section'] = field(default_factory=list)


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
class Subsection:
    """
    A subsection within a section, containing multiple plots.

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
    plots : List[Plot]
        A list of plots within this subsection.
    """
    identifier: int
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    plots: List['Plot'] = field(default_factory=list)


@dataclass
class Plot:
    """
    A plot within a subsection of a report.

    Attributes
    ----------
    identifier : int
        A unique identifier for the plot.
    name : str
        The name of the plot.
    plot_type : str
        The type of the plot ('interactive' or 'static').
    file_path : str
        The file path for the JSON representation of the plot (for interactive plots) or the image file path (for static plots).
    visualization_tool : str, optional
        The visualization_tool for rendering interactive plots ('plotly', 'bokeh', or 'altair'). 
        It is not required for static plots (default is None).
    title : str, optional
        The title of the plot (default is None).
    caption : str, optional
        A caption for the plot (default is None).
    csv_network_format : str, optional
        The format of the CSV file for network plots (edgelist or adjlist) (default is None).
    """
    identifier: int
    name: str
    plot_type: str
    file_path: str
    visualization_tool: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    csv_network_format: Optional[str] = None

    def read_plot_fromjson(self) -> str:
        """
        Reads and parses the JSON representation of the plot. 

        Returns
        -------
        str
            A string representation of the parsed plot code.
        """
        if self.plot_type == 'interactive':
            with open(self.file_path, 'r') as plot_file:
                plot_json = plot_file.read()
            plot_dict = json.loads(plot_json) if plot_json else {}
            if self.visualization_tool == 'altair':
                altair_plot = alt.Chart.from_dict(plot_dict)
                return altair_plot.to_dict()
            return str(plot_dict)
        return ""

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
                if self.csv_network_format == 'edgelist':
                    G = nx.read_edgelist(self.file_path, delimiter=',')
                elif self.csv_network_format == 'adjlist':
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
        """
        # Create a PyVis network object
        net = Network(height='600px', width='100%', bgcolor='white', font_color='black')
        net.from_nx(G)

        # Optionally customize nodes
        for node in net.nodes:
            node_id = node['id']
            node_data = G.nodes[node_id]
            node['font'] = {'size': 12}
            node_data.get('name', node_id)
            node['borderWidth'] = 2
            node['borderWidthSelected'] = 2.5

        # Save the network as an HTML file
        net.save_graph(output_file)

        return net
    
    def generate_imports(self) -> str:
        """
        Generate the import statements required for the visualization tool.

        Returns
        -------
        str
            A string representing the import statements needed for the plot.
        """
        imports = []
        if self.visualization_tool == 'altair':
            imports.append('import altair as alt')
            imports.append('import json')
        return "\n".join(imports)

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
    def generate_report(self, output_dir: str = 'tmp') -> None:
        """
        Generates the report and creates output files.
        
        Parameters
        ----------
        output_dir : str, optional
            The directory where the generated report files will be saved (default is 'tmp').
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
    run_report(output_dir='tmp')
        Runs the generated web app report.
    _build_plots(output_dir='tmp')
        Generates plots for each section in the report.
    """

    report_framework: str

    def __init__(self, identifier: int, name: str, columns: Optional[List[str]], report_framework: str, report: Report):
        super().__init__(identifier, name=name, columns=columns, interface_type='WebAppReportView', report=report)
        self.report_framework = report_framework

    @abstractmethod
    def run_report(self, output_dir: str = 'tmp') -> None:
        """
        Runs the generated report.

        Parameters
        ----------
        output_dir : str, optional
            The directory where the report was generated (default is 'tmp').
        """
        pass

    @abstractmethod
    def _build_plots(self, output_dir: str) -> None:
        """
        Generates and organizes plots for each subsection and section in the report.
        
        Parameters
        ----------
        output_dir : str
            The directory where section files will be saved.

        Notes
        -----
        This method is intended to be used internally by the `generate_report` method.
        """
        pass


class StreamlitReportView(WebAppReportView):
    """
    A Streamlit-based implementation of a report view interface.

    Methods
    -------
    generate_report(output_dir='tmp')
        Generates the Streamlit report and saves the report files to the specified directory.
    run_report(output_dir='tmp')
        Runs the generated Streamlit report.
    _build_plots(output_dir='tmp')
        Generates Python files for each section in the report, containing the plots.
    """

    def __init__(self, identifier: int, name: str, columns: Optional[List[str]], report: Report):
        super().__init__(identifier, name=name, columns=columns, report_framework='Streamlit', report=report)

    def generate_report(self, output_dir: str = 'tmp') -> None:
        """
        Generates the Streamlit report and creates Python files for each section and its subsections and plots.

        Parameters
        ----------
        output_dir : str, optional
            The directory where the generated report files will be saved (default is 'tmp').
        """
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        if not os.path.exists(os.path.join(output_dir, 'pages')):
            os.mkdir(os.path.join(output_dir, 'pages'))

        pages_dir = os.path.join(output_dir, 'pages')
        home_msg = '''import streamlit as st
st.set_page_config(layout="wide", page_title="{}", menu_items={{}})
st.markdown("<h1 style='text-align: center; color: #023858;'>{}</h1>", unsafe_allow_html=True)'''.format(self.name, self.name)
        desc_msg = '''st.markdown("<h3 style='text-align: center; color: #020058;'>{}</h3>", unsafe_allow_html=True)'''.format(self.report.description)

        with open(os.path.join(output_dir, self.name.replace(" ", "_") + ".py"), 'w') as homepage:
            homepage.write(home_msg + "\n" + desc_msg)

        self._build_plots(output_dir=pages_dir)

    def run_report(self, output_dir: str = 'tmp') -> None:
        """
        Runs the generated Streamlit report.

        Parameters
        ----------
        output_dir : str, optional
            The directory where the report was generated (default is 'tmp').
        """
        sys.argv = ["streamlit", "run", os.path.join(output_dir, self.name.replace(" ", "_") + ".py")]
        sys.exit(stcli.main())

    def _build_plots(self, output_dir: str) -> None:
        """
        Generates Python files for each section in the report, including subsections and plots.
        
        Parameters
        ----------
        output_dir : str
            The directory where section files will be saved.
        """
        for section in self.report.sections:
            # Create the section file
            section_file_path = os.path.join(output_dir, section.name.replace(" ", "_") + ".py")
            # Track imports to avoid duplication
            imports_written = set() 
            
            # Collect section and subsection descriptions
            section_desc_msg = f"""st.markdown("<h2 style='text-align: center; color: #020058;'>{section.name}</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #020058;'>{section.description}</h3>", unsafe_allow_html=True)"""
        
            # Collect imports and section content
            imports = ['import streamlit as st']
            section_content = [section_desc_msg]

            # Iterate through subsections and integrate them into the section file
            for subsection in section.subsections:
                subsection_desc_msg = f"""st.markdown("<h3 style='text-align: center; color: #023558;'>{subsection.name}</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #024558;'>{subsection.description}</h4>", unsafe_allow_html=True)"""
                
                # Add subsection description to section content
                section_content.append(subsection_desc_msg)
                
                # Iterate through plots in the subsection
                for plot in subsection.plots:
                    # Write imports if not already done
                    imports_viz = plot.generate_imports()
                    if imports_viz and plot.visualization_tool not in imports_written:
                        imports.append(imports_viz)
                        imports_written.add(plot.visualization_tool)
                    
                    if plot.plot_type == 'interactive':
                        if plot.visualization_tool == 'plotly':
                            section_content.append(f"st.plotly_chart({plot.read_plot_fromjson()}, use_container_width=True)\n")
                        #elif plot.visualization_tool == 'bokeh':
                        #section_file.write(f"st.bokeh_chart({plot.read_plot_code()}, use_container_width=True)\n")
                        elif plot.visualization_tool == 'altair':
                            section_content.append(f"st.vega_lite_chart(json.loads(alt.Chart.from_dict({plot.read_plot_fromjson()}).to_json()), use_container_width=True)\n")
                        elif plot.visualization_tool == 'pyvis':
                            G = plot.read_network()
                            output_file = f"example_data/{plot.name.replace(' ', '_')}.html"  # Define the output file name
                            net = plot.create_and_save_pyvis_network(G, output_file)  # Get the Network object

                            # Write code to display the network in the Streamlit app
                            section_content.append(f"""with open('{output_file}', 'r') as f:\n""")
                            section_content.append(f"""    html_data = f.read()\n""")
                            section_content.append(f"""st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of nodes:</b> {len(net.nodes)} </p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: black;'> <b>Number of relationships:</b> {len(net.edges)} </p>", unsafe_allow_html=True)""")                         
                            section_content.append(f"""st.components.v1.html(html_data, height=600)\n""")
                    elif plot.plot_type == 'static':
                        section_content.append(f"st.image('{plot.file_path}', caption='{plot.caption}', use_column_width=True)\n")

            # Write everything to the file
            with open(section_file_path, 'w') as section_file:
                # Write imports at the top of the file
                section_file.write("\n".join(imports) + "\n\n")

                # Write the section content (descriptions, plots)
                section_file.write("\n".join(section_content))




