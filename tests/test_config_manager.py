from vuegen.config_manager import ConfigManager


def test_create_title_fromdir_keeps_dots_in_folder_names():
    cm = ConfigManager()
    # Folder names have no extension, so nothing after a dot may be stripped
    # A dot within the name is kept, it can be part of the name (abbreviation)
    assert cm._create_title_fromdir("Test._Species", is_dir=True) == "Test. Species"
    assert cm._create_title_fromdir("1._Species", is_dir=True) == "Species"
    assert cm._create_title_fromdir("v1.2_results", is_dir=True) == "V1.2 Results"
    # File names still lose their extension
    assert cm._create_title_fromdir("1_my_table.csv") == "My Table"


def test_create_yamlconfig_fromdir_keeps_dots_in_folder_names(tmp_path):
    base_dir = tmp_path / "My.Report"
    section_dir = base_dir / "1._Test._Species"
    subsection_dir = section_dir / "2._Sub.Section"
    subsection_dir.mkdir(parents=True)
    (subsection_dir / "1_my_table.csv").write_text("a,b\n1,2\n")

    config, _ = ConfigManager().create_yamlconfig_fromdir(str(base_dir))

    assert config["report"]["title"] == "My.Report"
    (section,) = config["sections"]
    assert section["title"] == "Test. Species"
    (subsection,) = section["subsections"]
    assert subsection["title"] == "Sub.Section"
    assert [c["title"] for c in subsection["components"]] == ["My Table"]
