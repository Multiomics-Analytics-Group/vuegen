"""Main API entry point for generating reports using VueGen."""

import logging
import shutil
import sys
from pathlib import Path

from .config_manager import ConfigManager
from .quarto_reportview import QuartoReportView
from .report import ReportType
from .streamlit_reportview import StreamlitReportView
from .utils import assert_enum_value, get_logger, load_yaml_config, write_yaml_config


def get_report(
    report_type: str,
    logger: logging.Logger = None,
    config_path: str = None,
    dir_path: str = None,
    streamlit_autorun: bool = False,
    quarto_checks: bool = False,
    output_dir: Path = None,
    max_depth: int = 2,  # section and subsection folders
) -> tuple[str, str]:
    """
    Generate and run a report based on the specified engine.

    Parameters
    ----------
    report_type : str
        The report type. It should be one of the values of the ReportType Enum.
    logger : logging.Logger, optional
        A logger object to track warnings, errors, and info messages. If not provided,
        a default logger will be created.
    config_path : str, optional
        Path to the YAML configuration file.
    dir_path : str, optional
        Path to the directory from which to generate the configuration file.
    streamlit_autorun : bool, optional
        Whether to automatically run the Streamlit report after generation
        (default is False).
    quarto_checks : bool, optional
        Whether to perform checks for Quarto report generation for TeX and Chromium
        installation (default is False).
    output_dir : Path, optional
        The directory where the report folder will be generated.
        If not provided, the current directory will be used.
    max_depth : int, optional
        The maximum depth of the directory structure to consider when generating the
        report. The default is 2, which means it will include sections and subsections.
        The parater is only used when 'dir_path' is used.

    Raises
    ------
    ValueError
        If neither 'config_path' nor 'directory' is provided.

    Returns
    -------
    tuple[str, str]
        The path to the generated report and the path to the configuration file.
    """
    if output_dir is None:
        output_dir = Path(".")
    else:
        output_dir = Path(output_dir)
        if output_dir.is_file():
            raise ValueError(
                "The output_dir parameter should be a directory, not a file."
            )
        if not output_dir.exists():
            logger.info("Creating output directory: %s", output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize logger only if it's not provided
    if logger is None:
        _folder = "logs"
        if output_dir:
            _folder = output_dir / _folder
        logger, _ = get_logger("report", folder=_folder)

    # Create the config manager object
    config_manager = ConfigManager(logger, max_depth=max_depth)

    if dir_path:
        # Generate configuration from the provided directory
        yaml_data, _ = config_manager.create_yamlconfig_fromdir(dir_path)
        # yaml_data has under report a title created based on the directory name
        config_path = write_yaml_config(yaml_data, output_dir)
        logger.info("Configuration file generated at %s", config_path)

    # Load the YAML configuration file with the report metadata
    report_config = load_yaml_config(config_path)

    # Load report object and metadata
    report, _ = config_manager.initialize_report(report_config)

    # Validate and convert the report type to its enum value
    report_type = assert_enum_value(ReportType, report_type, logger)

    # Create and run ReportView object based on its type
    if report_type == ReportType.STREAMLIT:
        report_dir = output_dir / "streamlit_report"
        sections_dir = report_dir / "sections"
        static_files_dir = report_dir / "static"
        st_report = StreamlitReportView(
            report=report,
            report_type=report_type,
            streamlit_autorun=streamlit_autorun,
            static_dir=static_files_dir,
            sections_dir=sections_dir,
        )
        st_report.generate_report()
        st_report.run_report()
    else:
        # Check if Quarto is installed
        if shutil.which("quarto") is None and not hasattr(
            sys, "_MEIPASS"
        ):  # ? and not getattr(sys, "frozen", False)
            msg = (
                "Quarto is not installed. Please install Quarto before generating this "
                "report type."
            )
            logger.error(msg)
            raise RuntimeError(msg)
        report_dir = output_dir / "quarto_report"
        static_files_dir = report_dir / "static"
        quarto_report = QuartoReportView(
            report=report,
            report_type=report_type,
            quarto_checks=quarto_checks,
            output_dir=report_dir,
            static_dir=static_files_dir,
        )
        quarto_report.generate_report()
        quarto_report.run_report()
    # ? Could be also the path to the report file for quarto based reports
    return report_dir, config_path
