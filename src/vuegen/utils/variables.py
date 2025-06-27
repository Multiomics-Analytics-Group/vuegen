"""Create valid variable names for Python identifiers."""

import re


def make_valid_identifier(name: str) -> str:
    """Create a valid Python identifier from a given name.

    Used in streamlit report sections to build structure (pages).
    """
    ret = re.sub(r"[^a-zA-Z0-9]", "_", name)
    if not ret[0].isalpha():
        ret = "_" + ret
    return ret
