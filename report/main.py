import streamlit_reportview as st_reportview
import document_reportview as doc_reportview
from metadata_manager import YAMLMetadataManager

if __name__ == '__main__':
    # Load report metadata from YAML file
    yaml_manager = YAMLMetadataManager()
    report_metadata = yaml_manager.load_report_metadata('./report_metadata_micw2graph.yaml')

    # Create report view
    doc_report = doc_reportview.DocumentReportView(12312, "MicW2Graph", report=report_metadata, columns=None, output_format="html")
    doc_report.generate_report(output_dir="document_report/")
    doc_report.run_report(output_dir="document_report/")

    st_report = st_reportview.StreamlitReportView(12312, "MicW2Graph", report=report_metadata, columns=None)
    st_report.generate_report(output_dir="streamlit_report/sections")
    st_report.run_report(output_dir="streamlit_report/sections")