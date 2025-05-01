import re
from pathlib import Path

# Mapping section titles to their corresponding filenames
SECTION_MAPPING = {
    "![VueGen Logo](https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuegen/main/docs/images/vuegen_logo.svg)": "home_page.md",
    "About the project": "about.md",
    "Installation": "installation.md",
    "Execution": "execution.md",
    "GUI": "gui.md",
    "Case studies": "case_studies.md",
    "Web application deployment": "web_app_deploy.md",
    "Citation": "citation.md",
    "Credits and acknowledgements": "credits.md",
}


def extract_section(readme, section_title):
    """Extracts content between current section and next ## heading"""
    pattern = rf"## {re.escape(section_title)}(.*?)(?=\n## |\Z)"
    match = re.search(pattern, readme, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_links_from_readme(readme):
    """Extract link references from README.md into a dictionary"""
    link_pattern = r"\[([^\]]+)\]: (\S+)"
    links = {}

    matches = re.findall(link_pattern, readme)
    for ref, url in matches:
        links[ref] = url

    return links


def convert_gfm_to_sphinx(content, links):
    """Convert GitHub Flavored Markdown to Sphinx-style syntax."""
    # Convert GFM admonitions (like > [!IMPORTANT] and > [!NOTE])
    content = re.sub(
        r"(^|\n)> \[!(\w+)\]([^\n]*)((?:\n> [^\n]*)*)",
        lambda m: f"\n:::{{{m.group(2)}}}\n"  # Note the curly braces here
        + re.sub(r"^> ", "", m.group(4), flags=re.MULTILINE).strip()
        + "\n:::\n",
        content,
    )

    # Replace link references dynamically using the links dictionary
    for ref, url in links.items():
        content = re.sub(rf"\[{re.escape(ref)}\]", f"({url})", content)

    return content


def decrease_header_levels(content):
    """Decrease each Markdown header by one level."""
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if re.match(r"^(#{2,6})\s", line):
            num_hashes = len(line.split()[0])
            new_line = "#" * (num_hashes - 1) + line[num_hashes:]
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    return "\n".join(new_lines)


def process_readme(readme_path, output_dir):
    readme = Path(readme_path).read_text()

    # Extract links from README
    links = extract_links_from_readme(readme)

    # Create output directory
    output_dir.mkdir(exist_ok=True, parents=True)

    for section_title, filename in SECTION_MAPPING.items():
        content = extract_section(readme, section_title)
        if content:
            myst_content = (
                f"## {section_title}\n\n{convert_gfm_to_sphinx(content, links)}"
            )
            myst_content = decrease_header_levels(myst_content)
            (output_dir / filename).write_text(myst_content)
            print(f"Generated {filename}")
        else:
            print(f"Warning: Section '{section_title}' not found in README")


if __name__ == "__main__":
    default_readme = Path(__file__).resolve().parent.parent / "README.md"
    output_sections_readme = Path("./sections_readme")
    process_readme(default_readme, output_sections_readme)
