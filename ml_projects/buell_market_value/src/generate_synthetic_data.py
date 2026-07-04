"""Generate a portfolio-safe motorcycle marketplace dataset.

The dataset is synthetic and designed for model-building practice. It does not
scrape live listings or claim to represent official valuations.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_SEED = 42
N_ROWS = 3000

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


BIKES = [
    {
        "make": "Buell",
        "model": "Hammerhead 1190",
        "family": "superbike",
        "start_year": 2023,
        "end_year": 2026,
        "engine_cc": 1190,
        "horsepower": 185,
        "torque_ft_lbs": 102,
        "weight_lbs": 419,
        "base_msrp": 19995,
        "rarity": 1.28,
        "brand_heat": 1.10,
        "abs": 1,
        "carbon_fiber": 1,
    },
    {
        "make": "Buell",
        "model": "1190SX",
        "family": "streetfighter",
        "start_year": 2014,
        "end_year": 2026,
        "engine_cc": 1190,
        "horsepower": 185,
        "torque_ft_lbs": 102,
        "weight_lbs": 414,
        "base_msrp": 19995,
        "rarity": 1.18,
        "brand_heat": 1.08,
        "abs": 1,
        "carbon_fiber": 1,
    },
    {
        "make": "Buell",
        "model": "Super Cruiser",
        "family": "performance cruiser",
        "start_year": 2025,
        "end_year": 2026,
        "engine_cc": 1190,
        "horsepower": 175,
        "torque_ft_lbs": 94,
        "weight_lbs": 485,
        "base_msrp": 23995,
        "rarity": 1.38,
        "brand_heat": 1.16,
        "abs": 1,
        "carbon_fiber": 0,
    },
    {
        "make": "Buell",
        "model": "XB12R Firebolt",
        "family": "sportbike",
        "start_year": 2004,
        "end_year": 2010,
        "engine_cc": 1203,
        "horsepower": 103,
        "torque_ft_lbs": 84,
        "weight_lbs": 395,
        "base_msrp": 10995,
        "rarity": 1.12,
        "brand_heat": 1.02,
        "abs": 0,
        "carbon_fiber": 0,
    },
    {
        "make": "Buell",
        "model": "1125CR",
        "family": "streetfighter",
        "start_year": 2009,
        "end_year": 2010,
        "engine_cc": 1125,
        "horsepower": 146,
        "torque_ft_lbs": 82,
        "weight_lbs": 375,
        "base_msrp": 11995,
        "rarity": 1.15,
        "brand_heat": 1.04,
        "abs": 0,
        "carbon_fiber": 0,
    },
    {
        "make": "Buell",
        "model": "Blast",
        "family": "standard",
        "start_year": 2000,
        "end_year": 2009,
        "engine_cc": 492,
        "horsepower": 34,
        "torque_ft_lbs": 30,
        "weight_lbs": 360,
        "base_msrp": 4595,
        "rarity": 0.88,
        "brand_heat": 0.93,
        "abs": 0,
        "carbon_fiber": 0,
    },
    {
        "make": "Ducati",
        "model": "Monster",
        "family": "naked",
        "start_year": 2012,
        "end_year": 2026,
        "engine_cc": 937,
        "horsepower": 111,
        "torque_ft_lbs": 69,
        "weight_lbs": 414,
        "base_msrp": 12995,
        "rarity": 1.02,
        "brand_heat": 1.09,
        "abs": 1,
        "carbon_fiber": 0,
    },
    {
        "make": "Yamaha",
        "model": "MT-09",
        "family": "naked",
        "start_year": 2014,
        "end_year": 2026,
        "engine_cc": 890,
        "horsepower": 117,
        "torque_ft_lbs": 68,
        "weight_lbs": 417,
        "base_msrp": 10499,
        "rarity": 0.96,
        "brand_heat": 1.03,
        "abs": 1,
        "carbon_fiber": 0,
    },
    {
        "make": "Harley-Davidson",
        "model": "Sportster S",
        "family": "performance cruiser",
        "start_year": 2021,
        "end_year": 2026,
        "engine_cc": 1252,
        "horsepower": 121,
        "torque_ft_lbs": 94,
        "weight_lbs": 502,
        "base_msrp": 16999,
        "rarity": 0.98,
        "brand_heat": 1.08,
        "abs": 1,
        "carbon_fiber": 0,
    },
    {
        "make": "KTM",
        "model": "1290 Super Duke R",
        "family": "naked",
        "start_year": 2014,
        "end_year": 2026,
        "engine_cc": 1301,
        "horsepower": 177,
        "torque_ft_lbs": 103,
        "weight_lbs": 440,
        "base_msrp": 19999,
        "rarity": 1.03,
        "brand_heat": 1.08,
        "abs": 1,
        "carbon_fiber": 0,
    },
    {
        "make": "BMW",
        "model": "S1000R",
        "family": "naked",
        "start_year": 2014,
        "end_year": 2026,
        "engine_cc": 999,
        "horsepower": 165,
        "torque_ft_lbs": 84,
        "weight_lbs": 438,
        "base_msrp": 14995,
        "rarity": 1.00,
        "brand_heat": 1.07,
        "abs": 1,
        "carbon_fiber": 0,
    },
]

REGION_MULTIPLIER = {
    "Southwest": 1.03,
    "West Coast": 1.08,
    "Mountain": 1.01,
    "Midwest": 0.96,
    "Southeast": 0.98,
    "Northeast": 1.04,
}

CONDITION_MULTIPLIER = {
    "poor": 0.68,
    "fair": 0.82,
    "good": 0.94,
    "very good": 1.03,
    "excellent": 1.12,
}

SELLER_MULTIPLIER = {
    "private": 0.98,
    "dealer": 1.06,
    "auction": 0.94,
}

SEASON_MULTIPLIER = {
    "winter": 0.94,
    "spring": 1.06,
    "summer": 1.04,
    "fall": 0.99,
}


def weighted_choice(rng: np.random.Generator, items: list[dict]) -> dict:
    """Choose bikes with extra weight on Buell but enough comparables for context."""
    weights = np.array([
        0.13 if item["make"] == "Buell" and item["model"] in {"1190SX", "Hammerhead 1190"} else
        0.10 if item["make"] == "Buell" else
        0.055
        for item in items
    ])
    weights = weights / weights.sum()
    return items[int(rng.choice(len(items), p=weights))]


def generate_dataset(n_rows: int = N_ROWS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    current_year = 2026
    rows = []

    for listing_id in range(1, n_rows + 1):
        bike = weighted_choice(rng, BIKES)
        year = int(rng.integers(bike["start_year"], bike["end_year"] + 1))
        age = max(current_year - year, 0)

        yearly_miles = max(250, rng.normal(3300, 1650))
        mileage = int(max(35, age * yearly_miles + rng.normal(0, 1800)))
        if age <= 1:
            mileage = int(max(20, rng.normal(1200, 850)))

        condition = str(rng.choice(
            ["poor", "fair", "good", "very good", "excellent"],
            p=[0.04, 0.11, 0.34, 0.32, 0.19],
        ))
        seller_type = str(rng.choice(["private", "dealer", "auction"], p=[0.56, 0.34, 0.10]))
        region = str(rng.choice(list(REGION_MULTIPLIER)))
        season = str(rng.choice(list(SEASON_MULTIPLIER)))
        title_status = str(rng.choice(["clean", "lien", "rebuilt"], p=[0.88, 0.08, 0.04]))

        mods_score = float(np.clip(rng.normal(0.35, 0.24), 0, 1))
        service_records = int(rng.choice([0, 1], p=[0.32, 0.68]))
        num_photos = int(np.clip(rng.normal(11, 4), 1, 24))
        description_score = float(np.round(np.clip(rng.normal(0.68, 0.2), 0.05, 1), 3))
        days_on_market = int(np.clip(rng.gamma(3.0, 8.0), 1, 120))

        mileage_penalty = np.exp(-mileage / 70000)
        age_penalty = 0.89 ** age
        performance_bonus = 1 + ((bike["horsepower"] / max(bike["weight_lbs"], 1)) - 0.18) * 0.35
        title_multiplier = {"clean": 1.0, "lien": 0.95, "rebuilt": 0.72}[title_status]
        records_bonus = 1.04 if service_records else 0.97
        mods_multiplier = 1 + (mods_score - 0.35) * 0.12

        fair_market_value = (
            bike["base_msrp"]
            * age_penalty
            * mileage_penalty
            * CONDITION_MULTIPLIER[condition]
            * SELLER_MULTIPLIER[seller_type]
            * REGION_MULTIPLIER[region]
            * SEASON_MULTIPLIER[season]
            * title_multiplier
            * records_bonus
            * mods_multiplier
            * bike["rarity"]
            * bike["brand_heat"]
            * performance_bonus
        )

        listing_noise = rng.normal(1.0, 0.11)
        listing_price = float(np.clip(fair_market_value * listing_noise, 1200, 32000))
        fair_market_value = float(np.clip(fair_market_value, 1000, 34000))
        deal_delta_pct = (listing_price - fair_market_value) / fair_market_value

        if deal_delta_pct <= -0.12:
            deal_quality = "strong deal"
        elif deal_delta_pct <= -0.04:
            deal_quality = "fair deal"
        elif deal_delta_pct <= 0.08:
            deal_quality = "market price"
        else:
            deal_quality = "overpriced"

        rows.append({
            "listing_id": f"L{listing_id:05d}",
            "make": bike["make"],
            "model": bike["model"],
            "family": bike["family"],
            "year": year,
            "age": age,
            "mileage": mileage,
            "condition": condition,
            "seller_type": seller_type,
            "region": region,
            "season": season,
            "title_status": title_status,
            "engine_cc": bike["engine_cc"],
            "horsepower": bike["horsepower"],
            "torque_ft_lbs": bike["torque_ft_lbs"],
            "weight_lbs": bike["weight_lbs"],
            "power_to_weight": round(bike["horsepower"] / bike["weight_lbs"], 4),
            "abs": bike["abs"],
            "carbon_fiber": bike["carbon_fiber"],
            "mods_score": round(mods_score, 3),
            "service_records": service_records,
            "num_photos": num_photos,
            "description_score": description_score,
            "days_on_market": days_on_market,
            "listing_price": round(listing_price, 2),
            "synthetic_fair_market_value": round(fair_market_value, 2),
            "deal_delta_pct": round(deal_delta_pct, 4),
            "deal_quality": deal_quality,
        })

    return pd.DataFrame(rows)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    data = generate_dataset()
    raw_path = RAW_DIR / "synthetic_motorcycle_listings.csv"
    processed_path = PROCESSED_DIR / "modeling_dataset.csv"
    data.to_csv(raw_path, index=False)
    data.to_csv(processed_path, index=False)

    print(f"Wrote {len(data):,} rows to {processed_path}")
    print(data.head(3).to_string(index=False))


if __name__ == "__main__":
    main()
