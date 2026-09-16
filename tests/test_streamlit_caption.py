"""Tests for caption rendering of plot components in the Streamlit report view."""

import ast
import logging

import pytest

from vuegen import report as r
from vuegen.streamlit_reportview import StreamlitReportView


@pytest.fixture
def view(tmp_path):
    """Return a StreamlitReportView with an empty report writing to tmp_path."""
    logger = logging.getLogger("test_streamlit_caption")
    report = r.Report(title="Caption test", logger=logger, sections=[])
    return StreamlitReportView(
        report=report,
        report_type=r.ReportType.STREAMLIT,
        static_dir=tmp_path / "static",
        sections_dir=tmp_path / "sections",
    )


def _plot(tmp_path, plot_type, caption, suffix):
    """Create a plot component pointing to a placeholder file."""
    logger = logging.getLogger("test_streamlit_caption")
    plot_file = tmp_path / f"a_plot{suffix}"
    plot_file.write_text("{}")
    return r.Plot(
        title="A plot",
        logger=logger,
        plot_type=plot_type,
        file_path=plot_file.as_posix(),
        caption=caption,
    )


@pytest.mark.parametrize(
    "plot_type,suffix",
    [
        (r.PlotType.STATIC, ".png"),
        (r.PlotType.PLOTLY, ".json"),
        (r.PlotType.ALTAIR, ".json"),
    ],
)
def test_caption_rendered_for_all_plot_types(view, tmp_path, plot_type, suffix):
    """The caption is rendered regardless of the plot type, not only for static."""
    plot = _plot(tmp_path, plot_type, "My caption text.", suffix)

    content = "\n".join(view._generate_plot_content(plot))

    assert "My caption text." in content


def test_no_caption_does_not_render_none(view, tmp_path):
    """A missing caption is not rendered as the literal string 'None'."""
    plot = _plot(tmp_path, r.PlotType.STATIC, None, ".png")

    content = "\n".join(view._generate_plot_content(plot))

    assert "None" not in content
    assert "caption" not in content


def test_caption_with_quotes_yields_valid_python(view, tmp_path):
    """Quote characters in a caption do not break the generated code."""
    plot = _plot(
        tmp_path,
        r.PlotType.STATIC,
        """The model's output isn't "shown" here.""",
        ".png",
    )

    content = "\n".join(view._generate_plot_content(plot))

    # Raises SyntaxError if the caption broke out of its string literal
    ast.parse(content)
    assert "isn't" in content


def test_multiline_caption_yields_valid_python(view, tmp_path):
    """A multi-line caption (as written by folded YAML) stays valid Python."""
    plot = _plot(
        tmp_path,
        r.PlotType.PLOTLY,
        "First line of the caption\nand a second line.",
        ".json",
    )

    content = "\n".join(view._generate_plot_content(plot))

    ast.parse(content)
    assert "and a second line." in content
