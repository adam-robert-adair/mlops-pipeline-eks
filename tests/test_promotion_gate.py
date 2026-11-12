from pathlib import Path

import pandas as pd

from src.evaluation import EvaluationResult
from src.promotion_gate import evaluate_promotion_gate


def _write_dataset(path: Path) -> None:
    df = pd.DataFrame(
        {
            "sepal_length": [5.1, 4.9, 6.0],
            "sepal_width": [3.5, 3.0, 2.2],
            "petal_length": [1.4, 1.4, 4.0],
            "petal_width": [0.2, 0.2, 1.2],
            "species": ["setosa", "setosa", "versicolor"],
        }
    )
    df.to_csv(path, index=False)


def test_promotes_when_improvement_exceeds_threshold(tmp_path: Path) -> None:
    dataset = tmp_path / "dataset.csv"
    _write_dataset(dataset)

    decision = evaluate_promotion_gate(
        EvaluationResult(candidate_metric=0.95, production_metric=0.93, metric_name="accuracy"),
        min_delta=0.01,
        data_path=dataset,
    )

    assert decision.promote is True


def test_blocks_when_improvement_is_below_threshold(tmp_path: Path) -> None:
    dataset = tmp_path / "dataset.csv"
    _write_dataset(dataset)

    decision = evaluate_promotion_gate(
        EvaluationResult(candidate_metric=0.935, production_metric=0.93, metric_name="accuracy"),
        min_delta=0.01,
        data_path=dataset,
    )

    assert decision.promote is False
