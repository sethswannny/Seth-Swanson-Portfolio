"""Streamlit demo for the Synthetic REIT Portfolio Risk Model."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "models" / "best_health_classifier.joblib"


PROPERTY_DEFAULTS = {
    "Industrial": {"tenant_industry": "Logistics", "annual_rent": 1_950_000, "property_value": 31_000_000},
    "Grocery": {"tenant_industry": "Grocery", "annual_rent": 1_420_000, "property_value": 24_500_000},
    "Quick Service Restaurant": {"tenant_industry": "Restaurant", "annual_rent": 520_000, "property_value": 8_800_000},
    "Medical Office": {"tenant_industry": "Healthcare", "annual_rent": 880_000, "property_value": 14_500_000},
    "Automotive Service": {"tenant_industry": "Auto", "annual_rent": 610_000, "property_value": 9_250_000},
    "Convenience Store": {"tenant_industry": "Fuel", "annual_rent": 430_000, "property_value": 7_500_000},
    "Fitness": {"tenant_industry": "Fitness", "annual_rent": 720_000, "property_value": 10_400_000},
    "Entertainment": {"tenant_industry": "Entertainment", "annual_rent": 1_150_000, "property_value": 14_800_000},
    "Office": {"tenant_industry": "Professional Services", "annual_rent": 1_080_000, "property_value": 13_200_000},
    "Distribution": {"tenant_industry": "Logistics", "annual_rent": 2_250_000, "property_value": 37_500_000},
}


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


def format_health(label: str) -> str:
    return {"healthy": "Healthy", "watchlist": "Watchlist", "at risk": "At Risk"}.get(label, label)


st.set_page_config(page_title="Synthetic REIT Risk Model", page_icon="🏢", layout="wide")
st.title("Synthetic REIT Portfolio Risk Model")
st.caption("Portfolio-safe synthetic demo. Not based on employer data or confidential business rules.")

if not MODEL_PATH.exists():
    st.error("Model artifact not found. Run `python src/generate_synthetic_data.py` and `python src/train_model.py` first.")
    st.stop()

model = load_model()
left, right = st.columns([0.95, 1.05])

with left:
    property_type = st.selectbox("Property type", list(PROPERTY_DEFAULTS))
    defaults = PROPERTY_DEFAULTS[property_type]
    region = st.selectbox("Region", ["Southwest", "Southeast", "Mountain", "Midwest", "Northeast", "West Coast"])
    tenant_industry = st.selectbox(
        "Tenant industry",
        ["Logistics", "Grocery", "Restaurant", "Healthcare", "Auto", "Fuel", "Fitness", "Entertainment", "Professional Services", "Manufacturing"],
        index=["Logistics", "Grocery", "Restaurant", "Healthcare", "Auto", "Fuel", "Fitness", "Entertainment", "Professional Services", "Manufacturing"].index(defaults["tenant_industry"]),
    )
    credit_tier = st.selectbox("Credit tier", ["Investment Grade", "Strong Private", "Stable", "Watch", "Weak"], index=2)
    annual_rent = st.number_input("Annual rent", min_value=100_000, max_value=5_000_000, value=defaults["annual_rent"], step=25_000)
    property_value = st.number_input("Property value", min_value=1_000_000, max_value=90_000_000, value=defaults["property_value"], step=250_000)
    asset_age = st.slider("Asset age", 1, 42, 14)
    lease_term_remaining = st.slider("Lease term remaining", 0.2, 18.0, 6.5, 0.1)
    occupancy_rate = st.slider("Occupancy rate", 0.72, 1.0, 0.96, 0.01)
    rent_coverage_ratio = st.slider("Rent coverage ratio", 0.35, 5.5, 2.15, 0.05)
    noi_margin = st.slider("NOI margin", 0.35, 0.86, 0.66, 0.01)
    sales_trend_12m = st.slider("Sales trend, 12m", -0.34, 0.31, 0.02, 0.01)
    traffic_trend_12m = st.slider("Traffic trend, 12m", -0.30, 0.28, 0.01, 0.01)
    delinquency_days = st.slider("Delinquency days", 0, 95, 4)
    arrears_pct_annual_rent = st.slider("Arrears as % annual rent", 0.0, 0.32, 0.02, 0.01)
    capex_need_pct_value = st.slider("Capex need as % value", 0.0, 0.09, 0.015, 0.005)
    tenant_concentration_pct = st.slider("Tenant concentration %", 0.003, 0.18, 0.035, 0.005)
    local_unemployment = st.slider("Local unemployment", 0.021, 0.089, 0.041, 0.002)
    market_rent_growth = st.slider("Market rent growth", -0.08, 0.12, 0.015, 0.005)
    renewal_probability = st.slider("Renewal probability", 0.12, 0.98, 0.74, 0.02)

input_row = {
    "property_type": property_type,
    "region": region,
    "tenant_industry": tenant_industry,
    "credit_tier": credit_tier,
    "annual_rent": annual_rent,
    "property_value": property_value,
    "asset_age": asset_age,
    "lease_term_remaining": lease_term_remaining,
    "occupancy_rate": occupancy_rate,
    "rent_coverage_ratio": rent_coverage_ratio,
    "noi_margin": noi_margin,
    "sales_trend_12m": sales_trend_12m,
    "traffic_trend_12m": traffic_trend_12m,
    "capex_need_pct_value": capex_need_pct_value,
    "delinquency_days": delinquency_days,
    "arrears_pct_annual_rent": arrears_pct_annual_rent,
    "tenant_concentration_pct": tenant_concentration_pct,
    "local_unemployment": local_unemployment,
    "market_rent_growth": market_rent_growth,
    "renewal_probability": renewal_probability,
}

frame = pd.DataFrame([input_row])
prediction = str(model.predict(frame)[0])
probabilities = dict(zip(model.classes_, model.predict_proba(frame)[0]))

with right:
    st.metric("Predicted health", format_health(prediction))
    st.subheader("Class probabilities")
    probability_frame = pd.DataFrame({
        "class": [format_health(label) for label in model.classes_],
        "probability": [probabilities[label] for label in model.classes_],
    }).sort_values("probability", ascending=False)
    st.dataframe(probability_frame, use_container_width=True, hide_index=True)

    if prediction == "at risk":
        st.error("This asset would be escalated for portfolio review.")
    elif prediction == "watchlist":
        st.warning("This asset should be monitored with a clear follow-up plan.")
    else:
        st.success("This asset profiles as healthy under the synthetic model.")

    st.subheader("Main risk context")
    st.write(
        "- Lower rent coverage, negative sales trends, delinquency, short lease term, and weak credit tier generally increase risk.\n"
        "- The model is synthetic and designed to demonstrate workflow, not to replace underwriting."
    )
    st.subheader("Input record")
    st.dataframe(frame.T.rename(columns={0: "value"}), use_container_width=True)
