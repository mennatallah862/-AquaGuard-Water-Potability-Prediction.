import streamlit as st
import pandas as pd
import random
import joblib

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AquaGuard | Water Potability",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    /* =========================
       GLOBAL
    ========================= */

    html, body, .stApp, button, input,
    [data-testid="stWidgetLabel"] p {
        font-family: 'Poppins', 'Segoe UI', sans-serif !important;
    }

    .stApp {
        background:
            radial-gradient(1000px 500px at 90% -10%, rgba(6,182,212,.09), transparent 60%),
            radial-gradient(900px 520px at -10% 110%, rgba(2,132,199,.07), transparent 60%),
            linear-gradient(135deg, #f7fcff 0%, #eef8fe 50%, #f1fcfd 100%);
    }

    .block-container {
        max-width: 1400px;
        padding-top: 1.8rem;
        padding-bottom: 2rem;
    }

    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #b9d9e8; border-radius: 8px; }

    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    /* =========================
       ANIMATIONS
    ========================= */

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes heroRise {
        0%   { transform: translateY(0) scale(.7); opacity: 0; }
        15%  { opacity: .55; }
        100% { transform: translateY(-420px) scale(1.3); opacity: 0; }
    }

    @keyframes pulseSafe {
        0%,100% { box-shadow: 0 12px 30px rgba(16,185,129,.12); }
        50%     { box-shadow: 0 12px 44px rgba(16,185,129,.32); }
    }

    @keyframes pulseWarn {
        0%,100% { box-shadow: 0 12px 30px rgba(234,88,12,.12); }
        50%     { box-shadow: 0 12px 44px rgba(234,88,12,.30); }
    }

    /* =========================
       SIDEBAR
    ========================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b2437 0%, #0d3b5e 55%, #0e4d6e 100%) !important;
        border-right: 1px solid rgba(103,232,249,.18);
    }

    section[data-testid="stSidebar"] * {
        color: #eafaff !important;
    }

    .sidebar-logo {
        text-align: center;
        padding: 12px 0 22px 0;
    }

    .sidebar-logo-icon {
        font-size: 48px;
        margin-bottom: 5px;
        filter: drop-shadow(0 0 14px rgba(103,232,249,.45));
    }

    .sidebar-logo-title {
        font-size: 25px;
        font-weight: 800;
        letter-spacing: .5px;
        background: linear-gradient(90deg, #a5f3fc, #67e8f9, #ffffff);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sidebar-logo-subtitle {
        font-size: 12.5px;
        opacity: .7;
        margin-top: 5px;
    }

    .sidebar-card {
        background: rgba(255,255,255,.07);
        border: 1px solid rgba(125,211,252,.18);
        border-radius: 16px;
        padding: 16px 18px;
        margin-top: 16px;
    }

    .sidebar-card-title {
        font-size: 14.5px;
        font-weight: 700;
        margin-bottom: 12px;
        color: #a5f3fc !important;
    }

    .sidebar-item {
        font-size: 13px;
        margin: 9px 0;
        opacity: .92;
    }

    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(103,232,249,.35), transparent);
        margin: 6px 0 4px 0;
    }

    .ranges-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 11.5px;
    }

    .ranges-table td {
        padding: 6px 4px;
        border-bottom: 1px solid rgba(255,255,255,.08);
        color: #bfe3f2 !important;
    }

    .ranges-table tr:last-child td { border-bottom: none; }
    .ranges-table td:first-child { color: #eafaff !important; font-weight: 600; }

    section[data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(255,255,255,.06);
        border: 1px solid rgba(125,211,252,.16);
        border-radius: 14px;
    }

    /* =========================
       HERO
    ========================= */

    .hero {
        position: relative;
        overflow: hidden;
        z-index: 2;
        background: linear-gradient(135deg, #0b2437 0%, #0d3b5e 45%, #0e7490 100%);
        border-radius: 28px;
        padding: 46px 48px;
        box-shadow: 0 22px 50px rgba(11,36,55,.25);
        margin-bottom: 6px;
    }

    .hero:before {
        content: "";
        position: absolute;
        width: 300px; height: 300px;
        border-radius: 50%;
        background: rgba(34,211,238,.13);
        right: -80px; top: -110px;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 190px; height: 190px;
        border-radius: 50%;
        background: rgba(45,212,191,.10);
        right: 190px; bottom: -110px;
    }

    .hero-bubble {
        position: absolute;
        bottom: -120px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, rgba(165,243,252,.35), rgba(34,211,238,.05));
        animation: heroRise linear infinite;
        pointer-events: none;
    }

    .hero-content { position: relative; z-index: 3; }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,.12);
        border: 1px solid rgba(255,255,255,.20);
        padding: 7px 15px;
        border-radius: 999px;
        color: #a5f3fc;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 16px;
        letter-spacing: .4px;
    }

    .hero-title {
        color: white;
        font-size: 46px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 12px;
    }

    .hero-title .grad {
        background: linear-gradient(90deg, #67e8f9, #a5f3fc, #ffffff);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #cffafe;
        font-size: 16.5px;
        line-height: 1.7;
        max-width: 760px;
        opacity: .92;
    }

    .hero-chips {
        display: flex;
        gap: 10px;
        margin-top: 20px;
        flex-wrap: wrap;
    }

    .chip {
        background: rgba(255,255,255,.10);
        border: 1px solid rgba(255,255,255,.22);
        color: #cffafe;
        padding: 7px 15px;
        border-radius: 999px;
        font-size: 12.5px;
        font-weight: 600;
    }

    /* =========================
       WAVE DIVIDER
    ========================= */

    .wave-wrap {
        position: relative;
        z-index: 1;
        margin-top: -16px;
        line-height: 0;
    }

    /* =========================
       INFO CARDS
    ========================= */

    .info-card {
        background: rgba(255,255,255,.88);
        backdrop-filter: blur(8px);
        border: 1px solid #e0edf5;
        border-radius: 20px;
        padding: 22px;
        min-height: 150px;
        box-shadow: 0 8px 25px rgba(15,23,42,.06);
        height: 100%;
        transition: transform .25s ease, box-shadow .25s ease;
        animation: fadeUp .6s ease both;
    }

    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 34px rgba(8,145,178,.15);
    }

    .info-icon {
        width: 48px; height: 48px;
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 23px;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #cffafe, #e0f2fe);
        border: 1px solid #bae6fd;
    }

    .info-title {
        font-size: 16.5px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 7px;
    }

    .info-text {
        color: #64748b;
        font-size: 13px;
        line-height: 1.6;
    }

    /* =========================
       SECTION TITLES
    ========================= */

    .section-title {
        display: flex;
        align-items: center;
        gap: 11px;
        color: #0f172a;
        font-size: 24px;
        font-weight: 800;
        margin: 20px 0 4px 0;
    }

    .section-title .bar {
        display: inline-block;
        width: 6px; height: 26px;
        border-radius: 4px;
        background: linear-gradient(180deg, #22d3ee, #0e7490);
    }

    .section-subtitle {
        color: #64748b;
        font-size: 14px;
        margin: 0 0 18px 17px;
    }

    /* =========================
       GLASS CARD CONTAINERS
    ========================= */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,.92) !important;
        border: 1px solid #e0edf5 !important;
        border-radius: 22px !important;
        box-shadow: 0 10px 28px rgba(15,23,42,.06) !important;
    }

    /* =========================
       CATEGORY HEADERS
    ========================= */

    .cat-head {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 14px;
    }

    .cat-icon {
        width: 44px; height: 44px;
        border-radius: 13px;
        display: flex; align-items: center; justify-content: center;
        font-size: 21px;
        flex-shrink: 0;
    }

    .cat-title {
        color: #0f172a;
        font-size: 16px;
        font-weight: 800;
        line-height: 1.2;
    }

    .cat-sub {
        color: #64748b;
        font-size: 11.5px;
        margin-top: 2px;
    }

    /* =========================
       STREAMLIT INPUTS
    ========================= */

    div[data-testid="stNumberInput"] label p {
        color: #334155 !important;
        font-size: 13px !important;
        font-weight: 650 !important;
    }

    div[data-testid="stNumberInput"] input {
        border-radius: 11px !important;
        border: 1.5px solid #dbe7ef !important;
        background: #f8fbfe !important;
        color: #0f172a !important;
        transition: all .2s ease;
    }

    div[data-testid="stNumberInput"] input:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 0 3px rgba(6,182,212,.15) !important;
        background: #ffffff !important;
    }

    /* =========================
       PREDICT BUTTON
    ========================= */

    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        min-height: 56px;
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 50%, #0e7490 100%);
        color: white;
        border: none;
        font-size: 16.5px;
        font-weight: 800;
        letter-spacing: .3px;
        box-shadow: 0 12px 28px rgba(8,145,178,.30);
        transition: all .25s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 36px rgba(8,145,178,.42);
        filter: brightness(1.06);
    }

    div.stButton > button:active { transform: translateY(0); }

    /* =========================
       RESULT CARDS
    ========================= */

    .result-card {
        border-radius: 24px;
        padding: 32px 30px;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .result-safe {
        background: linear-gradient(135deg, #ecfdf5, #d1fae5);
        border: 1px solid #6ee7b7;
        animation: fadeUp .5s ease, pulseSafe 2.6s ease-in-out .6s infinite;
    }

    .result-unsafe {
        background: linear-gradient(135deg, #fff7ed, #ffedd5);
        border: 1px solid #fdba74;
        animation: fadeUp .5s ease, pulseWarn 2.6s ease-in-out .6s infinite;
    }

    .result-icon { font-size: 55px; margin-bottom: 8px; }

    .result-title {
        font-size: 29px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .safe-title { color: #065f46; }
    .unsafe-title { color: #c2410c; }

    .result-description {
        color: #475569;
        font-size: 14px;
        line-height: 1.65;
    }

    /* =========================
       PROBABILITY CARD
    ========================= */

    .probability-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 28px 30px;
        box-shadow: 0 12px 30px rgba(15,23,42,.07);
        height: 100%;
    }

    .probability-label {
        color: #64748b;
        font-size: 13.5px;
        font-weight: 650;
        margin-bottom: 5px;
    }

    .probability-value {
        color: #0e7490;
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 20px;
    }

    .progress-background {
        position: relative;
        width: 100%;
        height: 16px;
        background: #e6eef5;
        border-radius: 999px;
    }

    .progress-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #22d3ee, #0891b2);
        box-shadow: 0 2px 8px rgba(8,145,178,.35);
    }

    .threshold-marker {
        position: absolute;
        top: -5px; bottom: -5px;
        width: 3px;
        background: #0f172a;
        border-radius: 3px;
        box-shadow: 0 0 8px rgba(15,23,42,.4);
        z-index: 2;
    }

    .scale-row {
        display: flex;
        justify-content: space-between;
        color: #94a3b8;
        font-size: 11px;
        margin-top: 12px;
    }

    .scale-row .thr {
        color: #0f172a;
        font-weight: 700;
    }

    .threshold-text {
        color: #64748b;
        font-size: 12px;
        margin-top: 10px;
    }

    /* =========================
       SUMMARY CARDS
    ========================= */

    .summary-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 20px 22px;
        box-shadow: 0 7px 22px rgba(15,23,42,.05);
        height: 100%;
        transition: transform .2s ease, box-shadow .2s ease;
    }

    .summary-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(8,145,178,.12);
    }

    .summary-title {
        color: #0f172a;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 13px;
    }

    .summary-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 9px 0;
        border-bottom: 1px solid #f1f5f9;
        font-size: 13px;
    }

    .summary-item:last-child { border-bottom: none; }

    .summary-name { color: #64748b; }

    .summary-value {
        color: #0f172a;
        font-weight: 700;
    }

    /* =========================
       EMPTY STATE
    ========================= */

    .empty-state {
        text-align: center;
        color: #64748b;
        padding: 46px 20px;
        border: 1.5px dashed #bae6fd;
        border-radius: 22px;
        background: rgba(255,255,255,.6);
        font-size: 14.5px;
        margin-top: 24px;
    }

    .empty-state .empty-icon { font-size: 2.4rem; margin-bottom: 8px; }

    /* =========================
       FOOTER
    ========================= */

    .footer {
        text-align: center;
        padding: 32px 0 10px 0;
        color: #94a3b8;
        font-size: 12.5px;
    }

    /* =========================
       RESPONSIVE
    ========================= */

    @media (max-width: 820px) {
        .hero { padding: 32px 24px; }
        .hero-title { font-size: 33px; }
        .info-card { min-height: auto; }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    saved_data = joblib.load("water_potability_model.pkl")

    if not isinstance(saved_data, dict):
        raise ValueError(
            "The saved PKL file does not contain the expected dictionary."
        )

    if "model" not in saved_data:
        raise ValueError(
            "The 'model' key was not found in the PKL file."
        )

    model = saved_data["model"]

    threshold = saved_data.get("threshold", 0.50)

    return model, threshold


model, THRESHOLD = load_model()


# =========================================================
# FEATURES
# =========================================================

FEATURES = [
    "ph",
    "Hardness",
    "Solids",
    "Chloramines",
    "Sulfate",
    "Conductivity",
    "Organic_carbon",
    "Trihalomethanes",
    "Turbidity"
]


# =========================================================
# HELPERS
# =========================================================

def hero_bubbles(count=12):
    """Generate floating bubbles inside the hero."""

    random.seed(7)

    return "".join(
        f'<span class="hero-bubble" style="width:{s}px;height:{s}px;'
        f'left:{l}%;animation-duration:{d}s;animation-delay:-{dl}s;"></span>'
        for s, l, d, dl in (
            (
                random.randint(10, 75),
                random.randint(1, 96),
                round(random.uniform(9, 20), 1),
                round(random.uniform(0, 14), 1)
            )
            for _ in range(count)
        )
    )


def gauge_figure(probability):
    """Ocean-themed safety gauge."""

    is_safe = probability >= THRESHOLD
    number_color = "#065f46" if is_safe else "#c2410c"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        number={
            "suffix": " %",
            "font": {"size": 40, "color": number_color, "family": "Poppins"}
        },
        title={
            "text": "<b>SAFETY SCORE</b>",
            "font": {"size": 13, "color": "#64748b"}
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickcolor": "#94a3b8",
                "tickfont": {"size": 10, "color": "#94a3b8"}
            },
            "bar": {"color": "#0891b2", "thickness": 0.28},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, THRESHOLD * 100], "color": "rgba(249,115,22,.14)"},
                {"range": [THRESHOLD * 100, 100], "color": "rgba(16,185,129,.16)"}
            ],
            "threshold": {
                "line": {"color": "#0f172a", "width": 3},
                "thickness": 0.85,
                "value": THRESHOLD * 100
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=290,
        margin=dict(t=52, b=0, l=30, r=30),
        font={"family": "Poppins"}
    )

    return fig


