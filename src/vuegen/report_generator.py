import logging

from .config_manager import ConfigManager
from .quarto_reportview import QuartoReportView
from .report import ReportType
from .streamlit_reportview import StreamlitReportView
from .utils import assert_enum_value, load_yaml_config, write_yaml_config


def get_report(report_type: str, logger: logging.Logger, config_path: str = None, dir_path: str = None, streamlit_autorun: bool = False) -> None:
    """
    Generate and run a report based on the specified engine.

    Parameters
    ----------
    report_type : str
        The report type. It should be one of the values of the ReportType Enum.
    logger : logging.Logger
        A logger object to track warnings, errors, and info messages.
    config_path : str, optional
        Path to the YAML configuration file.
    dir_path : str, optional
        Path to the directory from which to generate the configuration file.
    streamlit_autorun : bool, optional
        Whether to automatically run the Streamlit report after generation (default is False).

    Raises
    ------
    ValueError
        If neither 'config_path' nor 'directory' is provided.
    """
    # Initialize the config manager object 
    config_manager = ConfigManager(logger)
    
    if dir_path:
        # Generate configuration from the provided directory
        yaml_data, base_folder_path = config_manager.create_yamlconfig_fromdir(dir_path)
        config_path = write_yaml_config(yaml_data, base_folder_path)

    # Load the YAML configuration file with the report metadata
    report_config = load_yaml_config(config_path)
    
    # Load report object and metadata
    report, report_metadata = config_manager.initialize_report(report_config)

    # Validate and convert the report type to its enum value
    report_type = assert_enum_value(ReportType, report_type, logger)

    # Create and run ReportView object based on its type
    if report_type == ReportType.STREAMLIT:
        st_report = StreamlitReportView(
            report = report,
            report_type = report_type,
            streamlit_autorun = streamlit_autorun
        )
        st_report.generate_report()
        st_report.run_report()

    else:
        quarto_report = QuartoReportView(
            report = report,
            report_type = report_type
        )
        quarto_report.generate_report()
        quarto_report.run_report()
