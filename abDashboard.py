import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import beta


# LOAD DATA & METRICS

df = pd.read_csv("ab_test_data.csv")

group_stats = df.groupby("group").agg(
    impressions=("clicked", "count"),
    clicks=("clicked", "sum"),
    conversions=("converted", "sum")
)

ctr_A = group_stats.loc["A","clicks"] / group_stats.loc["A","impressions"]
ctr_B = group_stats.loc["B","clicks"] / group_stats.loc["B","impressions"]
cvr_A = group_stats.loc["A","conversions"] / group_stats.loc["A","impressions"]
cvr_B = group_stats.loc["B","conversions"] / group_stats.loc["B","impressions"]

ctr_abs_uplift = ctr_B - ctr_A
cvr_abs_uplift = cvr_B - cvr_A

ctr_rel_uplift = ctr_abs_uplift / ctr_A   # ~29.8%
cvr_rel_uplift = cvr_abs_uplift / cvr_A   # ~19.2%

# Bayesian probability (hard-coded from your results)
post_A = beta(1+3276, 1+(100000-3276))
post_B = beta(1+3905, 1+(100000-3905))
samples_A = post_A.rvs(200000)
samples_B = post_B.rvs(200000)
bayes_prob = float(np.mean(samples_B > samples_A))

# small helper
def pct(x): return f"{x*100:.2f}%"


# PAGE CONFIG & CUSTOM CSS

st.set_page_config(
    page_title="A/B Testing – UX Experiment",
    layout="wide",
    page_icon="🧠"
)