def detail_rows(prediction, probability):
    """Result details rows."""

    if prediction == 1:
        label, accent = "Potable", "#059669"
    else:
        label, accent = "Not Potable", "#c2410c"

    margin = probability - THRESHOLD
    direction = "above" if margin >= 0 else "below"

    def row(key, value, color="#0f172a"):
        return (
            f'<div class="summary-item">'
            f'<span class="summary-name">{key}</span>'
            f'<span class="summary-value" style="color:{color};">{value}</span>'
            f'</div>'
        )

    rows = (
        row("Prediction", label, accent)
        + row("Probability (Potable)", f"{probability:.1%}")
        + row("Decision Threshold", f"{THRESHOLD:.2f}")
        + row("Margin from Threshold", f"{abs(margin):.1%} {direction}", accent)
    )

    return f"""
    <div class="summary-card">
        <div class="summary-title">📌 Result Details</div>
        {rows}
    </div>
    """


# =========================================================
# SIDEBAR
# =========================================================

RANGES = [
    ("pH", "0 – 14", "6.5 – 8.5"),
    ("Hardness", "mg/L", "60 – 200"),
    ("Solids", "ppm", "10k – 35k"),
    ("Chloramines", "mg/L", "2 – 10"),
    ("Sulfate", "mg/L", "250 – 400"),
    ("Conductivity", "µS/cm", "300 – 550"),
    ("Organic Carbon", "mg/L", "5 – 20"),
    ("Trihalomethanes", "µg/L", "40 – 90"),
    ("Turbidity", "NTU", "1 – 5")
]

