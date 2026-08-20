"""Test that empty folders (subsections with no components) still produce
valid Python files with the required ``import streamlit as st`` statement."""

import logging

from vuegen import report as r
from vuegen.streamlit_reportview import StreamlitReportView


def _make_view() -> StreamlitReportView:
    """Return a minimal StreamlitReportView instance for testing."""
    logger = logging.getLogger("test_empty_folder")
    report = r.Report(title="Test Report", logger=logger)
    return StreamlitReportView(report=report, report_type=r.ReportType.STREAMLIT)


def test_empty_subsection_imports_contain_streamlit():
    """_generate_subsection must include 'import streamlit as st' even when
    the subsection has no components (empty folder scenario)."""
    view = _make_view()

    subsection = r.Subsection(title="Empty Section", components=[])

    _content, imports = view._generate_subsection(subsection)

    assert "import streamlit as st" in imports, (
        "import streamlit as st must be present even for an empty subsection"
    )


def test_empty_subsection_imports_contain_pathlib():
    """Base Path imports should also be present for an empty subsection."""
    view = _make_view()

    subsection = r.Subsection(title="Empty Section", components=[])

    _content, imports = view._generate_subsection(subsection)

    assert "from pathlib import Path" in imports
    assert "section_dir = Path(__file__).resolve().parent.parent" in imports


def test_non_empty_subsection_still_has_streamlit():
    """The fix must not remove streamlit imports when components ARE present."""
    view = _make_view()
    logger = logging.getLogger("test_empty_folder")

    # A markdown component is one of the simpler ones
    md = r.Markdown(
        file_path="test.md",
        title="Test MD",
        logger=logger,
    )
    subsection = r.Subsection(title="Populated Section", components=[md])

    _content, imports = view._generate_subsection(subsection)

    assert "import streamlit as st" in imports
