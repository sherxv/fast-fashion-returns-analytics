# Fast Fashion Returns & Supply Chain Analytics

## 📊 Project Overview

This project analyzes returns, refund delays, and supply chain leakage patterns in India's fast fashion e-commerce segment. Using real industry benchmarks and publicly available data, the analysis identifies critical pain points in the order-to-delivery lifecycle that impact customer satisfaction and operational efficiency.

**Key Focus Areas:**
- Returns funnel analysis (by category, city tier, reason codes)
- Wrong product/mispacking rate identification
- Refund delay tracking and SLA breach analysis
- Supply chain leakage point detection
- Customer complaint sentiment scoring

---

## 🎯 Industry Context

### India Fast Fashion E-commerce (2024-25 Data)

**Market Size:** USD 60.12 billion (2024)
- E-commerce fashion revenue: ~USD 20 billion
- 850M internet users, 290M with 5G
- 180M middle-class households averaging ₹2,500/month on fashion

**The Returns Crisis:**
- **Overall return rate:** 10.4% of all orders (FY23, up from 9.8% in FY22)
- **Fashion-specific returns:** 25-40% depending on category
- **Online apparel return rate:** 24.4% in India (vs 16.5% global average)
- **Most returned category:** Clothing (50% of respondents reported returning clothing in 2024)

**Key Reasons for Returns:**
1. **Size/fit issues** – 53% of all apparel returns globally
2. **Wrong product shipped** – Warehousing/fulfillment errors
3. **Quality/damage issues** – Manufacturing or handling defects
4. **Customer changed mind** – "Bracketing" behavior (buying multiple sizes)

**Cost Impact:**
- Return logistics cost: Up to 65% of item's original price
- Environmental footprint: Reverse shipping emissions + textile waste

---

## 📁 Datasets Used

### Primary Datasets (Kaggle)

1. **Fast Fashion Supply Chain Dataset**
   - Source: https://www.kaggle.com/datasets/harshbhatt02/fast-fashion-supply-chain
   - Contains: Cost optimization, trend patterns, logistics data
   
2. **E-Commerce Orders Dataset**
   - Source: https://www.kaggle.com/datasets/bytadit/ecommerce-order-dataset
   - Contains: Order lifecycle, delivery status, timestamps

3. **Synthetic E-Commerce Returns Analysis**
   - Source: https://www.kaggle.com/datasets/sayalikhot21/synthetic-dataset-for-e-commerce-return-analysis
   - Contains: Return reasons, categories, refund status

4. **Fashion E-commerce Data (India-specific)**
   - Source: https://www.kaggle.com/datasets/kuchhbhi/fashion-ecommerce-data
   - Contains: Indian fashion product listings, pricing, categories

### Supplementary Data Sources

5. **Industry Complaint Patterns** (manually aggregated)
   - Source: Public social media observations across Indian fast fashion platforms
   - Method: 30 complaint samples categorized into: wrong product, refund delay, damaged item, size mismatch
   - File: `data/raw/complaints_aggregated.csv`

---

## 🔍 Analysis Module

### Module 1: Returns Funnel Analysis
**Goal:** Identify which product categories and city tiers have highest return rates

**Key Metrics:**
- Return rate by category (tops, bottoms, dresses, footwear)
- Return rate by city tier (Metro vs Tier 2 vs Tier 3)
- Return reason breakdown

**Visualization:** Funnel chart showing order → delivery → return → refund stages

---

### Module 2: Mispacking & Wrong Product Rate
**Goal:** Detect fulfillment errors causing "wrong item shipped" complaints

**Key Metrics:**
- Mispack rate by warehouse/region
- Wrong size vs wrong item breakdown
- Impact on customer satisfaction score

**Visualization:** Heatmap of error rates by warehouse + bar chart of error types

---

### Module 3: Refund Delay Analysis
**Goal:** Track refund processing times and flag SLA breaches

**Key Metrics:**
- Average days from return initiation → refund completion
- % of refunds exceeding 7-day SLA
- Delay patterns by payment method (COD vs prepaid)

