import report_generator
from utils import get_logger, load_yaml_config, get_args

if __name__ == '__main__':
    # Parse command-line arguments
    args = get_args(prog_name="Vuegen")
    config_path = args.config
    report_type = args.report_type
    
    # Load the YAML configuration file with the report metadata
    report_config = load_yaml_config(config_path)

    # Define logger suffix based on report type and name
    report_name = report_config['report'].get('name')
    logger_suffix = f"{report_type}_report_{report_name}"

    # Initialize logger
    logger = get_logger(f"{logger_suffix}")

    # Generate the report
    report_generator.get_report(config = report_config, report_type = report_type, logger = logger)

