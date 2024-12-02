from streamlit_reportview import StreamlitReportView
from quarto_reportview import QuartoReportView
from metadata_manager import MetadataManager
from report import ReportType
from utils import assert_enum_value
import logging

def get_report(config: dict, report_type: str, logger: logging.Logger) -> None:
    """
    Generate and run a report based on the specified engine.

    Parameters
    ----------
    config : dict
        The report metadata obtained from a YAML config file.
    report_type : str
        The report type. It should be one of the values of the ReportType Enum.
    logger : logging.Logger
        A logger object to track warnings, errors, and info messages.

    Raises
    ------
    ValueError
        If an unsupported report engine, report type, or report format are provided.
    """
    # Load report object and metadata from the YAML file
    yaml_manager = MetadataManager(logger)
    report, report_metadata = yaml_manager.initialize_report(config)

    # Validate and convert the report type to its enum value
    report_type = assert_enum_value(ReportType, report_type, logger)

    # Create and run ReportView object based on its type
    if report_type == ReportType.STREAMLIT:
        st_report = StreamlitReportView(
            report=report,
            report_type=report_type
        )
        st_report.generate_report()
        st_report.run_report()

    else:
        quarto_report = QuartoReportView(
            report=report,
            report_type=report_type
        )
        quarto_report.generate_report()
        quarto_report.run_report()