**Visualization:** Time-series showing refund processing timeline + breach flags

---

### Module 4: Supply Chain Leakage Analysis
**Goal:** Identify where items "disappear" between stages (dispatch → transit → last-mile → delivered)

**Key Metrics:**
- Dropout rate by stage
- Lost/damaged in transit %
- RTO (Return to Origin) rate

**Visualization:** Sankey diagram showing flow + dropout points

---

### Module 5: Complaint Sentiment Scoring
**Goal:** Quantify severity of customer complaints over time

**Key Metrics:**
- Sentiment score (1-10 scale)
- Complaint category trends
- Escalation frequency

**Visualization:** Trend line + word cloud of top complaint keywords

---

## 🛠️ Tech Stack

- **Python 3.10+**: Pandas, NumPy, Matplotlib, Seaborn, Plotly
- **SQL**: PostgreSQL/SQLite for querying
- **Jupyter Notebook**: Main analysis environment
- **Libraries**: 
  - `pandas`, `numpy` – Data manipulation
  - `matplotlib`, `seaborn`, `plotly` – Visualization
  - `sqlalchemy` – Database connectivity
  - `textblob` or `vaderSentiment` – Sentiment analysis

---

## 📂 Project Structure

```
fast-fashion-returns-analytics/
├── README.md                          ← You are here
├── data/
│   ├── raw/                           ← Original datasets (Kaggle CSVs)
│   │   ├── ecommerce_orders_synthetic.csv
│   │   └── complaints_aggregated.csv
│   └── processed/                     ← Cleaned, merged datasets
│       ├── delivered_no_returns.csv 
│       ├── orders_cleaned.csv
|       └── returns_only.csv
├── notebooks/
│   └── analysis.ipynb 
├── scripts/
│   ├──  generate_data.py               ← Script to create India-flavored datasets
│   └── analyze.py
├── visuals/                           ← Exported charts (PNG/SVG)
└── requirements.txt                   ← Python dependencies
```

---

## 🚀 How to Use This Project

### 1. Clone the Repository
```bash
git clone https://github.com/sherxv/fast-fashion-returns-analytics.git
cd fast-fashion-returns-analytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download Datasets
- Go to the Kaggle links listed above
- Download CSVs to `data/raw/`
- Run the synthetic data generator (if using custom data):
  ```bash
  python scripts/generate_data.py
  ```

### 4. Run Notebooks in Order
Start with `01_data_cleaning.ipynb` and progress sequentially through all modules.

### 5. Generate Insights
Each notebook outputs:
- Key metrics (printed summaries)
- Visualizations (saved to `visuals/`)
- Business recommendations

---

## 📈 Key Findings (Preview)

> **Note:** This section will be populated after completing the analysis.

Expected insights:
- Clothing returns are 3x higher than accessories
- Metro cities show higher bracketing behavior (multiple-size purchases)
- 15-20% of refunds exceed the 7-day SLA
- Last-mile delivery accounts for 40% of supply chain leakage
- "Wrong size" complaints spike during sale periods

---

## 🎓 Learning Outcomes

This project demonstrates:
- **Data cleaning & feature engineering** for messy e-commerce data
- **SQL proficiency** for metric extraction and aggregation
- **Statistical analysis** of return patterns and trends
- **Visualization design** for business stakeholders
- **Actionable insights** for operations and growth teams

---

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome! Open an issue or submit a pull request.

---

## 📧 Contact

Shruti Priya  
Data Analytics Enthusiast | Aspiring Growth Analyst  
📧 sherxv7@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/shrutipriya1375/) | [GitHub](https://github.com/sherxv)

---

## 📝 License

This project is open-source under the MIT License.

---

## Acknowledgments

- Kaggle community for datasets
- Industry reports from Statista, Fibre2Fashion, Ken Research, Unicommerce
- Inspiration from real-world e-commerce challenges in India's fast fashion sector
