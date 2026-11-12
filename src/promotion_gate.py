from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.data_validation import validate_dataframe
from src.evaluation import EvaluationResult, improvement_over_production


@dataclass(frozen=True)
class PromotionDecision:
    promote: bool
    reason: str


def evaluate_promotion_gate(result: EvaluationResult, min_delta: float, data_path: Path) -> PromotionDecision:
    df = pd.read_csv(data_path)
    validate_dataframe(df)

    improvement = improvement_over_production(result)
    if result.production_metric is None:
        return PromotionDecision(promote=True, reason="No production model exists")

    if improvement >= min_delta:
        return PromotionDecision(promote=True, reason=f"Improved by {improvement:.4f}")

    return PromotionDecision(promote=False, reason=f"Improvement {improvement:.4f} is below threshold {min_delta:.4f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Promotion gate for model registry")
    parser.add_argument("--candidate", type=float, required=True)
    parser.add_argument("--production", type=float, required=False)
    parser.add_argument("--threshold", type=float, default=0.01)
    parser.add_argument("--data", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = EvaluationResult(
        candidate_metric=args.candidate,
        production_metric=args.production,
        metric_name="accuracy",
    )
    decision = evaluate_promotion_gate(result=result, min_delta=args.threshold, data_path=args.data)
    print(f"promote={decision.promote} reason={decision.reason}")


if __name__ == "__main__":
    main()
