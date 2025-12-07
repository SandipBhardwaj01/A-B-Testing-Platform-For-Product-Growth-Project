# 🧪 A/B Testing Platform – UX Experiment (Control vs Variant)

This project simulates and analyzes a large-scale **A/B test on 200,000 users** to evaluate whether a new UX variant (B) performs better than the existing design (A) in terms of **Click-Through Rate (CTR)** and **Conversion Rate (CVR)**.

It combines:

- ✅ Frequentist A/B testing (Z-test, p-values, uplift)
- ✅ Bayesian A/B testing (Beta-Binomial posterior, probability of winning)
- ✅ An interactive **“Google-style” experiment dashboard** built in Streamlit + Plotly

---

## 🎯 Business Question

> *“Should we roll out the new UX (Variant B) to all users?”*  
We answer this using both **frequentist** and **Bayesian** methods.

---

## 📂 Project Structure

```bash
ab-testing-platform/
│
├── ab_test_data.csv              # Simulated A/B dataset (200k users)
├── notebooks/
│   ├── 01_data_generation.ipynb  # Data simulation + base EDA
│   ├── 02_frequentist_test.ipynb # CTR/CVR Z-tests, p-values, uplift
│   └── 03_bayesian_test.ipynb    # Beta posterior, sampling, plots
│
├── dashboard/
│   ├── ab_google_dashboard.py    # Streamlit + Plotly experiment UI
│   └── beta_posterior_distribution.png
│
└── README.md

📊 Key Results
1. Metric Uplift
Metric	Control A	Variant B	Absolute Uplift	Relative Uplift
CTR	10.83%	14.05%	+3.23 pp	+29.8%
CVR	3.28%	3.91%	+0.63 pp	+19.2%
2. Frequentist Test (Z-test on proportions)

CTR p-value: ≈ 6.59 × 10⁻¹⁰⁶

CVR p-value: ≈ 4.04 × 10⁻¹⁴

➡️ Both well below 0.05 → Statistically significant improvement.

3. Bayesian View

Modeled conversion rate with Beta-Binomial posterior:

Posterior_A ~ Beta(1 + conv_A, 1 + non_conv_A)

Posterior_B ~ Beta(1 + conv_B, 1 + non_conv_B)

After 200,000 samples:

P(Conversion_B > Conversion_A) ≈ 100%

➡️ Under the Bayesian model, Variant B is almost certainly better than A.

🧠 Final Recommendation

Roll out Variant B to 100% of eligible traffic.
Expect ~+29.8% CTR uplift and +19.2% CVR uplift, with ~100% Bayesian confidence.

🖥 Dashboard Preview

Built with Streamlit + Plotly:

KPI strip: CTR/ CVR for A & B + uplift + Bayesian win probability

Bar charts: CTR and CVR comparisons

Bayesian tab: posterior curve visualization + decision card

Data tab: sample of underlying A/B dataset

(Screenshot here → ab_google_dashboard.png)

🛠 Tech Stack

Python (Pandas, NumPy)

statsmodels (frequentist Z-tests)

SciPy (Beta distribution)

Streamlit + Plotly (interactive dashboard)

Bayesian A/B testing concepts




