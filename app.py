import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Bengaluru HomeScope",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM STYLE — YELLOW + WHITE
# =========================================================

st.markdown(
    """
    <style>
:root {
    --paper:     #FFFBEA;
    --card:      #FFFFFF;
    --ink:       #1F1B10;
    --muted:     #6B6450;
    --sun:       #FFD84D;
    --sun-deep:  #F2B705;
    --sun-soft:  #FFF3B8;
    --line:      #EADFA8;
    --radius:    14px;
    --radius-lg: 22px;
}

/* ---------- Base ---------- */
html, body, .stApp, [class*="st-"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.stApp {
    background-color: var(--paper);
    color: var(--ink);
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 4rem;
    max-width: 1200px;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0;
}

h1, h2, h3, h4 {
    font-family: 'Avenir Next', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    color: var(--ink);
    letter-spacing: -0.02em;
}

/* ---------- Title ---------- */
.main-title {
    font-family: 'Avenir Next', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: var(--ink);
    margin-bottom: 0.4rem;
}

.subtitle {
    font-size: 1.1rem;
    line-height: 1.55;
    color: var(--muted);
    max-width: 62ch;
    margin-bottom: 2.25rem;
}

/* ---------- Section header ---------- */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-family: 'Avenir Next', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--ink);
    margin: 2.25rem 0 1rem;
    padding: 0;
    background: none;
}

.section-header::before {
    content: "";
    width: 8px;
    height: 1.6rem;
    border-radius: 4px;
    background: var(--sun);
    flex-shrink: 0;
}

/* ---------- Metric cards ---------- */
.metric-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 1.25rem 1.1rem;
    text-align: left;
    box-shadow: 0 1px 2px rgba(31, 27, 16, 0.05);
    transition: border-color 0.15s ease;
}

.metric-card:hover {
    border-color: var(--sun-deep);
}

.metric-label {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--muted);
    margin-bottom: 0.4rem;
}

.metric-value {
    font-family: 'Avenir Next', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    line-height: 1.1;
    color: var(--ink);
    font-variant-numeric: tabular-nums;
}

/* ---------- Prediction result (the one loud element) ---------- */
.prediction-card {
    background: var(--sun);
    border: 2px solid var(--ink);
    border-radius: var(--radius-lg);
    box-shadow: 8px 8px 0 var(--ink);
    padding: 2.5rem 2rem;
    text-align: center;
    margin: 2rem 8px 2.25rem 0;
}

.prediction-label {
    font-size: 1rem;
    font-weight: 500;
    color: var(--ink);
    opacity: 0.75;
    margin-bottom: 0.25rem;
}

.prediction-value {
    font-family: 'Avenir Next', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: clamp(2.6rem, 7vw, 4.5rem);
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.03em;
    color: var(--ink);
    font-variant-numeric: tabular-nums;
}

/* ---------- Info box ---------- */
.info-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-left: 6px solid var(--sun);
    border-radius: var(--radius);
    padding: 1.25rem 1.4rem;
    margin-top: 1rem;
    line-height: 1.6;
    color: var(--ink);
}

/* ---------- Button ---------- */
.stButton > button {
    width: 100%;
    background-color: var(--ink);
    color: var(--sun);
    border: 2px solid var(--ink);
    border-radius: var(--radius);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-weight: 700;
    font-size: 1rem;
    padding: 0.75rem 1.4rem;
    transition: background-color 0.15s ease, color 0.15s ease, transform 0.1s ease;
}

.stButton > button:hover {
    background-color: var(--sun);
    color: var(--ink);
    border-color: var(--ink);
}

.stButton > button:active {
    transform: translateY(1px);
}

.stButton > button:focus-visible {
    outline: 3px solid var(--sun-deep);
    outline-offset: 3px;
}

/* ---------- Inputs ---------- */
label, .stSelectbox label, .stNumberInput label, .stSlider label {
    font-weight: 500 !important;
    color: var(--ink) !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"] {
    background-color: var(--card);
    border: 1px solid var(--line);
    border-radius: 10px;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

div[data-baseweb="select"] > div:hover,
div[data-baseweb="input"] > div:hover {
    border-color: var(--sun-deep);
}

div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] > div:focus-within {
    border-color: var(--ink);
    box-shadow: 0 0 0 3px var(--sun-soft);
}

/* Slider accent */
div[data-baseweb="slider"] [role="slider"] {
    background-color: var(--ink);
    border-color: var(--sun);
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    border-bottom: 2px solid var(--line);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--muted);
    border-radius: 10px 10px 0 0;
    padding: 0.65rem 1.25rem;
    font-weight: 500;
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--sun-soft);
    color: var(--ink);
}

.stTabs [aria-selected="true"] {
    background: var(--sun) !important;
    color: var(--ink) !important;
    font-weight: 700;
}

/* Hide the default red/blue tab underline so the yellow tab does the work */
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none;
}

/* ---------- Tables, alerts, sidebar ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: var(--radius);
    overflow: hidden;
}

[data-testid="stAlert"] {
    border-radius: var(--radius);
}

[data-testid="stSidebar"] {
    background-color: var(--sun-soft);
    border-right: 1px solid var(--line);
}

/* ---------- Small screens ---------- */
@media (max-width: 640px) {
    .block-container { padding-top: 1.5rem; }
    .prediction-card { padding: 1.75rem 1.25rem; box-shadow: 5px 5px 0 var(--ink); }
}

@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; }
}
</style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD FILES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "bengaluru_house_price_model.pkl"
DATA_PATH = BASE_DIR / "bengaluru_house_clean.csv"
EDA_DIR = BASE_DIR / "eda"


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


model = load_model()
df = load_data()


# =========================================================
# NORMALIZE LOCATION NAMES
# =========================================================

df["location"] = (
    df["location"]
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
    .str.title()
)


# Use the exact categories present in the cleaned training data
locations = sorted(df["location"].dropna().unique())
area_types = sorted(df["area_type"].dropna().unique())


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🏠 Bengaluru HomeScope</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Explore Bengaluru property trends and get a data-driven price estimate.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# TABS
# =========================================================

predict_tab, insights_tab = st.tabs(
    ["🏠 Price Predictor", "📊 Market Insights"]
)


# =========================================================
# TAB 1 — PRICE PREDICTOR
# =========================================================

with predict_tab:

    st.markdown(
        '<div class="section-header">Property Details</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        location = st.selectbox(
            "Location",
            locations,
            index=locations.index("Whitefield")
            if "Whitefield" in locations else 0
        )

        area_type = st.selectbox(
            "Area Type",
            area_types
        )

    with col2:

        bhk = st.number_input(
            "BHK",
            min_value=1,
            max_value=10,
            value=2,
            step=1
        )

        total_sqft = st.number_input(
            "Total Area (sqft)",
            min_value=300.0,
            max_value=20000.0,
            value=1200.0,
            step=50.0
        )

    with col3:

        bath = st.number_input(
            "Bathrooms",
            min_value=1,
            max_value=12,
            value=2,
            step=1
        )

        balcony = st.number_input(
            "Balconies",
            min_value=0,
            max_value=3,
            value=1,
            step=1
        )

    # Engineered feature used by the model
    sqft_per_bhk = total_sqft / bhk

    st.markdown(
        f"""
        <div class="info-card">
            <b>Derived property metric</b><br>
            Space per bedroom: <b>{sqft_per_bhk:,.0f} sqft/BHK</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    predict_button = st.button(
        "✨ Estimate Property Price"
    )

    if predict_button:

        input_data = pd.DataFrame({
            "area_type": [area_type],
            "location": [location],
            "bhk": [float(bhk)],
            "total_sqft": [float(total_sqft)],
            "bath": [float(bath)],
            "balcony": [float(balcony)],
            "sqft_per_bhk": [float(sqft_per_bhk)]
        })

        try:

            prediction = float(model.predict(input_data)[0])

            st.markdown(
                f"""
                <div class="prediction-card">
                    <div class="prediction-label">
                        Estimated Property Price
                    </div>
                    <div class="prediction-value">
                        ₹{prediction:,.2f} Lakh
                    </div>
                    <div style="font-size:1rem; color:#555;">
                        Approximately ₹{prediction / 100:,.2f} Crore
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Simple context metrics
            area_price_per_sqft = (
                prediction * 100000 / total_sqft
            )

            m1, m2, m3 = st.columns(3)

            with m1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Estimated price</div>
                        <div class="metric-value">
                            ₹{prediction:,.1f}L
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with m2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Estimated ₹/sqft</div>
                        <div class="metric-value">
                            ₹{area_price_per_sqft:,.0f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with m3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Space per BHK</div>
                        <div class="metric-value">
                            {sqft_per_bhk:,.0f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.caption(
                "This estimate is based on patterns learned from the "
                "Bengaluru housing dataset used to train the model. "
                "It should be treated as an estimate, not a formal property valuation."
            )

        except Exception as e:

            st.error(
                "Prediction failed. Check that the model and cleaned dataset "
                "were generated from the same preprocessing pipeline."
            )

            st.exception(e)


# =========================================================
# TAB 2 — MARKET INSIGHTS
# =========================================================

with insights_tab:

    st.markdown(
        '<div class="section-header">Bengaluru Housing Snapshot</div>',
        unsafe_allow_html=True
    )

    # Overall metrics
    median_price = df["price"].median()
    median_area = df["total_sqft"].median()
    median_bhk = df["bhk"].median()
    median_price_sqft = df["price_per_sqft"].median()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Median Price</div>
                <div class="metric-value">
                    ₹{median_price:,.0f}L
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Median Area</div>
                <div class="metric-value">
                    {median_area:,.0f} sqft
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Typical BHK</div>
                <div class="metric-value">
                    {median_bhk:.0f} BHK
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Median ₹/sqft</div>
                <div class="metric-value">
                    ₹{median_price_sqft:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # BHK ANALYSIS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-header">Price by BHK</div>',
        unsafe_allow_html=True
    )

    bhk_summary_path = EDA_DIR / "bhk_summary.csv"

    if bhk_summary_path.exists():

        bhk_summary = pd.read_csv(bhk_summary_path)

        st.bar_chart(
            bhk_summary.set_index("bhk")["median_price"],
            y_label="Median Price (₹ Lakh)",
            x_label="BHK"
        )

    else:

        bhk_fallback = (
            df.groupby("bhk")["price"]
            .median()
            .sort_index()
        )

        st.bar_chart(
            bhk_fallback,
            y_label="Median Price (₹ Lakh)",
            x_label="BHK"
        )

    # -----------------------------------------------------
    # TOP LOCATIONS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-header">Higher-Value Locations</div>',
        unsafe_allow_html=True
    )

    location_stats_path = EDA_DIR / "location_stats.csv"

    if location_stats_path.exists():

        location_stats = pd.read_csv(location_stats_path)

    else:

        location_stats = (
            df.groupby("location")
            .agg(
                property_count=("price", "count"),
                median_price=("price", "median"),
                median_sqft=("total_sqft", "median"),
                median_price_per_sqft=("price_per_sqft", "median")
            )
            .reset_index()
        )

    top_locations = (
        location_stats[
            location_stats["property_count"] >= 20
        ]
        .sort_values("median_price", ascending=False)
        .head(15)
    )

    st.dataframe(
        top_locations[
            [
                "location",
                "property_count",
                "median_price",
                "median_price_per_sqft"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # SAVED EDA VISUALIZATIONS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-header">Explore the Market</div>',
        unsafe_allow_html=True
    )

    graph1, graph2 = st.columns(2)

    price_graph = EDA_DIR / "price_distribution.png"
    area_graph = EDA_DIR / "area_vs_price.png"

    with graph1:

        if price_graph.exists():
            st.image(
                str(price_graph),
                caption="Distribution of property prices"
            )

    with graph2:

        if area_graph.exists():
            st.image(
                str(area_graph),
                caption="Property area vs price"
            )

    graph3, graph4 = st.columns(2)

    bhk_graph = EDA_DIR / "bhk_vs_price.png"
    psf_graph = EDA_DIR / "price_per_sqft_distribution.png"

    with graph3:

        if bhk_graph.exists():
            st.image(
                str(bhk_graph),
                caption="Price distribution across BHK categories"
            )

    with graph4:

        if psf_graph.exists():
            st.image(
                str(psf_graph),
                caption="Distribution of price per square foot"
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Bengaluru HomeScope • Built with Pandas, NumPy, "
    "Scikit-learn and Streamlit"
)