import os
import sys
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
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
        The type of the plot (e.g., 'plotly', 'bokeh').
    title : str, optional
        The title of the plot (default is None).
    caption : str, optional
        A caption for the plot (default is None).
    code : str, optional
        The code representing the plot, stored as a JSON string (default is None).

    Methods
    -------
    read_plot_code()
        Reads and parses the plot code from the stored JSON string.
    """
    identifier: int
    name: str
    plot_type: str
    title: Optional[str] = None
    caption: Optional[str] = None
    code: Optional[str] = None

    def read_plot_code(self) -> str:
        """
        Reads and parses the plot code from the stored JSON string.

        Returns
        -------
        str
            A string representation of the parsed plot code.
        """
        plot_dict = json.loads(self.code) if self.code else {}
        return str(plot_dict)


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
    framework : str
        The web app framework used (e.g., 'Streamlit').

    Methods
    -------
    run_report(output_dir='tmp')
        Runs the generated web app report.
    _build_plots(output_dir='tmp')
        Generates plots for each section in the report.
    """

    framework: str

    def __init__(self, identifier: int, name: str, columns: Optional[List[str]], framework: str, report: Report):
        super().__init__(identifier, name=name, columns=columns, interface_type='WebAppReportView', report=report)
        self.framework = framework

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
        super().__init__(identifier, name=name, columns=columns, framework='Streamlit', report=report)

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
            section_desc_msg = f"""st.markdown("<h2 style='text-align: center; color: #020058;'>{section.name}</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #020058;'>{section.description}</h3>", unsafe_allow_html=True)"""

            with open(os.path.join(output_dir, section.name.replace(" ", "_") + ".py"), 'w') as section_file:
                # Start the section file with the home message
                section_file.write(f'import streamlit as st\n{section_desc_msg}\n')

                # Iterate through subsections and integrate them into the section file
                for subsection in section.subsections:
                    subsection_desc_msg = f"""st.markdown("<h3 style='text-align: center; color: #023558;'>{subsection.name}</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #024558;'>{subsection.description}</h4>", unsafe_allow_html=True)"""
                    
                    # Write the subsection description first
                    section_file.write(subsection_desc_msg + "\n")
                    
                    # Iterate through plots in the subsection
                    for plot in subsection.plots:
                        if plot.plot_type == 'bokeh':
                            section_file.write(f"st.bokeh_chart({plot.read_plot_code()}, use_container_width=True)\n")
                        elif plot.plot_type == 'plotly':
                            section_file.write(f"st.plotly_chart({plot.read_plot_code()}, use_container_width=True)\n")


