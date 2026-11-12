from __future__ import annotations

import os
from typing import Any

import mlflow.pyfunc
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
from prometheus_client import Counter, generate_latest
from starlette.responses import Response

PREDICTION_COUNTER = Counter("model_prediction_requests_total", "Total prediction requests")

app = FastAPI(title="mlops-pipeline-eks inference service")


class PredictionRequest(BaseModel):
    sepal_length: float = Field(..., ge=0)
    sepal_width: float = Field(..., ge=0)
    petal_length: float = Field(..., ge=0)
    petal_width: float = Field(..., ge=0)


def _load_model() -> Any:
    model_uri = os.getenv("MODEL_URI", "models:/iris-classifier/Production")
    return mlflow.pyfunc.load_model(model_uri)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type="text/plain; version=0.0.4")


@app.post("/predict")
def predict(payload: PredictionRequest) -> dict[str, Any]:
    model = _load_model()
    features = pd.DataFrame([payload.model_dump()])
    prediction = model.predict(features)
    PREDICTION_COUNTER.inc()
    return {"prediction": prediction[0]}
