# builtin
import setuptools

def get_long_description():
    with open("README.md", "r") as readme_file:
        long_description = readme_file.read()
    return long_description


def get_requirements():
    with open('requirements.txt') as f:
        required = f.read().splitlines()
    return required
    

def create_pip_wheel():
    requirements = get_requirements()
    setuptools.setup(
        name="report_generator",
        version="0.1.0",
        license="MIT",
        description="An open-source Python package for generating reports for Omics datasets",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        author="Multi-omics Network Analytics lab",
        author_email="albsad@dtu.dk",
        url="",
        project_urls={
            "Multi-omics Network Analytics": "",
            "GitHub": "",
            "ReadTheDocs": "",
            "PyPi": "",
            "Scientific paper": "https://www.nature.com/articles/s41587-021-01145-6",
        },
        keywords=["dashboard", "bioinformatics", "multi-omics",],
        classifiers=[
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific :: Bioinformatics",
        ],
        packages=[
            "report",
        ],
        include_package_data=True,
        entry_points={},
        install_requires=requirements,
        python_requires=">=3.9,<4",
    )


if __name__ == "__main__":
    create_pip_wheel()
