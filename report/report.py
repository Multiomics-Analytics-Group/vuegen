import os
import sys
import json
from dataclasses import dataclass, field
from streamlit.web import cli as stcli

@dataclass
class Report:
    identifier: int
    name: str
    title: str = None
    description: str = None
    sections: list = field(default_factory=list)

@dataclass
class Section:
    identifier: int
    name: str
    title: str = None
    description: str = None
    plots: list = field(default_factory=list)

@dataclass
class Plot:
    identifier: int
    name: str
    plot_type: str
    title: str = None
    caption: str = None
    code: str = None

    def read_plot_code(self):
        plot_dict = json.loads(self.code)
        return str(plot_dict)

class ReportInterface:
    def __init__(self, identifier, name, columns=None, interface_type=None, report=None):
        self._identifier = identifier
        self._name = name
        self._type = interface_type
        self._columns = columns
        self._report = report

class StreamlitReport(ReportInterface):
    def __init__(self, identifier, name, columns, report=None):
        super().__init__(identifier, name=name, columns=columns, interface_type='streamlit', report=report)

    def generate_report(self, output_dir='tmp'):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        if not os.path.exists(os.path.join(output_dir, 'pages')):
            os.mkdir(os.path.join(output_dir, 'pages'))

        pages_dir = os.path.join(output_dir, 'pages')
        home_msg = f'''import streamlit as st
st.set_page_config(layout="wide", page_title="{self._name}", menu_items={{}})
st.markdown("<h1 style='text-align: center; color: #023858;'>{self._name}</h1>", unsafe_allow_html=True)'''
        desc_msg = f'''st.markdown("<h3 style='text-align: center; color: #020058;'>{self._report.description}</h3>", unsafe_allow_html=True)'''
        
        with open(os.path.join(output_dir, self._name.replace(" ", "_")+".py"), 'w') as homepage:
            homepage.write(home_msg+"\n"+desc_msg)
        
        self.plot_sections(msg=home_msg, output_dir=pages_dir)

    def plot_sections(self, msg, output_dir):
        for section in self._report.sections:
            section_desc_msg = f'''st.markdown("<h2 style='text-align: center; color: #020058;'>{section.name}</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #020058;'>{section.description}</h3>", unsafe_allow_html=True)'''
            
            with open(os.path.join(output_dir, section.name+".py"), 'w') as pfile:
                bokeh_code = '''st.bokeh_chart({}, use_container_width=True)'''
                plotly_code = '''st.plotly_chart({}, use_container_width=True)'''
                code_chunk = []
                
                for plot in section.plots:
                    plot_type = plot.plot_type
                    if plot_type == 'bokeh':
                        code_chunk.append(bokeh_code.format(plot.read_plot_code()))
                    elif plot_type == 'plotly':
                        code_chunk.append(plotly_code.format(plot.read_plot_code()))

                pfile.write(f'''{msg}
{section_desc_msg}
import holoviews as hv
from holoviews import opts, dim
{"\n".join(code_chunk)}''')

    def run_report(self, output_dir='tmp'):
        sys.argv = ["streamlit", "run", os.path.join(output_dir, self._name+".py")]
        sys.exit(stcli.main())