st.markdown("""
<style>
body { background-color:#f5f5f7; }
.big-title {
    text-align:center;
    font-size:38px;
    font-weight:700;
    padding-top:10px;
}
.sub-title {
    text-align:center;
    font-size:17px;
    color:#555;
    padding-bottom:18px;
}
.metric-card {
    padding:18px 16px;
    border-radius:18px;
    background:#ffffff;
    border:1px solid #e2e2e2;
    box-shadow:0 4px 12px rgba(0,0,0,0.04);
}
.metric-label {
    font-size:14px;
    color:#666;
}
.metric-value {
    font-size:22px;
    font-weight:700;
}
.metric-sub {
    font-size:13px;
    color:#888;
}
.decision-card {
    padding:22px;
    border-radius:18px;
    background:#e6ffed;
    border:1px solid #2ecc71;
}
.tab-title {
    font-size:18px;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)


# SIDEBAR – SUMMARY

st.sidebar.title("Experiment Summary")
st.sidebar.write(f"**Total Users:** {len(df):,}")
st.sidebar.write("**Groups:** A (Control), B (Variant)")
st.sidebar.write(f"**CTR A:** {pct(ctr_A)}")
st.sidebar.write(f"**CTR B:** {pct(ctr_B)}")
st.sidebar.write(f"**CVR A:** {pct(cvr_A)}")
st.sidebar.write(f"**CVR B:** {pct(cvr_B)}")
st.sidebar.markdown("---")
st.sidebar.write("**Bayesian P(B > A):**")
st.sidebar.markdown(f"✅ **{bayes_prob*100:.2f}%**")


# HEADER

st.markdown("<div class='big-title'>A/B Testing Experiment Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Evaluating new UX Variant B against Control A on CTR & Conversion</div>", unsafe_allow_html=True)


# KPI ROW

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

with c1:
    st.markdown("<div class='metric-card'>"
                "<div class='metric-label'>CTR – Control A</div>"
                f"<div class='metric-value'>{pct(ctr_A)}</div>"
                "<div class='metric-sub'>Baseline</div>"
                "</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='metric-card'>"
                "<div class='metric-label'>CTR – Variant B</div>"
                f"<div class='metric-value'>{pct(ctr_B)}</div>"
                "<div class='metric-sub'>New UX</div>"
                "</div>", unsafe_allow_html=True)

with c3:
    st.markdown("<div class='metric-card'>"
                "<div class='metric-label'>CTR Uplift</div>"
                f"<div class='metric-value' style='color:#2ecc71;'>{pct(ctr_abs_uplift)}</div>"
                f"<div class='metric-sub'>Rel: {ctr_rel_uplift*100:.1f}%</div>"
                "</div>", unsafe_allow_html=True)

with c4:
    st.markdown("<div class='metric-card'>"
                "<div class='metric-label'>CVR – Control A</div>"
                f"<div class='metric-value'>{pct(cvr_A)}</div>"
                "<div class='metric-sub'>Baseline</div>"
                "</div>", unsafe_allow_html=True)

with c5:
    st.markdown("<div class='metric-card'>"
                "<div class='metric-label'>CVR – Variant B</div>"
                f"<div class='metric-value'>{pct(cvr_B)}</div>"
                "<div class='metric-sub'>New UX</div>"
                "</div>", unsafe_allow_html=True)

with c6:
    st.markdown("<div class='metric-card'>"
                "<div class='metric-label'>CVR Uplift</div>"
                f"<div class='metric-value' style='color:#2ecc71;'>{pct(cvr_abs_uplift)}</div>"
                f"<div class='metric-sub'>Rel: {cvr_rel_uplift*100:.1f}%</div>"
                "</div>", unsafe_allow_html=True)

with c7:
    st.markdown("<div class='metric-card'>"
                "<div class='metric-label'>Bayesian Win Prob (B > A)</div>"
                f"<div class='metric-value' style='color:#1e90ff;'>{bayes_prob*100:.2f}%</div>"
                "<div class='metric-sub'>Beta-Binomial posterior</div>"
                "</div>", unsafe_allow_html=True)

st.write("")


# TABS

tab1, tab2, tab3 = st.tabs(["📊 Overview", "🧠 Bayesian View", "📄 Data"])

# --- TAB 1: OVERVIEW ---
with tab1:
    st.markdown("<div class='tab-title'>CTR & Conversion Comparison</div>", unsafe_allow_html=True)

    # CTR bar
    ctr_df = pd.DataFrame({
        "Group": ["A – Control", "B – Variant"],
        "CTR": [ctr_A, ctr_B]
    })
    fig_ctr = px.bar(ctr_df, x="Group", y="CTR", text=ctr_df["CTR"].map(lambda x: f"{x*100:.2f}%"),
                     color="Group", color_discrete_sequence=["#8888ff", "#2ecc71"])
    fig_ctr.update_traces(textposition="outside")
    fig_ctr.update_yaxes(tickformat=".0%")
    fig_ctr.update_layout(height=350, margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(fig_ctr, use_container_width=True)

    # CVR bar
    cvr_df = pd.DataFrame({
        "Group": ["A – Control", "B – Variant"],
        "CVR": [cvr_A, cvr_B]
    })
    fig_cvr = px.bar(cvr_df, x="Group", y="CVR", text=cvr_df["CVR"].map(lambda x: f"{x*100:.2f}%"),
                     color="Group", color_discrete_sequence=["#8888ff", "#2ecc71"])
    fig_cvr.update_traces(textposition="outside")
    fig_cvr.update_yaxes(tickformat=".0%")
    fig_cvr.update_layout(height=350, margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(fig_cvr, use_container_width=True)

    st.markdown("**Interpretation:** Variant B shows strong absolute and relative lifts in both CTR and CVR versus control, consistent with statistical test results.")

# --- TAB 2: BAYESIAN VIEW ---
with tab2:
    st.markdown("<div class='tab-title'>Bayesian Posterior & Decision</div>", unsafe_allow_html=True)

    # Rebuild posterior curve for visualization
    x = np.linspace(0.02, 0.06, 500)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(x, post_A.pdf(x), label="Control A", lw=2)
    ax.plot(x, post_B.pdf(x), label="Variant B", lw=2, color="red")
    ax.set_xlabel("Conversion rate")
    ax.set_ylabel("Density")
    ax.set_title("Posterior distributions for conversion rate")
    ax.legend()
    st.pyplot(fig)

    st.write(f"- **P(Conversion_B > Conversion_A)** ≈ **{bayes_prob*100:.2f}%**")
    st.write("- Interpretation: Under the Bayesian model, Variant B is almost certainly better than A in true conversion rate.")

    st.markdown("<div class='decision-card'>"
                "<h3>🚀 Recommended Action</h3>"
                "<p>Roll out <b>Variant B</b> to 100% of eligible traffic.</p>"
                "<ul>"
                "<li>CTR uplift: ~{0:.1f}% relative over control.</li>"
                "<li>CVR uplift: ~{1:.1f}% relative over control.</li>"
                "<li>Bayesian confidence that B &gt; A ≈ {2:.2f}%.</li>"
                "</ul>"
                "</div>".format(ctr_rel_uplift*100, cvr_rel_uplift*100, bayes_prob*100),
                unsafe_allow_html=True)

# --- TAB 3: DATA ---
with tab3:
    st.markdown("<div class='tab-title'>Sample of Underlying Data</div>", unsafe_allow_html=True)
    st.dataframe(df.head(20))
    st.write(f"Total rows: {len(df):,}")
