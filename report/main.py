import report as r
from metadata_manager import YAMLMetadataManager

if __name__ == '__main__':
    # Load report metadata from YAML file
    yaml_manager = YAMLMetadataManager()
    report = yaml_manager.load_report_metadata('./report_metadata.yaml')

    # Create report view
    report_view = r.StreamlitReportView(12312, "Multi-omics project report", report=report, columns=None)
    report_view.generate_report(output_dir="tmp")
    report_view.run_report(output_dir='tmp')