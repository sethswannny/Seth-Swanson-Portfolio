"""Train and evaluate a synthetic REIT portfolio health classifier."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "modeling_dataset.csv"
MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "reports"
FIGURE_DIR = REPORT_DIR / "figures"

TARGET = "portfolio_health"
DROP_COLUMNS = ["asset_id", "portfolio_health", "synthetic_risk_score"]
CLASS_ORDER = ["healthy", "watchlist", "at risk"]


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
    return {
        "model": name,
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "balanced_accuracy": round(float(balanced_accuracy_score(y_test, predictions)), 4),
        "macro_f1": round(float(f1_score(y_test, predictions, average="macro")), 4),
        "weighted_f1": round(float(f1_score(y_test, predictions, average="weighted")), 4),
    }


def save_confusion_matrix(y_test: pd.Series, predictions: pd.Series, model_name: str) -> None:
    matrix = confusion_matrix(y_test, predictions, labels=CLASS_ORDER)
    matrix_df = pd.DataFrame(matrix, index=CLASS_ORDER, columns=CLASS_ORDER)
    matrix_df.to_csv(REPORT_DIR / "confusion_matrix.csv")
    plt.figure(figsize=(7, 5.8))
    sns.heatmap(matrix_df, annot=True, fmt="d", cmap="YlGnBu", cbar=False)
    plt.title(f"Confusion Matrix - {model_name}")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "confusion_matrix.png", dpi=180)
    plt.close()


def save_feature_importance(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> pd.DataFrame:
    result = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=8,
        random_state=42,
        scoring="f1_macro",
    )
    importance = pd.DataFrame({
        "feature": X_test.columns,
        "importance": result.importances_mean,
        "std": result.importances_std,
    }).sort_values("importance", ascending=False)
    importance.to_csv(REPORT_DIR / "feature_importance.csv", index=False)

    top = importance.head(12).sort_values("importance")
    plt.figure(figsize=(8, 6))
    plt.barh(top["feature"], top["importance"], color="#0b6b68")
    plt.title("Top Drivers of Portfolio Health Classification")
    plt.xlabel("Permutation importance")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "feature_importance.png", dpi=180)
    plt.close()
    return importance


def save_distribution_charts(data: pd.DataFrame) -> None:
    plt.figure(figsize=(7.5, 5))
    sns.countplot(data=data, x=TARGET, order=CLASS_ORDER, color="#8ecae6")
    plt.title("Synthetic Portfolio Health Distribution")
    plt.xlabel("Portfolio health")
    plt.ylabel("Asset count")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "health_distribution.png", dpi=180)
    plt.close()

    exposure = data.groupby(["property_type", TARGET])["property_value"].sum().reset_index()
    pivot = exposure.pivot(index="property_type", columns=TARGET, values="property_value").fillna(0)
    pivot = pivot.reindex(columns=CLASS_ORDER)
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=True).index]
    pivot.plot(kind="barh", stacked=True, figsize=(10, 6), color=["#0b6b68", "#d5a93f", "#d86446"])
    plt.title("Portfolio Value Exposure by Property Type and Health")
    plt.xlabel("Synthetic property value")
    plt.ylabel("Property type")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "exposure_by_property_type.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8, 5.5))
    sns.boxplot(data=data, x=TARGET, y="rent_coverage_ratio", order=CLASS_ORDER, color="#f0b38e")
    plt.title("Rent Coverage by Portfolio Health")
    plt.xlabel("Portfolio health")
    plt.ylabel("Rent coverage ratio")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "coverage_by_health.png", dpi=180)
    plt.close()


def create_scored_watchlist(data: pd.DataFrame, model: Pipeline, X_columns: list[str]) -> pd.DataFrame:
    scored = data.copy()
    probabilities = model.predict_proba(scored[X_columns])
    class_labels = list(model.classes_)
    for label in class_labels:
        scored[f"prob_{label.replace(' ', '_')}"] = probabilities[:, class_labels.index(label)]
    scored["predicted_health"] = model.predict(scored[X_columns])
    scored = scored.sort_values(["prob_at_risk", "synthetic_risk_score"], ascending=False)
    columns = [
        "asset_id",
        "property_type",
        "region",
        "credit_tier",
        "annual_rent",
        "property_value",
        "lease_term_remaining",
        "rent_coverage_ratio",
        "delinquency_days",
        "sales_trend_12m",
        "synthetic_risk_score",
        "predicted_health",
        "prob_at_risk",
    ]
    output = scored[columns].head(30)
    output.to_csv(REPORT_DIR / "top_watchlist_assets.csv", index=False)
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
        test_size=0.24,
        random_state=42,
        stratify=y,
    )

    preprocessor = build_preprocessor(X_train)
    candidates = {
        "logistic_regression": LogisticRegression(max_iter=1200, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=420,
            min_samples_leaf=5,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
        "hist_gradient_boosting": HistGradientBoostingClassifier(
            learning_rate=0.065,
            max_iter=360,
            min_samples_leaf=20,
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

    metrics_df = pd.DataFrame(metrics).sort_values("macro_f1", ascending=False)
    metrics_df.to_csv(REPORT_DIR / "model_metrics.csv", index=False)
    best_model_name = str(metrics_df.iloc[0]["model"])
    best_model = fitted_models[best_model_name]
    predictions = best_model.predict(X_test)

    report = classification_report(y_test, predictions, labels=CLASS_ORDER, output_dict=True, zero_division=0)
    pd.DataFrame(report).transpose().to_csv(REPORT_DIR / "classification_report.csv")
    save_confusion_matrix(y_test, predictions, best_model_name)
    save_distribution_charts(data)
    save_feature_importance(best_model, X_test, y_test)
    create_scored_watchlist(data, best_model, X.columns.tolist())

    joblib.dump(best_model, MODEL_DIR / "best_health_classifier.joblib")
    with open(MODEL_DIR / "model_metadata.json", "w", encoding="utf-8") as file:
        json.dump(
            {
                "best_model": best_model_name,
                "target": TARGET,
                "rows": int(len(data)),
                "class_order": CLASS_ORDER,
                "features": X.columns.tolist(),
                "metrics": metrics_df.to_dict(orient="records"),
            },
            file,
            indent=2,
        )

    print("Model training complete")
    print(metrics_df.to_string(index=False))
    print(f"Best model: {best_model_name}")
    print(f"Saved model to {MODEL_DIR / 'best_health_classifier.joblib'}")


if __name__ == "__main__":
    main()
