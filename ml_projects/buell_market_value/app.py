"""Streamlit demo for the Buell Market Value Predictor."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "models" / "best_price_model.joblib"


BIKE_DEFAULTS = {
    "Hammerhead 1190": {
        "make": "Buell",
        "family": "superbike",
        "engine_cc": 1190,
        "horsepower": 185,
        "torque_ft_lbs": 102,
        "weight_lbs": 419,
        "power_to_weight": 185 / 419,
        "abs": 1,
        "carbon_fiber": 1,
    },
    "1190SX": {
        "make": "Buell",
        "family": "streetfighter",
        "engine_cc": 1190,
        "horsepower": 185,
        "torque_ft_lbs": 102,
        "weight_lbs": 414,
        "power_to_weight": 185 / 414,
        "abs": 1,
        "carbon_fiber": 1,
    },
    "Super Cruiser": {
        "make": "Buell",
        "family": "performance cruiser",
        "engine_cc": 1190,
        "horsepower": 175,
        "torque_ft_lbs": 94,
        "weight_lbs": 485,
        "power_to_weight": 175 / 485,
        "abs": 1,
        "carbon_fiber": 0,
    },
    "XB12R Firebolt": {
        "make": "Buell",
        "family": "sportbike",
        "engine_cc": 1203,
        "horsepower": 103,
        "torque_ft_lbs": 84,
        "weight_lbs": 395,
        "power_to_weight": 103 / 395,
        "abs": 0,
        "carbon_fiber": 0,
    },
    "1125CR": {
        "make": "Buell",
        "family": "streetfighter",
        "engine_cc": 1125,
        "horsepower": 146,
        "torque_ft_lbs": 82,
        "weight_lbs": 375,
        "power_to_weight": 146 / 375,
        "abs": 0,
        "carbon_fiber": 0,
    },
    "Blast": {
        "make": "Buell",
        "family": "standard",
        "engine_cc": 492,
        "horsepower": 34,
        "torque_ft_lbs": 30,
        "weight_lbs": 360,
        "power_to_weight": 34 / 360,
        "abs": 0,
        "carbon_fiber": 0,
    },
}


def classify_deal(listing_price: float, predicted_price: float) -> tuple[str, float]:
    delta_pct = (listing_price - predicted_price) / predicted_price
    if delta_pct <= -0.12:
        label = "Strong deal"
    elif delta_pct <= -0.04:
        label = "Fair deal"
    elif delta_pct <= 0.08:
        label = "Market price"
    else:
        label = "Overpriced"
    return label, delta_pct


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


st.set_page_config(page_title="Buell Market Value Predictor", page_icon="🏍️", layout="wide")

st.title("Buell Market Value Predictor")
st.caption("Synthetic portfolio demo. Not an official appraisal or financial recommendation.")

if not MODEL_PATH.exists():
    st.error("Model artifact not found. Run `python src/generate_synthetic_data.py` and `python src/train_model.py` first.")
    st.stop()

model = load_model()

left, right = st.columns([0.95, 1.05])

with left:
    selected_model = st.selectbox("Model", list(BIKE_DEFAULTS))
    defaults = BIKE_DEFAULTS[selected_model]
    year = st.slider("Year", 2000, 2026, 2023)
    mileage = st.number_input("Mileage", min_value=0, max_value=120000, value=8500, step=500)
    condition = st.selectbox("Condition", ["poor", "fair", "good", "very good", "excellent"], index=3)
    seller_type = st.selectbox("Seller type", ["private", "dealer", "auction"])
    region = st.selectbox("Region", ["Southwest", "West Coast", "Mountain", "Midwest", "Southeast", "Northeast"])
    season = st.selectbox("Season", ["winter", "spring", "summer", "fall"], index=1)
    title_status = st.selectbox("Title status", ["clean", "lien", "rebuilt"])
    listing_price = st.number_input("Asking price", min_value=1000, max_value=35000, value=14500, step=250)
    mods_score = st.slider("Modification quality score", 0.0, 1.0, 0.45, 0.05)
    service_records = st.toggle("Service records available", value=True)
    num_photos = st.slider("Listing photos", 1, 24, 12)
    description_score = st.slider("Description quality score", 0.05, 1.0, 0.72, 0.05)
    days_on_market = st.slider("Days on market", 1, 120, 21)

input_row = {
    "make": defaults["make"],
    "model": selected_model,
    "family": defaults["family"],
    "year": year,
    "age": 2026 - year,
    "mileage": mileage,
    "condition": condition,
    "seller_type": seller_type,
    "region": region,
    "season": season,
    "title_status": title_status,
    "engine_cc": defaults["engine_cc"],
    "horsepower": defaults["horsepower"],
    "torque_ft_lbs": defaults["torque_ft_lbs"],
    "weight_lbs": defaults["weight_lbs"],
    "power_to_weight": defaults["power_to_weight"],
    "abs": defaults["abs"],
    "carbon_fiber": defaults["carbon_fiber"],
    "mods_score": mods_score,
    "service_records": int(service_records),
    "num_photos": num_photos,
    "description_score": description_score,
    "days_on_market": days_on_market,
}

prediction = float(model.predict(pd.DataFrame([input_row]))[0])
deal_label, delta_pct = classify_deal(float(listing_price), prediction)

with right:
    st.metric("Predicted fair listing price", f"${prediction:,.0f}")
    st.metric("Asking price vs. model", f"{delta_pct:+.1%}", deal_label)

    st.subheader("Interpretation")
    if deal_label == "Strong deal":
        st.success("The asking price is materially below the model estimate. Worth a closer look.")
    elif deal_label == "Fair deal":
        st.info("The listing appears somewhat favorable versus the model estimate.")
    elif deal_label == "Market price":
        st.info("The listing is close to the model's fair market range.")
    else:
        st.warning("The asking price is above the model estimate. Negotiate or compare alternatives.")

    st.subheader("Input record")
    st.dataframe(pd.DataFrame([input_row]).T.rename(columns={0: "value"}), use_container_width=True)
