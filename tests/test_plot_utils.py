"""Tests for plot_utils module."""

import base64
import json
import struct
from pathlib import Path

import pytest

from vuegen.plot_utils import decode_plotly_json

# Path to example JSON files used as fixtures
EXAMPLE_DATA_DIR = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "example_data"
    / "Basic_example_vuegen_demo_notebook"
    / "1_Plots"
    / "1_Interactive_plots"
)


def _make_bdata(values: list, fmt: str) -> str:
    """Encode a list of values to a base64 bdata string."""
    raw = struct.pack(fmt * len(values), *values)
    return base64.b64encode(raw).decode()


class TestDecodeScalarTypes:
    """Test that all supported dtype codes are decoded correctly."""

    @pytest.mark.parametrize(
        "dtype,fmt,values",
        [
            ("i1", "b", [-128, 0, 127]),
            ("i2", "h", [-1000, 0, 1000]),
            ("i4", "i", [-100000, 0, 100000]),
            ("i8", "q", [-10**9, 0, 10**9]),
            ("u1", "B", [0, 128, 255]),
            ("u2", "H", [0, 1000, 65535]),
            ("u4", "I", [0, 100000, 4294967295]),
            ("u8", "Q", [0, 10**9, 10**15]),
            ("f4", "f", [-1.5, 0.0, 1.5]),
            ("f8", "d", [-1.5, 0.0, 1.5]),
        ],
    )
    def test_flat_array(self, dtype, fmt, values):
        obj = {"dtype": dtype, "bdata": _make_bdata(values, fmt)}
        result = decode_plotly_json(obj)
        assert isinstance(result, list)
        assert len(result) == len(values)
        for decoded, expected in zip(result, values):
            assert abs(decoded - expected) < 1e-3


class TestDecodeShape:
    """Test that the 'shape' field reshapes the flat array into nested lists."""

    def test_shape_as_string(self):
        values = list(range(6))
        obj = {
            "dtype": "i4",
            "bdata": _make_bdata(values, "i"),
            "shape": "2, 3",
        }
        result = decode_plotly_json(obj)
        assert result == [[0, 1, 2], [3, 4, 5]]

    def test_shape_as_list(self):
        values = list(range(6))
        obj = {
            "dtype": "i4",
            "bdata": _make_bdata(values, "i"),
            "shape": [2, 3],
        }
        result = decode_plotly_json(obj)
        assert result == [[0, 1, 2], [3, 4, 5]]

    def test_shape_single_dim_not_reshaped(self):
        """A 1-D shape tuple should not trigger 2-D reshaping."""
        values = [1, 2, 3]
        obj = {
            "dtype": "i4",
            "bdata": _make_bdata(values, "i"),
            "shape": [3],
        }
        result = decode_plotly_json(obj)
        assert result == [1, 2, 3]


class TestRecursiveDecode:
    """Test that decode_plotly_json recurses into nested dicts and lists."""

    def test_nested_dict(self):
        values = [10, 20, 30]
        bdata_obj = {"dtype": "i4", "bdata": _make_bdata(values, "i")}
        obj = {"data": [{"x": bdata_obj, "type": "scatter"}], "layout": {}}
        result = decode_plotly_json(obj)
        assert result["data"][0]["x"] == values

    def test_plain_values_untouched(self):
        obj = {"a": 1, "b": [1, 2, 3], "c": "hello"}
        assert decode_plotly_json(obj) == obj


class TestNoPrettyJsonFile:
    """Test that a real Plotly JSON file produced without pretty=True is decoded."""

    def test_load_no_pretty_json(self):
        path = EXAMPLE_DATA_DIR / "7_module_means_heatmap_no_pretty_plotly.json"
        with open(path) as f:
            raw = json.load(f)

        decoded = decode_plotly_json(raw)

        # After decoding, 'y' and 'z' should be plain Python lists
        data_entry = decoded["data"][0]
        assert isinstance(data_entry["y"], list)
        assert isinstance(data_entry["z"], list)
        # y should be a flat list of integers
        assert all(isinstance(v, (int, float)) for v in data_entry["y"])
        # z should be a list of lists (2-D)
        assert isinstance(data_entry["z"][0], list)

    def test_load_with_pretty_json_unchanged(self):
        """A standard pretty-printed JSON should pass through decode unchanged."""
        path = EXAMPLE_DATA_DIR / "8_module_means_heatmap_with_pretty_plotly.json"
        with open(path) as f:
            raw = json.load(f)

        decoded = decode_plotly_json(raw)

        data_entry = decoded["data"][0]
        assert isinstance(data_entry["y"], list)
        assert isinstance(data_entry["z"], list)
