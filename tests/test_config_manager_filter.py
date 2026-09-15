"""Tests for the exclude_file_types / deduplication logic in ConfigManager."""

import logging
from pathlib import Path

import pytest

from vuegen.config_manager import ConfigManager


@pytest.fixture()
def manager(tmp_path):
    """Return a ConfigManager whose logger does not write to disk."""
    logger = logging.getLogger("test_config_manager")
    logger.setLevel(logging.DEBUG)
    return ConfigManager(logger=logger)


@pytest.fixture()
def manager_exclude_csv(tmp_path):
    logger = logging.getLogger("test_config_manager_exclude")
    logger.setLevel(logging.DEBUG)
    return ConfigManager(logger=logger, exclude_file_types=["csv"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_files(tmp_path: Path, names: list) -> list:
    """Create empty files and return Path objects in the same order."""
    paths = []
    for name in names:
        p = tmp_path / name
        p.touch()
        paths.append(p)
    return paths


# ---------------------------------------------------------------------------
# Extension normalisation
# ---------------------------------------------------------------------------


class TestExcludeNormalisation:
    """The constructor should accept extensions with or without a leading dot."""

    def test_without_dots(self, tmp_path):
        logger = logging.getLogger("norm")
        cm = ConfigManager(logger=logger, exclude_file_types=["csv", "PNG"])
        assert ".csv" in cm.exclude_file_types
        assert ".png" in cm.exclude_file_types

    def test_with_dots(self, tmp_path):
        logger = logging.getLogger("norm_dot")
        cm = ConfigManager(logger=logger, exclude_file_types=[".csv", ".PNG"])
        assert ".csv" in cm.exclude_file_types
        assert ".png" in cm.exclude_file_types

    def test_none_gives_empty_list(self, tmp_path):
        logger = logging.getLogger("norm_none")
        cm = ConfigManager(logger=logger, exclude_file_types=None)
        assert cm.exclude_file_types == []


# ---------------------------------------------------------------------------
# _filter_files_by_type – basic exclusion
# ---------------------------------------------------------------------------


class TestFilterFilesExclusion:
    def test_excludes_specified_extension(self, tmp_path, manager_exclude_csv):
        files = _make_files(tmp_path, ["data.csv", "data.xlsx"])
        result = manager_exclude_csv._filter_files_by_type(files)
        names = [p.name for p in result]
        assert "data.csv" not in names
        assert "data.xlsx" in names

    def test_no_exclusion_keeps_all(self, tmp_path, manager):
        files = _make_files(tmp_path, ["data.csv", "plot.png"])
        result = manager._filter_files_by_type(files)
        assert len(result) == 2

    def test_exclude_multiple_types(self, tmp_path):
        logger = logging.getLogger("multi")
        cm = ConfigManager(logger=logger, exclude_file_types=["csv", "png"])
        files = _make_files(tmp_path, ["data.csv", "plot.png", "report.json"])
        result = cm._filter_files_by_type(files)
        names = [p.name for p in result]
        assert names == ["report.json"]

    def test_directories_are_never_excluded(self, tmp_path, manager_exclude_csv):
        subdir = tmp_path / "section"
        subdir.mkdir()
        csv_file = tmp_path / "data.csv"
        csv_file.touch()
        result = manager_exclude_csv._filter_files_by_type([subdir, csv_file])
        names = [p.name for p in result]
        assert "section" in names
        assert "data.csv" not in names

    def test_order_is_preserved(self, tmp_path, manager_exclude_csv):
        files = _make_files(tmp_path, ["b.xlsx", "a.xlsx", "c.xlsx"])
        result = manager_exclude_csv._filter_files_by_type(files)
        assert [p.name for p in result] == ["b.xlsx", "a.xlsx", "c.xlsx"]


# ---------------------------------------------------------------------------
# _filter_files_by_type – deduplication
# ---------------------------------------------------------------------------


class TestFilterFilesDedup:
    def test_xlsx_preferred_over_csv(self, tmp_path, manager):
        files = _make_files(tmp_path, ["data.csv", "data.xlsx"])
        result = manager._filter_files_by_type(files)
        names = [p.name for p in result]
        assert names == ["data.xlsx"]

    def test_json_preferred_over_png(self, tmp_path, manager):
        files = _make_files(tmp_path, ["plot.json", "plot.png"])
        result = manager._filter_files_by_type(files)
        names = [p.name for p in result]
        assert names == ["plot.json"]

    def test_no_dedup_for_different_stems(self, tmp_path, manager):
        files = _make_files(tmp_path, ["data.csv", "other.xlsx"])
        result = manager._filter_files_by_type(files)
        assert len(result) == 2

    def test_dedup_keeps_single_file_unchanged(self, tmp_path, manager):
        files = _make_files(tmp_path, ["plot.png"])
        result = manager._filter_files_by_type(files)
        assert [p.name for p in result] == ["plot.png"]

    def test_dedup_three_way(self, tmp_path, manager):
        # xlsx > csv > txt  => xlsx wins
        files = _make_files(tmp_path, ["table.csv", "table.xlsx", "table.txt"])
        result = manager._filter_files_by_type(files)
        names = [p.name for p in result]
        assert names == ["table.xlsx"]

    def test_unknown_extension_always_kept(self, tmp_path, manager):
        files = _make_files(tmp_path, ["notes.rst", "notes.csv"])
        # .rst is not in _DEDUP_PRIORITY so both stems differ in priority lookup
        result = manager._filter_files_by_type(files)
        # stems differ ("notes" but different extensions – .rst has no priority so it
        # stays), .csv also stays because it's a different stem_map key check:
        # actually both have stem "notes" but only .csv is in _DEDUP_PRIORITY;
        # .rst goes to non_priority, so result must contain both.
        names = [p.name for p in result]
        assert "notes.rst" in names
        assert "notes.csv" in names

    def test_exclusion_before_dedup(self, tmp_path):
        """If xlsx is excluded but csv is not, csv should be kept (no dedup clash)."""
        logger = logging.getLogger("exc_before_dedup")
        cm = ConfigManager(logger=logger, exclude_file_types=["xlsx"])
        files = _make_files(tmp_path, ["data.csv", "data.xlsx"])
        result = cm._filter_files_by_type(files)
        names = [p.name for p in result]
        assert "data.xlsx" not in names
        assert "data.csv" in names


# ---------------------------------------------------------------------------
# Integration: create_yamlconfig_fromdir respects exclude_file_types
# ---------------------------------------------------------------------------


class TestCreateYamlconfigExclusion:
    def test_excluded_extension_not_in_config(self, tmp_path):
        logger = logging.getLogger("yaml_excl")
        cm = ConfigManager(logger=logger, exclude_file_types=["csv"])

        # Flat directory with one CSV and one XLSX sharing the same stem
        section_dir = tmp_path / "Results"
        section_dir.mkdir()
        (section_dir / "data.csv").touch()
        (section_dir / "data.xlsx").touch()

        yaml_data, _ = cm.create_yamlconfig_fromdir(str(tmp_path))

        # Collect all file_path values from every component in every section
        file_paths = []
        for section in yaml_data.get("sections", []):
            for comp in section.get("components", []):
                file_paths.append(comp.get("file_path", ""))
            for sub in section.get("subsections", []):
                for comp in sub.get("components", []):
                    file_paths.append(comp.get("file_path", ""))

        assert not any(fp.endswith(".csv") for fp in file_paths), (
            "CSV files should have been excluded"
        )
        assert any(fp.endswith(".xlsx") for fp in file_paths), (
            "XLSX file should be present"
        )

    def test_dedup_in_yaml_config(self, tmp_path):
        """Without any exclusion, same-stem xlsx+csv → only xlsx in config."""
        logger = logging.getLogger("yaml_dedup")
        cm = ConfigManager(logger=logger)

        section_dir = tmp_path / "Results"
        section_dir.mkdir()
        (section_dir / "table.csv").touch()
        (section_dir / "table.xlsx").touch()

        yaml_data, _ = cm.create_yamlconfig_fromdir(str(tmp_path))

        file_paths = []
        for section in yaml_data.get("sections", []):
            for comp in section.get("components", []):
                file_paths.append(comp.get("file_path", ""))
            for sub in section.get("subsections", []):
                for comp in sub.get("components", []):
                    file_paths.append(comp.get("file_path", ""))

        assert not any(fp.endswith(".csv") for fp in file_paths), (
            "CSV should have been deduplicated away in favour of XLSX"
        )
        assert any(fp.endswith(".xlsx") for fp in file_paths)
