from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

IRIS_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"


def fetch_iris_dataset(output_path: Path) -> Path:
    df = pd.read_csv(IRIS_URL)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch public Iris dataset")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    fetch_iris_dataset(args.output)


if __name__ == "__main__":
    main()
