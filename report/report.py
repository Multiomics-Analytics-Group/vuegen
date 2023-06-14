import os
import sys
from streamlit.web import cli as stcli
import json

class Report:
    def __init__(self, identifier, name, title=None, description=None, sections=[]):
        self._identifier = identifier
        self._name = name
        self._title = title
        self._description = description
        self._sections = sections
        

class Section:
    def __init__(self, identifier, name, title=None, description=None, plots=[]):
        self._identifier = identifier
        self._name = name
        self._title = title
        self._description = description
        self._plots = plots
        
        
class Plot:
    def __init__(self, identifier, name, plot_type, title=None, caption=None, code=None):
        self._identifier = identifier
        self._name = name
        self._type = plot_type
        self._title = title
        self._caption = caption
        self._code = code
        
    def read_plot_code(self):
        plot_dict = json.loads(self._code)
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
        ReportInterface.__init__(self, identifier, name=name, columns=columns, interface_type='streamlit', report=report)

    def generate_report(self, output_dir='tmp'):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        if not os.path.exists(os.path.join(output_dir, 'pages')):
            os.mkdir(os.path.join(output_dir, 'pages'))
        
        pages_dir = os.path.join(output_dir, 'pages')
        home_msg = '''import streamlit as st
st.set_page_config(layout="wide", page_title="{}", menu_items={{}})
st.markdown("<h1 style='text-align: center; color: #023858;'>{}</h1>", unsafe_allow_html=True)'''.format(self._name, self._name)
        desc_msg = '''st.markdown("<h3 style='text-align: center; color: #020058;'>{}</h1>", unsafe_allow_html=True)'''.format(self._report._description)
        with open(os.path.join(output_dir, self._name.replace(" ", "_")+".py"), 'w') as homepage:
            homepage.write(home_msg+"\n"+desc_msg)
        
        self.plot_sections(msg=home_msg, output_dir=pages_dir)
        
    def plot_sections(self, msg, output_dir):
        for section in self._report._sections:
                section_desc_msg = '''st.markdown("<h2 style='text-align: center; color: #020058;'>{}</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #020058;'>{}</h1>", unsafe_allow_html=True)'''.format(section._name, section._description)
                with open(os.path.join(output_dir, section._name+".py"), 'w') as pfile:
                    bokeh_code = '''st.bokeh_chart({}, use_container_width=True)'''
                    plotly_code = '''st.plotly_chart({}, use_container_width=True)'''
                    code_chunk = []
                    for plot in section._plots:
                        plot_type = plot._type
                        if plot_type == 'bokeh':
                            code_chunk.append(bokeh_code.format(plot.read_plot_code()))
                        elif plot_type == 'plotly':
                            code_chunk.append(plotly_code.format(plot.read_plot_code()))
                    pfile.write('''{}
{}
import holoviews as hv
from holoviews import opts, dim
{}'''.format(msg, section_desc_msg, "\n".join(code_chunk)))
    
    
    def run_report(self, output_dir='tmp'):
        sys.argv = ["streamlit", "run", os.path.join(output_dir, self._name+".py")]
        sys.exit(stcli.main())