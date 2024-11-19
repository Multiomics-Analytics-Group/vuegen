import streamlit_reportview as st_reportview
import quarto_reportview as doc_reportview
from metadata_manager import MetadataManager
from report import ReportType
from helpers.utils import assert_enum_value

if __name__ == '__main__':
    # Load report object and  metadata from YAML file
    yaml_manager = MetadataManager()
    report, report_metadata = yaml_manager.load_report_metadata('./report_metadata_micw2graph.yaml')

    # Create report view
    doc_report = doc_reportview.QuartoReportView(report_metadata['report']['id'], 
                                                report_metadata['report']['name'], 
                                                report=report, 
                                                report_type = assert_enum_value(ReportType, report_metadata['report']['report_type'], report.logger),
                                                report_format = assert_enum_value(doc_reportview.ReportFormat, report_metadata['report']['report_format'], report.logger),
                                                columns=None)
    doc_report.generate_report()
    doc_report.run_report()

    # st_report = st_reportview.StreamlitReportView(report_metadata['report']['id'], 
    #                                              report_metadata['report']['name'], 
    #                                              report=report, 
    #                                              report_type = assert_enum_value(ReportType, report_metadata['report']['report_type'], report.logger),
    #                                              columns=None)
    # st_report.generate_report()
    # st_report.run_report()