ranges_rows = "".join(
    f"<tr><td>{name}</td><td>{unit}</td><td>{rng}</td></tr>"
    for name, unit, rng in RANGES
)

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-logo">
            <div class="sidebar-logo-icon">💧</div>
            <div class="sidebar-logo-title">AquaGuard</div>
            <div class="sidebar-logo-subtitle">Water Quality Intelligence</div>
        </div>
        <div class="sidebar-divider"></div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="sidebar-card">
            <div class="sidebar-card-title">🤖 Model Information</div>
            <div class="sidebar-item">🌲 Algorithm: Random Forest</div>
            <div class="sidebar-item">🎯 Decision Threshold: {THRESHOLD:.2f}</div>
            <div class="sidebar-item">🧪 Input Features: 9</div>
            <div class="sidebar-item">📊 Output: Potability (0 / 1)</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-card-title">📌 How It Works</div>
            <div class="sidebar-item">1️⃣ Enter water measurements</div>
            <div class="sidebar-item">2️⃣ Click Analyze</div>
            <div class="sidebar-item">3️⃣ Review the prediction</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("📋 Typical Ranges"):
        st.markdown(
            f"""
            <table class="ranges-table">
                <tr style="opacity:.65;">
                    <td>Parameter</td><td>Unit</td><td>Range</td>
                </tr>
                {ranges_rows}
            </table>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div style="text-align:center;opacity:.55;font-size:11.5px;margin-top:18px;">
            💧 AquaGuard · Machine Learning Project
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    f"""
    <div class="hero">
        {hero_bubbles()}
        <div class="hero-content">
            <div class="hero-badge">🤖 Machine Learning · Water Quality AI</div>
            <div class="hero-title">
                <span class="grad">AquaGuard</span> 💧
            </div>
            <div class="hero-subtitle">
                Analyze water quality parameters and estimate whether
                the water is suitable for drinking.
            </div>
            <div class="hero-chips">
                <span class="chip">🌲 Random Forest</span>
                <span class="chip">🎯 Threshold {THRESHOLD:.2f}</span>
                <span class="chip">🧪 9 Parameters</span>
                <span class="chip">⚡ Instant Analysis</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="wave-wrap">
        <svg viewBox="0 0 1440 80" width="100%" height="60" preserveAspectRatio="none">
            <path fill="rgba(6,182,212,.10)"
                d="M0,45 C240,80 480,10 720,35 C960,60 1200,15 1440,40 L1440,80 L0,80 Z"></path>
            <path fill="rgba(8,145,178,.07)"
                d="M0,60 C260,25 520,75 780,50 C1040,25 1240,65 1440,48 L1440,80 L0,80 Z"></path>
        </svg>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INFO CARDS
# =========================================================

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">🧪</div>
            <div class="info-title">9 Water Parameters</div>
            <div class="info-text">
                Enter physical and chemical measurements
                to analyze the water sample.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with info_col2:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon" style="background:linear-gradient(135deg,#ccfbf1,#cffafe);border-color:#99f6e4;">⚡</div>
            <div class="info-title">Instant Prediction</div>
            <div class="info-text">
                The trained model analyzes all inputs and returns
                a probability in real time.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with info_col3:
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-icon" style="background:linear-gradient(135deg,#fef3c7,#ffe4e6);border-color:#fde68a;">🎯</div>
            <div class="info-title">Optimized Threshold</div>
            <div class="info-text">
                The final decision uses the tuned threshold
                (<b>{THRESHOLD:.2f}</b>) from model evaluation.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# INPUT SECTION
# =========================================================

st.markdown(
    """
    <div class="section-title"><span class="bar"></span>🔬 Water Measurements</div>
    <div class="section-subtitle">Enter the values for the water sample below.</div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


# =========================================================
# COLUMN 1 · BASIC
# =========================================================

with col1:

    with st.container(border=True):

        st.markdown(
            """
            <div class="cat-head">
                <div class="cat-icon" style="background:linear-gradient(135deg,#cffafe,#e0f2fe);border:1px solid #bae6fd;">💧</div>
                <div>
                    <div class="cat-title">Basic Properties</div>
                    <div class="cat-sub">General characteristics of the sample</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        ph = st.number_input("pH", 0.0, 14.0, 7.2, 0.1, format="%.2f")
        hardness = st.number_input("Hardness (mg/L)", 0.0, 400.0, 180.0, 1.0, format="%.1f")
        solids = st.number_input("Solids (ppm)", 0.0, 70000.0, 15000.0, 100.0, format="%.0f")


# =========================================================
# COLUMN 2 · CHEMICAL
# =========================================================

with col2:

    with st.container(border=True):

        st.markdown(
            """
            <div class="cat-head">
                <div class="cat-icon" style="background:linear-gradient(135deg,#ccfbf1,#d1fae5);border:1px solid #99f6e4;">🧪</div>
                <div>
                    <div class="cat-title">Chemical Properties</div>
                    <div class="cat-sub">Important chemical measurements</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        chloramines = st.number_input("Chloramines (mg/L)", 0.0, 15.0, 7.0, 0.1, format="%.2f")
        sulfate = st.number_input("Sulfate (mg/L)", 0.0, 500.0, 330.0, 1.0, format="%.1f")
        organic_carbon = st.number_input("Organic Carbon (mg/L)", 0.0, 35.0, 12.0, 0.1, format="%.2f")


# =========================================================
# COLUMN 3 · ADDITIONAL
# =========================================================

with col3:

    with st.container(border=True):

        st.markdown(
            """
            <div class="cat-head">
                <div class="cat-icon" style="background:linear-gradient(135deg,#dbeafe,#cffafe);border:1px solid #bfdbfe;">🌊</div>
                <div>
                    <div class="cat-title">Additional Properties</div>
                    <div class="cat-sub">Additional water quality measurements</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        conductivity = st.number_input("Conductivity (µS/cm)", 0.0, 900.0, 420.0, 1.0, format="%.1f")
        trihalomethanes = st.number_input("Trihalomethanes (µg/L)", 0.0, 140.0, 70.0, 1.0, format="%.1f")
        turbidity = st.number_input("Turbidity (NTU)", 0.0, 8.0, 4.0, 0.1, format="%.2f")


# =========================================================
# PREDICT BUTTON
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

predict_button = st.button(
    "🔍  Analyze Water Quality",
    type="primary",
    use_container_width=True
)


# =========================================================
# PREDICTION
# =========================================================

if predict_button:

    sample = pd.DataFrame({
        "ph": [ph],
        "Hardness": [hardness],
        "Solids": [solids],
        "Chloramines": [chloramines],
        "Sulfate": [sulfate],
        "Conductivity": [conductivity],
        "Organic_carbon": [organic_carbon],
        "Trihalomethanes": [trihalomethanes],
        "Turbidity": [turbidity]
    })

    probability_safe = float(model.predict_proba(sample)[0, 1])

    prediction = int(probability_safe >= THRESHOLD)

    values = {
        "pH": ph,
        "Hardness": hardness,
        "Solids": solids,
        "Chloramines": chloramines,
        "Sulfate": sulfate,
        "Conductivity": conductivity,
        "Organic Carbon": organic_carbon,
        "Trihalomethanes": trihalomethanes,
        "Turbidity": turbidity
    }

    st.session_state["result"] = {
        "prediction": prediction,
        "probability": probability_safe,
        "values": values,
        "sample": sample
    }


# =========================================================
# RESULTS
# =========================================================

if "result" in st.session_state:

    result = st.session_state["result"]
    prediction = result["prediction"]
    probability_safe = result["probability"]
    values = result["values"]
    sample = result["sample"]

    st.markdown(
        """
        <div class="section-title"><span class="bar"></span>📊 Prediction Result</div>
        <div class="section-subtitle">Based on the entered water quality measurements.</div>
        """,
        unsafe_allow_html=True
    )

    with st.container(border=True):

        # -------------------------------------------------
        # Row 1 · Result + Probability
        # -------------------------------------------------

        result_col, probability_col = st.columns(2)

        with result_col:

            if prediction == 1:

                st.markdown(
                    """
                    <div class="result-card result-safe">
                        <div class="result-icon">💧</div>
                        <div class="result-title safe-title">Potable Water</div>
                        <div class="result-description">
                            The model predicts that this water sample is
                            <b>suitable for drinking</b> based on the
                            provided measurements.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="result-card result-unsafe">
                        <div class="result-icon">⚠️</div>
                        <div class="result-title unsafe-title">Not Potable</div>
                        <div class="result-description">
                            The model predicts that this water sample is
                            <b>not suitable for drinking</b> based on the
                            provided measurements.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with probability_col:

            probability_percent = probability_safe * 100

            st.markdown(
                f"""
                <div class="probability-card">
                    <div class="probability-label">Probability of Potability</div>
                    <div class="probability-value">{probability_percent:.1f}%</div>
                    <div class="progress-background">
                        <div class="progress-fill" style="width:{probability_percent:.2f}%;"></div>
                        <div class="threshold-marker" style="left:{THRESHOLD * 100:.0f}%;"></div>
                    </div>
                    <div class="scale-row">
                        <span>0%</span>
                        <span class="thr">▲ Threshold {THRESHOLD * 100:.0f}%</span>
                        <span>100%</span>
                    </div>
                    <div class="threshold-text">
                        The prediction is <b>{'Potable' if prediction == 1 else 'Not Potable'}</b>
                        because the probability is
                        {'≥' if prediction == 1 else '<'} the threshold.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # Row 2 · Gauge + Details
        # -------------------------------------------------

        st.markdown("<br>", unsafe_allow_html=True)

        gauge_col, details_col = st.columns(2)

        with gauge_col:
            if HAS_PLOTLY:
                st.plotly_chart(
                    gauge_figure(probability_safe),
                    use_container_width=True
                )
            else:
                st.bar_chart(
                    pd.DataFrame(
                        {"Probability": [1 - probability_safe, probability_safe]},
                        index=["Not Potable", "Potable"]
                    ),
                    color="#0891b2"
                )

        with details_col:
            st.markdown(detail_rows(prediction, probability_safe), unsafe_allow_html=True)

        # -------------------------------------------------
        # Row 3 · Sample Measurements
        # -------------------------------------------------

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="summary-title" style="font-size:17px;">📋 Sample Measurements</div>
            """,
            unsafe_allow_html=True
        )

        sum_col1, sum_col2, sum_col3 = st.columns(3)

        with sum_col1:
            st.markdown(
                f"""
                <div class="summary-card">
                    <div class="summary-item">
                        <span class="summary-name">pH</span>
                        <span class="summary-value">{values['pH']:.2f}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-name">Hardness</span>
                        <span class="summary-value">{values['Hardness']:.1f}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-name">Solids</span>
                        <span class="summary-value">{values['Solids']:.0f}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with sum_col2:
            st.markdown(
                f"""
                <div class="summary-card">
                    <div class="summary-item">
                        <span class="summary-name">Chloramines</span>
                        <span class="summary-value">{values['Chloramines']:.2f}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-name">Sulfate</span>
                        <span class="summary-value">{values['Sulfate']:.1f}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-name">Organic Carbon</span>
                        <span class="summary-value">{values['Organic Carbon']:.2f}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with sum_col3:
            st.markdown(
                f"""
                <div class="summary-card">
                    <div class="summary-item">
                        <span class="summary-name">Conductivity</span>
                        <span class="summary-value">{values['Conductivity']:.1f}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-name">Trihalomethanes</span>
                        <span class="summary-value">{values['Trihalomethanes']:.1f}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-name">Turbidity</span>
                        <span class="summary-value">{values['Turbidity']:.2f}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # Raw Data
        # -------------------------------------------------

        with st.expander("🔎 View Input Values as Table"):
            st.dataframe(
                sample.T.rename(columns={0: "Value"}),
                use_container_width=True
            )

else:

    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">🔍</div>
            Adjust the measurements and press
            <b>Analyze Water Quality</b> to see the prediction here.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        💧 AquaGuard &nbsp;•&nbsp; Water Potability Prediction
        &nbsp;•&nbsp; Powered by Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)