import streamlit_reportview as reportview
from metadata_manager import YAMLMetadataManager

if __name__ == '__main__':
    # Load report metadata from YAML file
    yaml_manager = YAMLMetadataManager()
    report_metadata = yaml_manager.load_report_metadata('./report_metadata_micw2graph.yaml')

    # Create report view
    st_report = reportview.StreamlitReportView(12312, "MicW2Graph", report=report_metadata, columns=None)
    st_report.generate_report(output_dir="streamlit_report/sections")
    st_report.run_report(output_dir="streamlit_report/sections")