from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from scipy.stats import ks_2samp

FEATURE_COLUMNS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


def compute_drift_score(baseline: pd.DataFrame, current: pd.DataFrame) -> float:
    p_values = [ks_2samp(baseline[col], current[col]).pvalue for col in FEATURE_COLUMNS]
    # Lower p-values indicate stronger drift; convert into [0,1] drift score.
    return max(0.0, 1.0 - (sum(p_values) / len(p_values)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check drift and emit retrain signal")
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--threshold", type=float, default=0.2)
    parser.add_argument("--output", type=Path, default=Path("monitoring/drift_result.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    baseline = pd.read_csv(args.baseline)
    current = pd.read_csv(args.current)
    drift_score = compute_drift_score(baseline, current)
    retrain = drift_score >= args.threshold

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps({"drift_score": drift_score, "threshold": args.threshold, "trigger_retrain": retrain}, indent=2),
        encoding="utf-8",
    )
    print(args.output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
