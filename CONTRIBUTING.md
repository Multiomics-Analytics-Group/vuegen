# Contributing to VueGen

[VueGen][vuegen-repo] is an open source project, and we welcome contributions of all 
kinds via **GitHub issues** and **pull requests**: correct or improve our 
[documentation][vuegen-docs], report or fix bugs, propose changes, and implement new 
features. Please follow these guidelines to make sure that your contribution is easily 
integrated into the project.

## Contributor Agreement

By contributing, you agree that we may redistribute your work under [our
license](LICENSE). In exchange, we will address your issues and/or assess
your change proposal as promptly as we can, and help you become a member of our
community.

## What to Contribute?

The easiest way to get started is by **reporting an issue** that needs to be fixed, 
such as a bug in the code, unclear explanations, conceptual errors, or other details.
If you are familiar with Python, Git,, and GitHub, you can **fix the bug** yourself 
and submit a **pull request (PR)** with your changes, as described below. 

You can also contribute by **fixing existing bugs** tagged with the `bug` and 
`help wanted` labels in the [list of open issues][issues] of the repository. There are 
**new features and imporvements** tagged with `enhancement` and `help wanted` as well, so
feel free to start a discussion if you would like to work on one of those. If you come up with 
any **ideas for new features or improvements** that are not yet reported, we are also happy to hear about them. 

Feedback from beginners is especially valuable, as experienced users may overlook how 
challenging certain aspects of the software can be for newcomers. Therefore, we encourage 
you to share any suggestions or observations you have.

## How to Contribute?

Here are the ways you can submit your suggestions and contribute to the project:

### 1. Reporting Issues or Suggesting Improvements

If you have a  [GitHub][github] account (or are willing to [open one][github-join]) but are unfamiliar with 
Git, you can report bugs or suggest improvements by [creating an issue][new-issue]. This GitHub feature allows 
for discussion threads on reported issues and proposed enhancements.

When reporting an issue, please provide as much relevant information as possible, including:

* A clear and descriptive title
* A detailed description of the problem or suggestion
* Steps to reproduce the issue (if applicable)
* Any relevant screenshots or error messages
* Your operating system, software version, and additonal details about your local setup that might be helpful in troubleshooting

> [!TIP]
> This guide from the [GitHub Docs][github-docs] provides useful tips on [how to write an issue][issue-github-guide].

### 2. Submitting Changes via Pull Requests

If you are comfortable using Git/GitHub and would like to add or modify a functionality, you can submit a **PR**. 
You may want to look at [How to Contribute to an Open Source Project on GitHub][how-contribute]. 
In brief, we use [GitHub flow][github-flow] to manage changes:

> [!TIP]
> Consider using an IDE (e.g., [VSCode][vscode]) or a GUI client (e.g., [GitHub Desktop][github-desktop]) to help 
> you with some of the common steps described below.

1. Fork the [vuegen][vuegen-repo] repo on GitHub. 
2. Clone your fork locally. Replace `yourusername` with your GitHub username.

   ```bash
   git clone https://github.com/yourusername/vuegen.git
   ```

3. Install your local copy into a virtual environment. Assuming you have Python available 
   on your system, this can be done using `venv`. Alternatives are `conda`, `uv`, or `poetry` 
   to create and manage virtual environments.

   ```bash
   cd vuegen/
   python -m venv .env
   source .env/bin/activate
   pip install -e .[dev]
   ```

4. Create a new branch in your desktop copy of this repository for each significant change.

   ```bash
   git checkout -b name-of-your-new-branch
   ```

5. When you're done making changes, check that your changes are formatted and pass `black` and
   `ruff` checks (some changes ruff can automatically fix for you, if you pass the `--fix` flag). 
   Also, run the `tests` to make sure everything is working as expected:

   ```bash
   black .
   ruff check src
   pytest .
   ```

6. Commit the changea in that branch.

   ```bash
   git add .
   git commit -m "Your detailed description of your changes."
   ```

7. Push that branch to your fork of this repository on GitHub.

   ```bash
   git push origin name-of-your-new-branch
   ```

8. Submit a pull request from that branch to the [upstream repository][vuegen-repo] via GitHub.
   See the **PR General Guidelines** below for more details.
9. If you receive feedback, make changes on your desktop and push to your branch on GitHub: the 
   pull request will update automatically.

> [!TIP]
> The documentation for [Git][git-docs] and [GitHub][github-docs] are easy to follow, and you can learn the 
> basics using their official guides.

#### PR General Guidelines

We have a general [PR template][general-pr-template] that is loaded autmatically when you open a new PR. 

Before you submit a PR, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring.
3. The pull request should pass the workflows on GitHub.

## Code & Documentation Standards

To maintain consistency across the codebase, please adhere to the following standards when contributing:

