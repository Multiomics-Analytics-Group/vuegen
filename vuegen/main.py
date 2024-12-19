from pathlib import Path

from vuegen import report_generator
from vuegen.utils import get_args, get_logger

if __name__ == '__main__':
    # Parse command-line arguments
    args = get_args(prog_name="VueGen")

    # Determine the vuegen arguments
    config_path = args.config
    dir_path = args.directory
    report_type = args.report_type
    streamlit_autorun = args.streamlit_autorun

    # Determine the report name for logger suffix
    if config_path:
        report_name = Path(config_path).stem
    else:
        report_name = Path(dir_path).name

    # Define logger suffix based on report type and name
    logger_suffix = f"{report_type}_report_{str(report_name)}"

    # Initialize logger
    logger = get_logger(f"{logger_suffix}")

    # Generate the report
    report_generator.get_report(report_type = report_type, 
                                logger = logger,
                                config_path = config_path,
                                dir_path = dir_path,
                                streamlit_autorun = streamlit_autorun)