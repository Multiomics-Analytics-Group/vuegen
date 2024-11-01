import streamlit_reportview as st_reportview
import quarto_reportview as doc_reportview
from metadata_manager import MetadataManager
from report import ReportType

if __name__ == '__main__':
    # Load report metadata from YAML file
    yaml_manager = MetadataManager()
    report_metadata = yaml_manager.load_report_metadata('./report_metadata_micw2graph.yaml')

    # Create report view
    doc_report = doc_reportview.QuartoReportView(12312, "MicW2Graph", report=report_metadata, 
                                                report_type = ReportType.DOCUMENT, report_formats = [doc_reportview.ReportFormat.HTML, doc_reportview.ReportFormat.PDF], columns=None)
    doc_report.generate_report(output_dir="quarto_report/")
    doc_report.run_report(output_dir="quarto_report/")

    #st_report = st_reportview.StreamlitReportView(12312, "MicW2Graph", report=report_metadata, 
    #                                              report_type = ReportType.STREAMLIT, columns=None)
    #st_report.generate_report(output_dir="streamlit_report/sections")
    #st_report.run_report(output_dir="streamlit_report/sections")