* **Docstrings:** Follow the [NumPy docstring style][numpy-docstring-guide]. Include examples where relevant.
* **Type Hints:** Use Python type hints for function signatures and variable annotations (**PEP 484**).
* **Code Formatting:** Use `black` for code formatting and `ruff` for linting (as mentioned in the PR guidelines).
* **Naming Conventions:** Follow **PEP8** for naming (e.g., snake_case for variables/functions, CamelCase for classes).

Here is an example of a simple function with a proper docstring and type hints:

```python
def calculate_average(values: List[float]) -> float:
    """
    Calculate the average of a list of numerical values.

    Parameters
    ----------
    values : List[float]
        List of numerical values to average.

    Returns
    -------
    float
        The arithmetic mean of the input values.

    Examples
    --------
    >>> calculate_average([1.0, 2.0, 3.0, 4.0])
    2.5
    """
    return sum(values) / len(values)
```

## Test Guidelines 

We encourage comprehensive testing to maintain code quality, so all contributions should include 
appropriate tests that verify functionality. We use `pytest` as our testing framework. Here are some considerations:

* **Structure:** Place tests in the tests/ directory, mirroring the source structure.
* **Coverage:** Aim for high test coverage, especially for new features or bug fixes. Try to cover typical use cases as well as edge cases.
* **Naming:** Use descriptive test function names that indicate what is being tested.
* **Docstrings:** Include docstrings in your test functions to explain their purpose, following the previous docstring guidelines.
* **Isolation:** Each test should be independent and not rely on other tests.
* **Local Execution:** Ensure that tests can be run locally using `pytest` before submitting a PR.

Here is an example of a test script for the `calculate_average` function: 

```python
import pytest
from vuegen.utils import calculate_average

def test_calculate_average_basic():
    """Test basic average calculation with positive numbers."""
    result = calculate_average([1.0, 2.0, 3.0, 4.0])
    assert result == 2.5

def test_calculate_average_single_value():
    """Test average calculation with a single value."""
    result = calculate_average([5.0])
    assert result == 5.0

def test_calculate_average_empty_list():
    """Test average calculation with empty list raises appropriate error."""
    with pytest.raises(ZeroDivisionError):
        calculate_average([])
```

Run the following command in the root directory to execute the tests locally:

```bash
pytest .
```

It's possible to run specific test files or functions by providing their paths. 
See the [pytest documentation][pytest-docs] for more details.

## Deployment

We created a [CI/CD worflow][cicd-workflow] using **GitHub Actions** to automatically deploy the Python package to 
[PyP][vuegen-pypi] when a new release is created. To create a new release, make sure all changed are merged into the `main` branch, 
then go to the [Releases section][releases-vuegen] of the GitHub repository and click on **Draft a new release**. Fill in the 
release title and description, then click on **Publish release**. This will trigger the GitHub Actions workflow to build and deploy the package to PyPI.

Also, we have a GitHub Action that automatically deploys the documentation to [Read the Docs][vuegen-docs] in
every push to a branch or when a PR is merged into `main`.

## Credits

This contribution guide was modified under the [Creative Commons Attribution 4.0 International License][ccby] from the [Software Carpentry guides][soft-cp-guides], [vuecore][vuecore-repo], and 
[acore][acore-repo] projects.

[vuegen-repo]: https://github.com/Multiomics-Analytics-Group/vuegen
[vuegen-docs]: https://vuegen.readthedocs.io/
[issues]: https://github.com/Multiomics-Analytics-Group/vuegen/issues
[new-issue]: https://github.com/Multiomics-Analytics-Group/vuegen/issues/new
[github]: https://github.com
[github-join]: https://github.com/join
[git-docs]: https://git-scm.com/doc
[github-docs]: https://guides.github.com/
[issue-github-guide]: https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/quickstart
[how-contribute]: https://egghead.io/courses/how-to-contribute-to-an-open-source-project-on-github
[github-flow]: https://guides.github.com/introduction/flow/
[vscode]: https://code.visualstudio.com/
[github-desktop]: https://github.com/apps/desktop
[general-pr-template]: https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/.github/PULL_REQUEST_TEMPLATE.md
[numpy-docstring-guide]: https://numpydoc.readthedocs.io/en/latest/format.html
[pytest-docs]: https://docs.pytest.org/en/stable
[cicd-workflow]: https://github.com/Multiomics-Analytics-Group/vuecore/blob/main/.github/workflows/cdci.yml
[vuegen-pypi]: https://pypi.org/project/vuegen/
[releases-vuegen]: https://github.com/Multiomics-Analytics-Group/vuegen/releases
[soft-cp-guides]: https://software-carpentry.org/lessons/
[ccby]: https://creativecommons.org/licenses/by/4.0/
[vuecore-repo]: https://github.com/Multiomics-Analytics-Group/vuecore
[acore-repo]: https://github.com/Multiomics-Analytics-Group/acore

