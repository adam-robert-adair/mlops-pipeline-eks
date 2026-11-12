from sklearn.datasets import load_iris

from src.training import train_model


def test_train_model_outputs_metrics_in_range() -> None:
    dataset = load_iris(as_frame=True)
    df = dataset.frame.rename(
        columns={
            "sepal length (cm)": "sepal_length",
            "sepal width (cm)": "sepal_width",
            "petal length (cm)": "petal_length",
            "petal width (cm)": "petal_width",
            "target": "species",
        }
    )
    df["species"] = df["species"].map(dict(enumerate(dataset.target_names)))

    _, metrics = train_model(df)

    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["f1_weighted"] <= 1.0
