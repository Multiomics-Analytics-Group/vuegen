import os
import sys
import json
from dataclasses import dataclass, field
from typing import List, Optional
from streamlit.web import cli as stcli

@dataclass
class Report:
    """
    A report consisting of multiple sections.

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
    A section within a report, containing multiple plots.

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
    plots : List[Plot]
        A list of plots within this section.
    """
    identifier: int
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    plots: List['Plot'] = field(default_factory=list)


@dataclass
class Plot:
    """
    A plot within a section of a report.

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
class ReportView:
    """
    A base class for report view interfaces.

    Attributes
    ----------
    identifier : int
        A unique identifier for the report view interface.
    name : str
        The name of the view.
    columns : List[str], optional
        Column names used in the report view interface (default is None).
    interface_type : str, optional
        The type of the interface (e.g., 'WebAppReportView', 'DocumentReportView', PresentReportView, 'WikiReportView', 'NotebookReportView') (default is None).
    report : Report, optional
        The report that this interface is associated with (default is None).
    """
    identifier: int
    name: str
    columns: Optional[List[str]] = None
    interface_type: Optional[str] = None
    report: Optional[Report] = None


class StreamlitReportView(ReportView):
    """
    A Streamlit-based implementation of a report view interface.

    Methods
    -------
    generate_report(output_dir='tmp')
        Generates the Streamlit report and saves the report files to the specified directory.
    plot_sections(msg, output_dir)
        Generates Python files for each section in the report, containing the plots.
    run_report(output_dir='tmp')
        Runs the generated Streamlit report.
    """

    def __init__(self, identifier: int, name: str, columns: Optional[List[str]], report: Optional[Report] = None):
        super().__init__(identifier, name=name, columns=columns, interface_type='streamlit', report=report)

    def generate_report(self, output_dir: str = 'tmp') -> None:
        """
        Generates the Streamlit report and creates Python files for each section and plot.

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
        desc_msg = '''st.markdown("<h3 style='text-align: center; color: #020058;'>{}</h1>", unsafe_allow_html=True)'''.format(self.report.description)

        with open(os.path.join(output_dir, self.name.replace(" ", "_") + ".py"), 'w') as homepage:
            homepage.write(home_msg + "\n" + desc_msg)

        self.plot_sections(msg=home_msg, output_dir=pages_dir)

    def plot_sections(self, msg: str, output_dir: str) -> None:
        """
        Generates Python files for each section in the report, containing the plots.

        Parameters
        ----------
        msg : str
            The message to be included in each section file (usually the home message).
        output_dir : str
            The directory where section files will be saved.
        """
        for section in self.report.sections:
            section_desc_msg = '''st.markdown("<h2 style='text-align: center; color: #020058;'>{}</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #020058;'>{}</h1>", unsafe_allow_html=True)'''.format(section.name, section.description)

            with open(os.path.join(output_dir, section.name + ".py"), 'w') as pfile:
                bokeh_code = '''st.bokeh_chart({}, use_container_width=True)'''
                plotly_code = '''st.plotly_chart({}, use_container_width=True)'''
                code_chunk = []
                for plot in section.plots:
                    if plot.plot_type == 'bokeh':
                        code_chunk.append(bokeh_code.format(plot.read_plot_code()))
                    elif plot.plot_type == 'plotly':
                        code_chunk.append(plotly_code.format(plot.read_plot_code()))
                pfile.write('{}\n{}\nimport holoviews as hv\nfrom holoviews import opts, dim\n{}'.format(
                    msg, section_desc_msg, "\n".join(code_chunk)))

    def run_report(self, output_dir: str = 'tmp') -> None:
        """
        Runs the generated Streamlit report.

        Parameters
        ----------
        output_dir : str, optional
            The directory where the report was generated (default is 'tmp').
        """
        sys.argv = ["streamlit", "run", os.path.join(output_dir, self.name + ".py")]
        sys.exit(stcli.main())