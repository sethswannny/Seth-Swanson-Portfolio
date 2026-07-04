"""Generate a synthetic diversified REIT portfolio risk dataset.

The records are fictional and built for a portfolio-safe machine learning
project. No employer data, schemas, tenant names, or confidential business logic
are used.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_SEED = 2026
N_ROWS = 5200

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


PROPERTY_TYPES = {
    "Industrial": {"base_rent": 1_950_000, "base_cap": 0.063, "volatility": 0.72},
    "Grocery": {"base_rent": 1_420_000, "base_cap": 0.058, "volatility": 0.55},
    "Quick Service Restaurant": {"base_rent": 520_000, "base_cap": 0.059, "volatility": 0.65},
    "Medical Office": {"base_rent": 880_000, "base_cap": 0.061, "volatility": 0.58},
    "Automotive Service": {"base_rent": 610_000, "base_cap": 0.066, "volatility": 0.70},
    "Convenience Store": {"base_rent": 430_000, "base_cap": 0.057, "volatility": 0.52},
    "Fitness": {"base_rent": 720_000, "base_cap": 0.071, "volatility": 0.88},
    "Entertainment": {"base_rent": 1_150_000, "base_cap": 0.078, "volatility": 1.05},
    "Office": {"base_rent": 1_080_000, "base_cap": 0.082, "volatility": 1.10},
    "Distribution": {"base_rent": 2_250_000, "base_cap": 0.060, "volatility": 0.62},
}

REGIONS = {
    "Southwest": {"growth": 0.018, "market": 1.03},
    "Southeast": {"growth": 0.015, "market": 1.01},
    "Mountain": {"growth": 0.021, "market": 1.04},
    "Midwest": {"growth": 0.006, "market": 0.97},
    "Northeast": {"growth": 0.004, "market": 0.99},
    "West Coast": {"growth": 0.011, "market": 1.08},
}

INDUSTRIES = [
    "Logistics",
    "Grocery",
    "Restaurant",
    "Healthcare",
    "Auto",
    "Fuel",
    "Fitness",
    "Entertainment",
    "Professional Services",
    "Manufacturing",
]

CREDIT_TIERS = {
    "Investment Grade": {"weight": 0.18, "risk": -18},
    "Strong Private": {"weight": 0.28, "risk": -10},
    "Stable": {"weight": 0.31, "risk": 0},
    "Watch": {"weight": 0.16, "risk": 13},
    "Weak": {"weight": 0.07, "risk": 28},
}


def clipped_normal(rng: np.random.Generator, mean: float, std: float, low: float, high: float) -> float:
    return float(np.clip(rng.normal(mean, std), low, high))


def generate_dataset(n_rows: int = N_ROWS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    property_names = list(PROPERTY_TYPES)
    region_names = list(REGIONS)
    credit_names = list(CREDIT_TIERS)
    credit_weights = np.array([CREDIT_TIERS[name]["weight"] for name in credit_names])
    credit_weights = credit_weights / credit_weights.sum()

    rows = []
    for idx in range(1, n_rows + 1):
        property_type = str(rng.choice(property_names, p=[0.14, 0.10, 0.13, 0.10, 0.10, 0.11, 0.08, 0.07, 0.08, 0.09]))
        region = str(rng.choice(region_names, p=[0.18, 0.23, 0.12, 0.19, 0.13, 0.15]))
        industry = str(rng.choice(INDUSTRIES))
        credit_tier = str(rng.choice(credit_names, p=credit_weights))

        type_cfg = PROPERTY_TYPES[property_type]
        region_cfg = REGIONS[region]
        type_vol = type_cfg["volatility"]
        credit_risk = CREDIT_TIERS[credit_tier]["risk"]

        annual_rent = max(130_000, rng.lognormal(np.log(type_cfg["base_rent"] * region_cfg["market"]), 0.38))
        property_value = annual_rent / clipped_normal(rng, type_cfg["base_cap"], 0.009, 0.045, 0.105)
        asset_age = int(rng.integers(1, 42))
        lease_term_remaining = clipped_normal(rng, 7.1, 3.8, 0.2, 18.0)
        occupancy_rate = clipped_normal(rng, 0.965 - 0.015 * (type_vol - 0.7), 0.035, 0.72, 1.0)
        rent_coverage_ratio = clipped_normal(rng, 2.45 - (credit_risk / 55) - 0.22 * (type_vol - 0.7), 0.58, 0.35, 5.5)
        noi_margin = clipped_normal(rng, 0.68 - 0.03 * (type_vol - 0.7), 0.08, 0.35, 0.86)
        sales_trend_12m = clipped_normal(rng, region_cfg["growth"] - 0.02 * (type_vol - 0.7) - credit_risk / 900, 0.085, -0.34, 0.31)
        traffic_trend_12m = clipped_normal(rng, region_cfg["growth"] - credit_risk / 1100, 0.075, -0.30, 0.28)
        capex_need_pct_value = clipped_normal(rng, 0.011 + asset_age / 2500 + max(type_vol - 0.7, 0) * 0.01, 0.013, 0.0, 0.09)
        delinquency_days = int(np.clip(rng.gamma(1.0 + max(credit_risk, 0) / 18, 5.5), 0, 95))
        arrears_pct_annual_rent = clipped_normal(rng, delinquency_days / 1600 + max(credit_risk, 0) / 900, 0.025, 0, 0.32)
        tenant_concentration_pct = clipped_normal(rng, 0.025 + annual_rent / 95_000_000, 0.018, 0.003, 0.18)
        local_unemployment = clipped_normal(rng, 0.042 - region_cfg["growth"] / 6, 0.012, 0.021, 0.089)
        market_rent_growth = clipped_normal(rng, region_cfg["growth"] + 0.004, 0.035, -0.08, 0.12)
        renewal_probability = clipped_normal(
            rng,
            0.78
            + (lease_term_remaining - 5) * 0.018
            + (rent_coverage_ratio - 2) * 0.075
            + sales_trend_12m * 0.55
            - max(credit_risk, 0) * 0.006,
            0.12,
            0.12,
            0.98,
        )

        risk_score = (
            46
            + credit_risk
            + (2.0 - rent_coverage_ratio) * 15
            + (0.94 - occupancy_rate) * 85
            + max(0, 5.0 - lease_term_remaining) * 3.2
            + delinquency_days * 0.38
            + arrears_pct_annual_rent * 95
            + max(0, -sales_trend_12m) * 80
            + max(0, -traffic_trend_12m) * 42
            + capex_need_pct_value * 95
            + local_unemployment * 75
            - market_rent_growth * 35
            - renewal_probability * 18
            + type_vol * 8
            + rng.normal(0, 5.5)
        )
        risk_score = float(np.clip(risk_score, 0, 100))

        if risk_score >= 68:
            portfolio_health = "at risk"
        elif risk_score >= 46:
            portfolio_health = "watchlist"
        else:
            portfolio_health = "healthy"

        rows.append({
            "asset_id": f"REIT-{idx:05d}",
            "property_type": property_type,
            "region": region,
            "tenant_industry": industry,
            "credit_tier": credit_tier,
            "annual_rent": round(float(annual_rent), 2),
            "property_value": round(float(property_value), 2),
            "asset_age": asset_age,
            "lease_term_remaining": round(lease_term_remaining, 2),
            "occupancy_rate": round(occupancy_rate, 4),
            "rent_coverage_ratio": round(rent_coverage_ratio, 3),
            "noi_margin": round(noi_margin, 4),
            "sales_trend_12m": round(sales_trend_12m, 4),
            "traffic_trend_12m": round(traffic_trend_12m, 4),
            "capex_need_pct_value": round(capex_need_pct_value, 4),
            "delinquency_days": delinquency_days,
            "arrears_pct_annual_rent": round(arrears_pct_annual_rent, 4),
            "tenant_concentration_pct": round(tenant_concentration_pct, 4),
            "local_unemployment": round(local_unemployment, 4),
            "market_rent_growth": round(market_rent_growth, 4),
            "renewal_probability": round(renewal_probability, 4),
            "synthetic_risk_score": round(risk_score, 2),
            "portfolio_health": portfolio_health,
        })

    return pd.DataFrame(rows)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    data = generate_dataset()
    raw_path = RAW_DIR / "synthetic_reit_assets.csv"
    processed_path = PROCESSED_DIR / "modeling_dataset.csv"
    data.to_csv(raw_path, index=False)
    data.to_csv(processed_path, index=False)
    print(f"Wrote {len(data):,} rows to {processed_path}")
    print(data["portfolio_health"].value_counts().to_string())
    print(data.head(3).to_string(index=False))


if __name__ == "__main__":
    main()
