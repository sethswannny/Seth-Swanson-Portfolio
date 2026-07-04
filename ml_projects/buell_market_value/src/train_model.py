"""Train and evaluate a Buell-focused motorcycle market value model."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "modeling_dataset.csv"
MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "reports"
FIGURE_DIR = REPORT_DIR / "figures"

TARGET = "listing_price"
DROP_COLUMNS = [
    "listing_id",
    "listing_price",
    "synthetic_fair_market_value",
    "deal_delta_pct",
    "deal_quality",
]


def mape(y_true: pd.Series, y_pred: np.ndarray) -> float:
    return float(np.mean(np.abs((y_true - y_pred) / y_true)))


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    categorical_features = X.select_dtypes(include=["object", "string"]).columns.tolist()
    numeric_features = [column for column in X.columns if column not in categorical_features]

    return ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
            ("numeric", StandardScaler(), numeric_features),
        ],
        remainder="drop",
    )


def evaluate_model(name: str, pipeline: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    predictions = pipeline.predict(X_test)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    return {
        "model": name,
        "mae": round(float(mean_absolute_error(y_test, predictions)), 2),
        "rmse": round(float(rmse), 2),
        "r2": round(float(r2_score(y_test, predictions)), 4),
        "mape": round(mape(y_test, predictions), 4),
    }


def save_actual_vs_predicted(y_test: pd.Series, predictions: np.ndarray) -> None:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=y_test, y=predictions, alpha=0.55, edgecolor=None)
    lower = min(y_test.min(), predictions.min())
    upper = max(y_test.max(), predictions.max())
    plt.plot([lower, upper], [lower, upper], color="#0f766e", linewidth=2)
    plt.title("Actual vs. Predicted Listing Price")
    plt.xlabel("Actual price")
    plt.ylabel("Predicted price")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "actual_vs_predicted.png", dpi=180)
    plt.close()


def save_residual_plot(y_test: pd.Series, predictions: np.ndarray) -> None:
    residuals = y_test - predictions
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=predictions, y=residuals, alpha=0.55, edgecolor=None)
    plt.axhline(0, color="#0f766e", linewidth=2)
    plt.title("Residuals by Predicted Listing Price")
    plt.xlabel("Predicted price")
    plt.ylabel("Residual")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "residuals.png", dpi=180)
    plt.close()


def save_price_by_model(data: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    order = data.groupby("model")[TARGET].median().sort_values(ascending=False).index
    sns.boxplot(data=data, x=TARGET, y="model", order=order, color="#8ecae6")
    plt.title("Synthetic Listing Price Distribution by Model")
    plt.xlabel("Listing price")
    plt.ylabel("Model")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "price_by_model.png", dpi=180)
    plt.close()


def save_feature_importance(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> pd.DataFrame:
    result = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=8,
        random_state=42,
        scoring="neg_mean_absolute_error",
    )
    importance = pd.DataFrame({
        "feature": X_test.columns,
        "importance": result.importances_mean,
        "std": result.importances_std,
    }).sort_values("importance", ascending=False)

    importance.to_csv(REPORT_DIR / "feature_importance.csv", index=False)

    top = importance.head(12).sort_values("importance")
    plt.figure(figsize=(8, 6))
    plt.barh(top["feature"], top["importance"], color="#0f766e")
    plt.title("Top Drivers of Predicted Listing Price")
    plt.xlabel("Permutation importance")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "feature_importance.png", dpi=180)
    plt.close()

    return importance


def create_scored_examples(data: pd.DataFrame, model: Pipeline, X_columns: list[str]) -> pd.DataFrame:
    scored = data.copy()
    scored["predicted_price"] = model.predict(scored[X_columns])
    scored["predicted_delta_pct"] = (scored["listing_price"] - scored["predicted_price"]) / scored["predicted_price"]
    scored["model_deal_flag"] = np.select(
        [
            scored["predicted_delta_pct"] <= -0.12,
            scored["predicted_delta_pct"] <= -0.04,
            scored["predicted_delta_pct"] <= 0.08,
        ],
        ["strong deal", "fair deal", "market price"],
        default="overpriced",
    )
    scored = scored.sort_values("predicted_delta_pct")
    cols = [
        "make",
        "model",
        "year",
        "mileage",
        "condition",
        "region",
        "listing_price",
        "predicted_price",
        "predicted_delta_pct",
        "model_deal_flag",
    ]
    output = scored[cols].head(25)
    output.to_csv(REPORT_DIR / "top_deal_examples.csv", index=False)
    return output


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(DATA_PATH)
    X = data.drop(columns=DROP_COLUMNS)
    y = data[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.22,
        random_state=42,
        stratify=data["make"],
    )

    preprocessor = build_preprocessor(X_train)
    candidates = {
        "ridge_regression": Ridge(alpha=1.0),
        "random_forest": RandomForestRegressor(
            n_estimators=350,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1,
        ),
        "hist_gradient_boosting": HistGradientBoostingRegressor(
            learning_rate=0.065,
            max_iter=350,
            min_samples_leaf=18,
            random_state=42,
        ),
    }

    metrics = []
    fitted_models = {}
    for name, estimator in candidates.items():
        pipeline = Pipeline([
            ("preprocess", preprocessor),
            ("model", estimator),
        ])
        pipeline.fit(X_train, y_train)
        fitted_models[name] = pipeline
        metrics.append(evaluate_model(name, pipeline, X_test, y_test))

    metrics_df = pd.DataFrame(metrics).sort_values("mae")
    metrics_df.to_csv(REPORT_DIR / "model_metrics.csv", index=False)
    best_model_name = str(metrics_df.iloc[0]["model"])
    best_model = fitted_models[best_model_name]
    predictions = best_model.predict(X_test)

    joblib.dump(best_model, MODEL_DIR / "best_price_model.joblib")
    with open(MODEL_DIR / "model_metadata.json", "w", encoding="utf-8") as file:
        json.dump(
            {
                "best_model": best_model_name,
                "target": TARGET,
                "rows": int(len(data)),
                "features": X.columns.tolist(),
                "metrics": metrics_df.to_dict(orient="records"),
            },
            file,
            indent=2,
        )

    save_actual_vs_predicted(y_test, predictions)
    save_residual_plot(y_test, predictions)
    save_price_by_model(data)
    save_feature_importance(best_model, X_test, y_test)
    create_scored_examples(data, best_model, X.columns.tolist())

    print("Model training complete")
    print(metrics_df.to_string(index=False))
    print(f"Best model: {best_model_name}")
    print(f"Saved model to {MODEL_DIR / 'best_price_model.joblib'}")


if __name__ == "__main__":
    main()
