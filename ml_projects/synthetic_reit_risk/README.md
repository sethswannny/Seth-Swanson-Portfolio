# Synthetic REIT Portfolio Risk Model

A portfolio-safe machine learning project that classifies synthetic REIT assets
as `healthy`, `watchlist`, or `at risk`.

I built this as a public version of the kind of portfolio health question that
comes up in real estate analytics: which assets need attention, which are stable,
and what signals explain that decision?

No employer data, schemas, tenant names, dashboards, or confidential business
rules are used.

## What I Built

- A synthetic diversified REIT portfolio with 5,200 asset records
- A reproducible data generation script
- A classification pipeline comparing three models
- Confusion matrix, classification report, feature importance, and exposure charts
- A Streamlit app for scoring individual assets
- A one-file HTML report that opens without a server

## Project Structure

```text
synthetic_reit_risk/
  app.py
  data/
    raw/
    processed/
  dist/
  docs/
  models/
  reports/
    figures/
  src/
    build_one_file_report.py
    generate_synthetic_data.py
    train_model.py
  requirements.txt
```

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

The target is `portfolio_health`.

Models compared:

- Logistic regression baseline
- Random forest classifier
- Histogram gradient boosting classifier

The final model is selected by macro F1 so the model is not rewarded for only
performing well on the largest class.

## Portfolio Summary

Built a synthetic REIT portfolio risk classifier using financial, lease, tenant,
and market indicators. Compared baseline and tree-based classifiers, selected
the best model by macro F1, and packaged the workflow with executive-style risk
outputs, feature importance, a Streamlit scoring app, and an offline one-file
HTML report.

## Limitations

This project is synthetic and should not be used for real investment or credit
decisions. It demonstrates workflow, modeling judgment, and communication. A
production model would need validated source data, backtesting, time-based
validation, threshold governance, and stakeholder review.

