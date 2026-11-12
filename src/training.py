from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import joblib
import mlflow
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

FEATURE_COLUMNS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
TARGET_COLUMN = "species"
MODEL_NAME = "iris-classifier"


def train_model(df: pd.DataFrame) -> tuple[Pipeline, dict[str, float]]:
    x_train, x_test, y_train, y_test = train_test_split(
        df[FEATURE_COLUMNS],
        df[TARGET_COLUMN],
        test_size=0.2,
        random_state=42,
        stratify=df[TARGET_COLUMN],
    )

    preprocessor = ColumnTransformer(
        transformers=[("num", StandardScaler(), FEATURE_COLUMNS), ("cat", OneHotEncoder(), [])]
    )
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=500, random_state=42)),
        ]
    )
    pipeline.fit(x_train, y_train)

    predictions = pipeline.predict(x_test)
    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "f1_weighted": f1_score(y_test, predictions, average="weighted"),
    }
    return pipeline, metrics


def log_to_mlflow(model: Pipeline, metrics: dict[str, float], model_uri_path: Path) -> None:
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow.mlops.svc.cluster.local:5000")
    experiment_name = os.getenv("MLFLOW_EXPERIMENT_NAME", "iris-training")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run():
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_metric("accuracy", metrics["accuracy"])
        mlflow.log_metric("f1_weighted", metrics["f1_weighted"])
        mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=MODEL_NAME)

        model_uri_path.parent.mkdir(parents=True, exist_ok=True)
        model_uri_path.write_text(json.dumps({"model_name": MODEL_NAME}), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train model and log to MLflow")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--model-output", type=Path, required=True)
    parser.add_argument("--mlflow-info-output", type=Path, default=Path("models/mlflow_model.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input)
    model, metrics = train_model(df)

    args.model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.model_output)
    log_to_mlflow(model, metrics, args.mlflow_info_output)


if __name__ == "__main__":
    main()
