# Data Dictionary

This project uses a synthetic motorcycle listing dataset. It is designed to look
like marketplace data while avoiding scraping, private data, or official
valuation claims.

| Field | Description |
| --- | --- |
| `listing_id` | Synthetic listing identifier. |
| `make` | Motorcycle make. Buell listings are intentionally overrepresented. |
| `model` | Motorcycle model. |
| `family` | Segment such as superbike, streetfighter, sportbike, naked, or performance cruiser. |
| `year` | Model year. |
| `age` | 2026 minus model year. |
| `mileage` | Odometer mileage. |
| `condition` | Listing condition category. |
| `seller_type` | Private seller, dealer, or auction. |
| `region` | US market region. |
| `season` | Listing season. |
| `title_status` | Clean, lien, or rebuilt title. |
| `engine_cc` | Engine displacement. |
| `horsepower` | Approximate horsepower. |
| `torque_ft_lbs` | Approximate torque. |
| `weight_lbs` | Approximate weight. |
| `power_to_weight` | Horsepower divided by weight. |
| `abs` | Whether the bike has ABS in the synthetic record. |
| `carbon_fiber` | Whether carbon fiber bodywork is represented in the synthetic record. |
| `mods_score` | Synthetic 0-1 score for modification quality. |
| `service_records` | Whether maintenance records are available. |
| `num_photos` | Number of listing photos. |
| `description_score` | Synthetic 0-1 score for listing description completeness. |
| `days_on_market` | Days since listing was posted. |
| `listing_price` | Synthetic asking price and model target. |
| `synthetic_fair_market_value` | Hidden generated fair-value estimate used only to create realistic labels. |
| `deal_delta_pct` | Asking price relative to synthetic fair market value. |
| `deal_quality` | Synthetic business label: strong deal, fair deal, market price, or overpriced. |

