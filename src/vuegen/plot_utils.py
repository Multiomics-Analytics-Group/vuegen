"""Utilities for loading and processing plot data."""

import base64
import struct
from typing import Any


def decode_plotly_json(obj: Any) -> Any:
    """
    Decode Plotly's binary TypedArray format back to Python lists.

    When Plotly generates JSON without pretty-printing (e.g. R's ``plotly_json()``
    with ``pretty = FALSE``), numeric arrays may be serialized as binary TypedArrays
    with the format::

        {"dtype": "f8", "bdata": "<base64 string>", "shape": "10, 8"}

    This function recursively walks through the parsed JSON object and converts
    any such TypedArray dicts back to regular Python lists so that Streamlit's
    ``st.plotly_chart`` can render them correctly.

    Parameters
    ----------
    obj : Any
        The parsed JSON value (dict, list, or scalar) to decode.

    Returns
    -------
    Any
        The decoded value with TypedArray dicts replaced by Python lists.
    """
    # Mapping from Plotly/NumPy dtype codes to (struct format char, byte size)
    dtype_to_struct: dict[str, tuple[str, int]] = {
        "i1": ("b", 1),
        "i2": ("h", 2),
        "i4": ("i", 4),
        "i8": ("q", 8),
        "u1": ("B", 1),
        "u2": ("H", 2),
        "u4": ("I", 4),
        "u8": ("Q", 8),
        "f4": ("f", 4),
        "f8": ("d", 8),
    }

    if isinstance(obj, dict):
        if "bdata" in obj and "dtype" in obj:
            # Decode a binary-encoded TypedArray
            dtype = obj["dtype"]
            fmt_char, item_size = dtype_to_struct.get(dtype, ("B", 1))
            raw = base64.b64decode(obj["bdata"])
            n = len(raw) // item_size
            values: list = list(struct.unpack(fmt_char * n, raw))

            shape = obj.get("shape")
            if shape is not None:
                # Shape may be a comma-separated string (e.g. "10, 8") or a list
                if isinstance(shape, str):
                    dims = [int(d.strip()) for d in shape.split(",")]
                else:
                    dims = [int(d) for d in shape]
                if len(dims) == 2:
                    rows, cols = dims
                    values = [values[i * cols : (i + 1) * cols] for i in range(rows)]

            return values

        # Recurse into regular dict
        return {k: decode_plotly_json(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [decode_plotly_json(item) for item in obj]

    return obj
