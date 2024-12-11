import report_generator
from pathlib import Path
from utils import get_logger, get_args

if __name__ == '__main__':
    # Parse command-line arguments
    args = get_args(prog_name="VueGen")

    # Determine the configuration file path or directory
    config_path = args.config
    dir_path = args.directory

    # Report type
    report_type = args.report_type

    # Determine the report name for logger suffix
    if config_path:
        report_name = Path(config_path).stem
    else:
        report_name = Path(dir_path).name

    # Define logger suffix based on report type and name
    logger_suffix = f"{report_type}_report_{report_name}"

    # Initialize logger
    logger = get_logger(f"{logger_suffix}")

    # Generate the report
    report_generator.get_report(config_path = config_path,
                                dir_path = dir_path,
                                report_type = report_type, 
                                logger = logger)

