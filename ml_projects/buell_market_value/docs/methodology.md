# Methodology

## Business Question

Can a motorcycle marketplace model estimate a fair listing price for used Buell
motorcycles and identify listings that look underpriced or overpriced?

This is framed as a portfolio-safe marketplace analytics problem. The model is
not an official appraisal tool. It demonstrates end-to-end data science:
problem framing, data generation, feature engineering, model comparison,
evaluation, explainability, and a lightweight decision app.

## Why Buell?

Buell is an interesting target because the brand combines current high
performance models with a used market that includes older and rarer motorcycles.
That creates a useful modeling problem: resale value is shaped by specs,
condition, mileage, model year, rarity, seller type, and market context.

## Data Strategy

The dataset is synthetic and generated from transparent assumptions. It is based
on listing-style fields that a public marketplace could expose:

- motorcycle make, model, year, mileage, and condition
- performance specs such as horsepower, torque, weight, and engine size
- marketplace details such as seller type, region, season, and days on market
- listing quality signals such as photo count, description quality, and service records

The synthetic approach keeps the project safe to publish while still proving the
technical workflow.

## Modeling Approach

The target variable is `listing_price`.

Models trained:

- Ridge regression as a simple baseline
- Random forest regressor as a nonlinear tree-based model
- Histogram gradient boosting regressor as the final candidate model

Categorical features are one-hot encoded. Numeric features are standardized for
models that benefit from scaling. The best model is selected by test-set MAE.

## Evaluation

Primary metric:

- Mean Absolute Error, because price errors are easiest to explain in dollars

Supporting metrics:

- RMSE
- R-squared
- MAPE

The final reporting also includes:

- actual vs. predicted plot
- residual plot
- permutation feature importance
- top modeled deal examples

## Portfolio Framing

Suggested resume bullet:

Built a Buell-focused motorcycle market value model using synthetic marketplace
data, feature engineering, tree-based regression, model evaluation, and a
Streamlit decision app to estimate fair listing prices and flag underpriced
opportunities.

## Sources Used For Context

- Buell official Hammerhead 1190 specs: https://buellmotorcycle.com/hammerhead-1190
- Buell official 1190SX specs: https://buellmotorcycle.com/1190sx
- Buell official Super Cruiser specs: https://buellmotorcycle.com/super-cruiser
- Public used listing/value context from Cycle Trader, Classic.com, KBB, and marketplace dataset listings found during project planning.
