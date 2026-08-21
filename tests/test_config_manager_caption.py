"""Tests for caption-from-markdown-file functionality in ConfigManager."""

import pytest

from vuegen.config_manager import ConfigManager


@pytest.fixture
def config_manager():
    """Return a ConfigManager instance."""
    return ConfigManager()


def test_read_caption_file_exists(tmp_path):
    """Caption content is returned when a companion .md file is present."""
    cm = ConfigManager()
    data_file = tmp_path / "my_plot.png"
    data_file.write_bytes(b"")  # empty placeholder
    caption_file = tmp_path / "my_plot.md"
    caption_file.write_text("This is the caption text.")

    assert cm._read_caption_file(data_file) == "This is the caption text."


def test_read_caption_file_missing(tmp_path):
    """Empty string is returned when no companion .md file exists."""
    cm = ConfigManager()
    data_file = tmp_path / "my_plot.png"
    data_file.write_bytes(b"")

    assert cm._read_caption_file(data_file) == ""


def test_caption_populated_for_csv(tmp_path):
    """Caption is populated from companion .md when building config for a CSV file."""
    cm = ConfigManager()
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("a,b\n1,2\n")
    caption_file = tmp_path / "data.md"
    caption_file.write_text("  Caption for the data table.  ")

    config = cm._create_component_config_fromfile(csv_file)

    assert config is not None
    assert config["caption"] == "Caption for the data table."


def test_caption_populated_for_png(tmp_path):
    """Caption is populated from companion .md for a static image file."""
    cm = ConfigManager()
    png_file = tmp_path / "figure.png"
    png_file.write_bytes(b"\x89PNG\r\n")  # minimal PNG header bytes
    caption_file = tmp_path / "figure.md"
    caption_file.write_text("Figure caption here.")

    config = cm._create_component_config_fromfile(png_file)

    assert config is not None
    assert config["caption"] == "Figure caption here."


def test_caption_empty_when_no_companion_md(tmp_path):
    """Caption is empty string when no companion .md file is present."""
    cm = ConfigManager()
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("a,b\n1,2\n")

    config = cm._create_component_config_fromfile(csv_file)

    assert config is not None
    assert config["caption"] == ""


def test_md_caption_file_skipped_as_component(tmp_path):
    """A .md file that is a caption companion is not added as a MARKDOWN component."""
    cm = ConfigManager()
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("a,b\n1,2\n")
    caption_file = tmp_path / "data.md"
    caption_file.write_text("Caption text.")

    # Processing the .md caption file directly should return None (skip it)
    result = cm._create_component_config_fromfile(caption_file)
    assert result is None


def test_standalone_md_still_creates_markdown_component(tmp_path):
    """A .md file without a sibling data/plot file is still a MARKDOWN component."""
    cm = ConfigManager()
    md_file = tmp_path / "notes.md"
    md_file.write_text("Some notes.")

    config = cm._create_component_config_fromfile(md_file)

    assert config is not None
    assert config["component_type"].lower() == "markdown"


def test_caption_file_excluded_from_subsection_components(tmp_path):
    """A .md caption file is not included as a component in subsection config."""
    cm = ConfigManager()
    # Create a subsection dir with a CSV and its companion .md caption
    subsect_dir = tmp_path / "my_subsection"
    subsect_dir.mkdir()
    csv_file = subsect_dir / "data.csv"
    csv_file.write_text("a,b\n1,2\n")
    caption_file = subsect_dir / "data.md"
    caption_file.write_text("Caption for data.")

    config = cm._create_subsect_config_fromdir(subsect_dir)

    # Only the CSV component should be present, not the .md caption file
    assert len(config["components"]) == 1
    assert config["components"][0]["caption"] == "Caption for data."
    assert config["components"][0]["component_type"].lower() == "dataframe"
