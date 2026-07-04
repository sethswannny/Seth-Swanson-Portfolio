# Methodology

## Business Question

Can a synthetic REIT portfolio model classify assets into `healthy`,
`watchlist`, or `at risk` using financial, tenant, lease, and market indicators?

The goal is to demonstrate a portfolio-safe version of asset health analytics:
not to recreate any employer dashboard, schema, or proprietary workflow.

## Data Strategy

The dataset is synthetic. It includes a diversified real estate portfolio with
asset types such as:

- Industrial
- Grocery
- Quick Service Restaurant
- Medical Office
- Automotive Service
- Convenience Store
- Fitness
- Entertainment
- Office
- Distribution

Each record includes public-style or generic portfolio monitoring features:
rent coverage, occupancy, lease term, credit tier, delinquency, arrears, market
rent growth, sales trend, traffic trend, renewal probability, and capex need.

## Modeling Approach

Target variable:

`portfolio_health`

Classes:

- `healthy`
- `watchlist`
- `at risk`

Models trained:

- Logistic regression baseline
- Random forest classifier
- Histogram gradient boosting classifier

Categorical variables are one-hot encoded. Numeric variables are standardized.
The final model is selected by macro F1 so smaller classes matter.

## Evaluation

Primary metric:

- Macro F1

Supporting metrics:

- Accuracy
- Balanced accuracy
- Weighted F1
- Confusion matrix
- Classification report

## Portfolio Framing

Suggested resume bullet:

Built a portfolio-safe REIT asset health classifier using synthetic financial,
lease, tenant, and market indicators; compared baseline and tree-based models,
selected the final classifier by macro F1, and packaged the workflow with
executive-style risk outputs and a Streamlit demo.

## Limitations

This is a synthetic demonstration. It proves the modeling and communication
workflow, not real-world portfolio risk performance. A production version would
need validated source systems, time-based validation, business owner review, and
model governance.
