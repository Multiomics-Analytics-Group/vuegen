import os
import sys
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
import altair as alt
from streamlit.web import cli as stcli

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
    """
    identifier: int
    name: str
    plot_type: str
    file_path: str
    visualization_tool: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None

    def read_plot_fromjson(self) -> str:
        """
        Reads and parses the JSON representation of the plot. 

        Returns
        -------
        str
            A string representation of the parsed plot code.
        """
        if self.plot_type == 'interactive':
            plot_dict = json.loads(self.file_path) if self.file_path else {}
            if self.visualization_tool == 'altair':
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
            #with open(section_file_path, 'w') as section_file:
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
                            #section_file.write('import altair as alt\nimport json\n')
                            section_content.append(f"st.vega_lite_chart(json.loads(alt.Chart.from_dict({plot.read_plot_fromjson()}).to_json()), use_container_width=True)\n")
                    elif plot.plot_type == 'static':
                        section_content.append(f"st.image('{plot.file_path}', caption='{plot.caption}', use_column_width=True)\n")

            # Write everything to the file
            with open(section_file_path, 'w') as section_file:
                # Write imports at the top of the file
                section_file.write("\n".join(imports) + "\n\n")

                # Write the section content (descriptions, plots)
                section_file.write("\n".join(section_content))




