# Data Dictionary

This project uses a synthetic REIT asset-level dataset. Records are fictional and
designed to resemble portfolio health monitoring data without exposing employer
data, tenant data, schemas, or confidential business rules.

| Field | Description |
| --- | --- |
| `asset_id` | Synthetic asset identifier. |
| `property_type` | Asset segment such as Industrial, Grocery, Medical Office, or Office. |
| `region` | Broad US region. |
| `tenant_industry` | Tenant operating category. |
| `credit_tier` | Synthetic tenant credit band. |
| `annual_rent` | Annual contractual rent in synthetic dollars. |
| `property_value` | Synthetic property value estimate. |
| `asset_age` | Asset age in years. |
| `lease_term_remaining` | Remaining lease term in years. |
| `occupancy_rate` | Occupied percentage of the asset. |
| `rent_coverage_ratio` | Tenant-level rent coverage proxy. |
| `noi_margin` | Net operating income margin proxy. |
| `sales_trend_12m` | 12-month tenant sales trend. |
| `traffic_trend_12m` | 12-month traffic trend proxy. |
| `capex_need_pct_value` | Estimated capex need as a percentage of property value. |
| `delinquency_days` | Days delinquent on rent or reporting obligations. |
| `arrears_pct_annual_rent` | Arrears as a share of annual rent. |
| `tenant_concentration_pct` | Asset exposure as a share of total portfolio value. |
| `local_unemployment` | Local labor market risk proxy. |
| `market_rent_growth` | Local market rent growth proxy. |
| `renewal_probability` | Synthetic renewal likelihood. |
| `synthetic_risk_score` | Hidden generated risk score used to create the label. |
| `portfolio_health` | Target label: healthy, watchlist, or at risk. |

