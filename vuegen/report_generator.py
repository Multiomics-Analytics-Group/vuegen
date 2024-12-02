from streamlit_reportview import StreamlitReportView
from quarto_reportview import QuartoReportView, ReportFormat
from metadata_manager import MetadataManager
from report import ReportType
from utils import assert_enum_value
from enum import StrEnum, auto
import logging

class ReportEngine(StrEnum):
    STREAMLIT = auto()
    QUARTO = auto()

def get_report(config: dict, report_engine: str, logger: logging.Logger) -> None:
    """
    Generate and run a report based on the specified engine.

    Parameters
    ----------
    config : dict
        The report metadata obtained from a YAML config file.
    report_engine : str
        The engine to use for generating and displaying the report. 
        It should be one of the values of the ReportEngine Enum.
    logger : logging.Logger
        A logger object to track warnings, errors, and info messages.

    Raises
    ------
    ValueError
        If an unsupported report engine, report type, or report format are provided.
    """
    # Validate and convert the report engine to its enum value
    validated_engine = assert_enum_value(ReportEngine, report_engine, logger)

    # Load report object and metadata from the YAML file
    yaml_manager = MetadataManager(logger)
    report, report_metadata = yaml_manager.initialize_report(config)

    # Collect report type from YAML file
    report_type = assert_enum_value(ReportType, report_metadata['report']['report_type'], logger)

    # Create and run ReportView object based on its engine
    if validated_engine == ReportEngine.STREAMLIT:
        st_report = StreamlitReportView(
            report=report,
            report_type=report_type
        )
        st_report.generate_report()
        st_report.run_report()

    elif validated_engine == ReportEngine.QUARTO:
        report_format = assert_enum_value(ReportFormat, report_metadata['report']['report_format'], logger)
        quarto_report = QuartoReportView(
            report=report,
            report_type=report_type,
            report_format=report_format
        )
        quarto_report.generate_report()
        quarto_report.run_report()