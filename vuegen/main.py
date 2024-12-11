from vuegen import report_generator
from vuegen.utils import get_args, get_logger, load_yaml_config

if __name__ == '__main__':
    # Parse command-line arguments
    args = get_args(prog_name="VueGen")
    config_path = args.config
    report_type = args.report_type
    
    # Load the YAML configuration file with the report metadata
    report_config = load_yaml_config(config_path)

    # Define logger suffix based on report type and name
    report_title = report_config['report'].get('title')
    logger_suffix = f"{report_type}_report_{report_title}"

    # Initialize logger
    logger = get_logger(f"{logger_suffix}")

    # Generate the report
    report_generator.get_report(config = report_config, report_type = report_type, logger = logger)

