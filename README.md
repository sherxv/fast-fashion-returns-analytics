# Fast Fashion Returns & Supply Chain Analytics

Analyzing returns, refund delays, and supply chain issues in India's fast fashion e-commerce space.

Built this after noticing a pattern of customer complaints about wrong products and delayed refunds
in the Indian fast fashion market — wanted to understand the scale of the problem through data.

---

## Industry Context

India's online fashion return rate sits at **24.4%** — significantly higher than the global average
of 16.5%. Key drivers:

- Size/fit issues account for 53% of returns globally
- Wrong product shipped — fulfillment/warehouse errors
- Quality or damage on arrival
- Bracketing behavior (buying multiple sizes, keeping one)

Return logistics can cost up to **65% of the item's original price**, making this a major
operational and profitability problem for fast fashion platforms.

---

## Key Findings

- **31% overall return rate** — Dresses highest at 55%, Accessories lowest at 12%
- **Size/fit issues** drive 53% of all returns
- **24% of refunds breach the 7-day SLA** — prepaid orders take ~3 days longer than COD
- **5% of orders fail to deliver** — split across lost in transit, damaged, and RTO
- **Refund delays** score most negatively in customer sentiment (1.9/10)
- Metro cities return ~8% more than Tier 3 — likely due to bracketing behavior

---

## Data

Synthetically generated dataset of **50,000 orders** modelled on real Indian e-commerce patterns:

- Return rates by category based on Unicommerce & Fibre2Fashion 2024 reports
- City tier distribution: 55% Metro, 30% Tier 2, 15% Tier 3
- COD vs Prepaid split: 40/60
- 300 customer complaints aggregated from public social media observations,
  categorized into: wrong product, refund delay, damaged item, size mismatch

---
## Project Structure

```
├── data/
│   ├── raw/            # Synthetic orders + complaints dataset
│   └── processed/      # Cleaned datasets (output of analyze.py)
├── notebooks/
│   └── analysis.ipynb  # Exploratory analysis with visualizations
├── scripts/
│   ├── generate_data.py  # Generates the synthetic dataset
│   └── analyze.py        # Data cleaning + full analysis pipeline
├── visuals/            # Output charts (PNG)
└── requirements.txt
```
---

## How to Run

```bash
pip install -r requirements.txt

cd scripts
python generate_data.py
python analyze.py
```

Charts saved to `visuals/`, cleaned data to `data/processed/`.

To explore interactively, open `notebooks/analysis.ipynb` in Jupyter.

---

## Tech Stack

Python, Pandas, NumPy, Matplotlib, Seaborn

---

## Next Steps

- [ ] Return probability prediction model (logistic regression)
- [ ] Seasonal analysis — sale periods vs regular demand
- [ ] Interactive dashboard with Streamlit

---

*Shruti Priya — [LinkedIn](https://www.linkedin.com/in/shrutipriya1375/) · [GitHub](https://github.com/sherxv)*