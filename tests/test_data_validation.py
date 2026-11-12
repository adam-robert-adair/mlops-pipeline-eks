import pandas as pd
import pytest

from src.data_validation import validate_dataframe


def _valid_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sepal_length": [5.1, 4.9, 6.0],
            "sepal_width": [3.5, 3.0, 2.2],
            "petal_length": [1.4, 1.4, 4.0],
            "petal_width": [0.2, 0.2, 1.2],
            "species": ["setosa", "setosa", "versicolor"],
        }
    )


def test_validate_dataframe_accepts_valid_input() -> None:
    df = _valid_df()
    validated = validate_dataframe(df)
    pd.testing.assert_frame_equal(df, validated)


def test_validate_dataframe_rejects_missing_column() -> None:
    df = _valid_df().drop(columns=["species"])
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_dataframe(df)
