from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationResult:
    candidate_metric: float
    production_metric: float | None
    metric_name: str


def improvement_over_production(result: EvaluationResult) -> float:
    if result.production_metric is None:
        return 1.0
    return result.candidate_metric - result.production_metric
