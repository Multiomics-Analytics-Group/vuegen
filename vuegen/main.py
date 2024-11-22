import report_generator
from utils import get_logger, load_yaml_config

if __name__ == '__main__':
    # Load the YAML configuration file with the report metadata
    config_path = "report_metadata_micw2graph.yaml"
    report_metadata = load_yaml_config(config_path)

    # Define logger suffix based on report engine, type and name
    report_engine = "streamlit" 
    report_type = report_metadata['report'].get('report_type')
    report_format = report_metadata['report'].get('report_format')
    report_name = report_metadata['report'].get('name')
    if report_engine == "streamlit": 
        logger_suffix = f"{report_engine}_report_{report_name}"
    else:
        logger_suffix = f"{report_type}_{report_format}_report_{report_name}"

    # Initialize logger
    logger = get_logger(f"{logger_suffix}")

    # Generate the report
    report_generator.get_report(metadata=report_metadata, report_engine=report_engine, logger=logger)

