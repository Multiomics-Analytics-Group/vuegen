"""Reading tabular data using pandas."""

import pandas as pd

from . import report as r

# Mapping of file extensions to read functions
read_function_mapping = {
    r.DataFrameFormat.CSV.value_with_dot: pd.read_csv,
    r.DataFrameFormat.PARQUET.value_with_dot: pd.read_parquet,
    r.DataFrameFormat.TXT.value_with_dot: pd.read_table,
    r.DataFrameFormat.XLS.value_with_dot: pd.read_excel,
    r.DataFrameFormat.XLSX.value_with_dot: pd.read_excel,
}


def get_sheet_names(
    file_path: str,
) -> list[str]:
    """Get the sheet names of an Excel file.

    Parameters
    ----------
    file_path : str
        Path to the Excel file.

    Returns
    -------
    list[str]
        List of sheet names.
    """
    return pd.ExcelFile(file_path).sheet_names
