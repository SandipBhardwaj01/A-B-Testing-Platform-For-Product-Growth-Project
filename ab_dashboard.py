import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import beta
import numpy as np

# ---------------------------------
# LOAD DATA
# ---------------------------------
df = pd.read_csv("ab_test_data.csv")

group_stats = df.groupby("group").agg(
    impressions=("clicked", "count"),
    clicks=("clicked", "sum"),
    conversions=("converted", "sum")
)

# Metrics
ctr_A = group_stats.loc["A","clicks"] / group_stats.loc["A","impressions"]
ctr_B = group_stats.loc["B","clicks"] / group_stats.loc["B","impressions"]
cvr_A = group_stats.loc["A","conversions"] / group_stats.loc["A","impressions"]
cvr_B = group_stats.loc["B","conversions"] / group_stats.loc["B","impressions"]

ctr_uplift = ctr_B - ctr_A
cvr_uplift = cvr_B - cvr_A

# Bayesian Probability
post_A = beta(1+3276, 1+(100000-3276))
post_B = beta(1+3905, 1+(100000-3905))
samples_A = post_A.rvs(200000)
samples_B = post_B.rvs(200000)
probability = np.mean(samples_B > samples_A)

# ---------------------------------
# UI DESIGN
# ---------------------------------

st.set_page_config(page_title="A/B Testing Dashboard", layout="wide")

# Header
st.markdown("""
<style>
h1 { text-align: center; font-size:42px; font-weight:700; }
h2 { text-align: center; }
.metric-card {
    padding:22px; border-radius:20px;
    background:linear-gradient(145deg,#ffffff,#f0f0f0);
    border:1px solid #e0e0e0;
    box-shadow: 3px 3px 12px rgba(0,0,0,0.08);
    text-align:center;
}
.badge {
    font-size:22px; font-weight:600;
    color:white; background:#3CB371;
    padding:10px 22px; border-radius:50px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>A/B Testing Experiment Dashboard 🧠</h1>", unsafe_allow_html=True)
st.write("### Evaluation of New UX Variant Against Existing Design")

# ---------------------------------
# KPI ROW
# ---------------------------------
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1: st.markdown(f"<div class='metric-card'><h3>CTR A</h3><h2>{ctr_A:.2%}</h2></div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='metric-card'><h3>CTR B</h3><h2>{ctr_B:.2%}</h2></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='metric-card'><h3>CTR Uplift</h3><h2 style='color:green;'>{ctr_uplift:.2%}</h2></div>", unsafe_allow_html=True)

with col4: st.markdown(f"<div class='metric-card'><h3>CVR A</h3><h2>{cvr_A:.2%}</h2></div>", unsafe_allow_html=True)
with col5: st.markdown(f"<div class='metric-card'><h3>CVR B</h3><h2>{cvr_B:.2%}</h2></div>", unsafe_allow_html=True)
with col6: st.markdown(f"<div class='metric-card'><h3>CVR Uplift</h3><h2 style='color:green;'>{cvr_uplift:.2%}</h2></div>", unsafe_allow_html=True)

# Bayesian Badge
with col7: st.markdown(f"<div class='metric-card'><h3>Bayesian Win Prob</h3><div class='badge'>{probability:.2%}</div></div>", unsafe_allow_html=True)

st.write(" ")

# ---------------------------------
# Bayesian Posterior Visual
# ---------------------------------
st.subheader("Bayesian Posterior Confidence Distribution")
st.image("beta_posterior_distribution.png", use_column_width=True)

# ---------------------------------
# Recommendation Zone
# ---------------------------------
st.markdown("""
<div style='padding:30px; border-radius:18px; background:#e8ffe8; border:2px solid #4CAF50; text-align:center;'>
<h2> 🚀 Final Decision: Roll Out Variant B to 100% Traffic </h2>
<h4> CTR +29.8% | CVR +19.2% | Bayesian Confidence ≈ 100% </h4>
</div>
""", unsafe_allow_html=True)
