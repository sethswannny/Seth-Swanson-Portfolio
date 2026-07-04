# Buell Market Value Predictor

An end-to-end machine learning project that estimates used motorcycle listing
prices and flags whether a Buell listing looks underpriced, fair, or overpriced.

I built this because I wanted a public project that felt closer to a real pricing
decision than another generic churn or Titanic model. Buell is a good subject:
the brand has current performance bikes, older enthusiast models, and enough
market nuance that price is not just "newer bike equals higher value."

## Project Goal

The model answers one practical question:

> Given a motorcycle listing, what is a reasonable market price, and does the
> asking price look like a strong deal, fair deal, market price, or overpriced?

This project uses synthetic listing-style data. It does not use employer data,
private marketplace data, scraped listings, or official appraisal values.

## What I Built

- A synthetic motorcycle marketplace dataset with 3,000 listings
- A reproducible data generation script
- A model training pipeline comparing three regressors
- Saved model artifacts and metadata
- Evaluation charts and feature importance
- A Streamlit app that turns predictions into deal labels

## Project Structure

```text
buell_market_value/
  app.py
  data/
    raw/
    processed/
  docs/
    data_dictionary.md
    methodology.md
  models/
  reports/
    figures/
  dist/
  src/
    build_one_file_report.py
    generate_synthetic_data.py
    train_model.py
  requirements.txt
```

## Results

| Model | MAE | RMSE | R2 | MAPE |
| --- | ---: | ---: | ---: | ---: |
| Hist Gradient Boosting | 1030.90 | 1668.11 | 0.9775 | 0.1118 |
| Random Forest | 1115.78 | 1899.05 | 0.9709 | 0.1033 |
| Ridge Regression | 2459.76 | 3184.76 | 0.9182 | 0.8978 |

The histogram gradient boosting model had the lowest test-set MAE, so I saved it
as the final model.

## How To Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/generate_synthetic_data.py
python src/train_model.py
python src/build_one_file_report.py
streamlit run app.py
```

## Modeling Notes

The target is `listing_price`. The pipeline compares:

- Ridge regression baseline
- Random forest regression
- Histogram gradient boosting regression

The final model is selected by lowest test-set MAE and saved to:

```text
models/best_price_model.joblib
```

The app converts the model output into a plain-English label:

- `strong deal`: asking price is at least 12% below predicted value
- `fair deal`: asking price is 4-12% below predicted value
- `market price`: asking price is close to predicted value
- `overpriced`: asking price is more than 8% above predicted value

## Deliverables

After running the pipeline, the project produces:

- `data/processed/modeling_dataset.csv`
- `reports/model_metrics.csv`
- `reports/feature_importance.csv`
- `reports/top_deal_examples.csv`
- `reports/figures/actual_vs_predicted.png`
- `reports/figures/residuals.png`
- `reports/figures/feature_importance.png`
- `dist/buell_market_value_one_file.html`
- `models/best_price_model.joblib`
- `models/model_metadata.json`

## Portfolio Summary

Built a Buell-focused motorcycle market value model using synthetic marketplace
data, feature engineering, model comparison, and a Streamlit decision app. The
model estimates fair listing prices and translates predictions into
business-friendly deal labels for buyer or marketplace workflows.

## Limitations

This is intentionally not an appraisal product. The data is synthetic, so the
model is useful for demonstrating workflow, not for claiming real-world price
accuracy. If I extended the project, I would add:

- licensed or manually collected public listing snapshots
- time-based validation so the model does not learn from future market signals
- separate Buell-only and comparable-market models
- richer geography, seasonality, and aftermarket modification features
- a confidence band around each predicted price

## Disclaimer

This is a synthetic data science project for portfolio demonstration. It is not
an official Buell product, appraisal, investment tool, or pricing guarantee.
