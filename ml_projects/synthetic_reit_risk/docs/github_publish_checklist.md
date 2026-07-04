# GitHub Publish Checklist

Use this checklist before publishing the project as a standalone repo.

## Keep

- `README.md`
- `requirements.txt`
- `app.py`
- `src/generate_synthetic_data.py`
- `src/train_model.py`
- `src/build_one_file_report.py`
- `docs/data_dictionary.md`
- `docs/methodology.md`
- `reports/project_report.md`
- `reports/model_metrics.csv`
- `reports/classification_report.csv`
- `reports/confusion_matrix.csv`
- `reports/feature_importance.csv`
- `reports/top_watchlist_assets.csv`
- `reports/figures/*.png`
- `dist/reit_risk_one_file.html`
- `models/model_metadata.json`

## Exclude

- `.venv/`
- `__pycache__/`
- `.DS_Store`
- secrets or local environment files

## Suggested Repository Name

`synthetic-reit-risk-classifier`

## Suggested Repository Description

Portfolio-safe machine learning project that classifies synthetic REIT assets as
healthy, watchlist, or at risk using tenant, lease, financial, and market
signals.

## Suggested Topics

- machine-learning
- scikit-learn
- streamlit
- classification
- real-estate-analytics
- portfolio-risk
- synthetic-data

