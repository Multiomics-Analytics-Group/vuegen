import pytest

from vuegen.utils.variables import make_valid_identifier

test_cases = [
    ("a.non valid name", "a_non_valid_name"),
    ("1.non valid name", "_1_non_valid_name"),
    ("a_valid_name", "a_valid_name"),
    ("test", "test"),
]


@pytest.mark.parametrize("var_name,expected", test_cases)
def test_make_valid_identifier(var_name, expected):
    """Test the make_valid_identifier function."""
    assert make_valid_identifier(var_name) == expected
