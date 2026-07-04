# GitHub Publish Checklist

Use this checklist before making the repo public.

## Keep

- `README.md`
- `requirements.txt`
- `app.py`
- `src/generate_synthetic_data.py`
- `src/train_model.py`
- `docs/data_dictionary.md`
- `docs/methodology.md`
- `reports/project_report.md`
- `reports/model_metrics.csv`
- `reports/feature_importance.csv`
- `reports/top_deal_examples.csv`
- `reports/figures/*.png`
- `models/model_metadata.json`

## Consider Excluding

- `.venv/`
- `__pycache__/`
- `.DS_Store`
- raw secrets or local environment files

The saved model file `models/best_price_model.joblib` is fine to include for a
portfolio demo, but GitHub file size limits can become annoying on larger
projects. If it ever gets too large, keep the training code and remove the model
artifact.

## Suggested Repository Description

Machine learning project that predicts used Buell motorcycle listing prices from
synthetic marketplace data and serves the result in a Streamlit decision app.

## Suggested GitHub Topics

- machine-learning
- scikit-learn
- streamlit
- regression
- portfolio-project
- synthetic-data
- motorcycle-analytics

## Suggested Portfolio Blurb

Built a Buell-focused motorcycle market value model using synthetic marketplace
data, feature engineering, regression modeling, and a Streamlit app. Compared
linear and tree-based models, selected histogram gradient boosting by test-set
MAE, and translated predictions into buyer-friendly deal labels.
