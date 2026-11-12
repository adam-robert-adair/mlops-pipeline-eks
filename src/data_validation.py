from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

EXPECTED_SCHEMA = {
    "sepal_length": "float64",
    "sepal_width": "float64",
    "petal_length": "float64",
    "petal_width": "float64",
    "species": "object",
}


def validate_schema(df: pd.DataFrame) -> None:
    missing_columns = [col for col in EXPECTED_SCHEMA if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def validate_nulls(df: pd.DataFrame) -> None:
    if df[list(EXPECTED_SCHEMA.keys())].isnull().any().any():
        raise ValueError("Validation failed: null values found in required columns")


def validate_species_cardinality(df: pd.DataFrame) -> None:
    if df["species"].nunique() < 2:
        raise ValueError("Validation failed: species needs at least two classes")


def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    validate_schema(df)
    validate_nulls(df)
    validate_species_cardinality(df)
    return df.copy()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate training dataset")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input)
    validated = validate_dataframe(df)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    validated.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
