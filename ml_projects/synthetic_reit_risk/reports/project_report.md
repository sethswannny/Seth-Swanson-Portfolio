# Synthetic REIT Portfolio Risk Model

## Executive Summary

This project classifies synthetic REIT assets as `healthy`, `watchlist`, or `at
risk` using financial, lease, tenant, and market signals.

The project is intentionally portfolio-safe. It does not use employer data,
tenant names, internal schemas, proprietary calculations, or confidential
dashboards.

## Business Use Case

A portfolio team could use a model like this to:

- screen assets for watchlist review
- identify drivers behind risk movement
- prioritize follow-up with asset managers
- summarize exposure by property type and asset health
- translate model output into executive-ready reporting

## Data

The generated dataset includes 5,200 fictional assets across a diversified real
estate portfolio. Features include property type, region, tenant credit tier,
annual rent, property value, occupancy, rent coverage, lease term, delinquency,
arrears, capex need, market rent growth, and renewal probability.

## Modeling Approach

The target is `portfolio_health`.

Models trained:

- Logistic regression
- Random forest classifier
- Histogram gradient boosting classifier

The best model is selected by macro F1.

## Key Outputs

- Saved model: `models/best_health_classifier.joblib`
- Metrics: `reports/model_metrics.csv`
- Classification report: `reports/classification_report.csv`
- Confusion matrix: `reports/confusion_matrix.csv`
- Feature importance: `reports/feature_importance.csv`
- Top watchlist assets: `reports/top_watchlist_assets.csv`
- Demo app: `app.py`
- Offline report: `dist/reit_risk_one_file.html`

## What This Demonstrates

- Synthetic data design for a realistic business problem
- Classification modeling and class-aware evaluation
- Feature importance and explainability
- Executive-style portfolio risk communication
- Turning model output into a scoring app and offline report

