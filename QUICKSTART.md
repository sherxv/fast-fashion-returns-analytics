# ⚡ QUICKSTART GUIDE

## Run the Complete Analysis in 2 Steps

### Step 1: Generate Data
```bash
cd scripts
python generate_synthetic_data.py
```

### Step 2: Run Analysis
```bash
python module_01_data_cleaning.py
python run_complete_analysis.py
```

## ✅ That's It!

You'll now have:
- ✅ Cleaned datasets in `data/processed/`
- ✅ Visualizations in `visuals/`
- ✅ Complete analysis printed in terminal

## 📊 What You Get

**Key Metrics:**
- 31.3% overall return rate
- 55.4% return rate for Dresses (highest)
- 24% of refunds breach 7-day SLA
- 4.9% supply chain failure rate
- 3.3/10 average customer sentiment

**Files Generated:**
1. `data/processed/orders_cleaned.csv` - All orders with features
2. `data/processed/returns_only.csv` - Just returns for analysis
3. `data/processed/delivered_no_returns.csv` - Successful deliveries
4. `visuals/return_rate_by_category.png`
5. `visuals/refund_delay_distribution.png`
6. `visuals/sentiment_distribution.png`

## 🎯 For GitHub

1. Update README.md with your name/email
2. Initialize git:
```bash
git init
git add .
git commit -m "Initial commit: Fast fashion analytics project"
```

3. Create repo on GitHub
4. Push:
```bash
git remote add origin https://github.com/YOUR-USERNAME/fast-fashion-returns-analytics.git
git branch -M main
git push -u origin main
```

## 📝 For LittleBox Application

**Your pitch:**
"I analyzed 50K orders in India's fast fashion e-commerce space, identifying that:
- Dresses have 55% return rate (vs 31% average)
- Refund delays (24% breach SLA) are the #1 complaint driver
- WH_Bangalore has 15.5% fulfillment error rate

Built with Python, SQL, data visualization. Full project on GitHub."

## 🔧 Optional: Jupyter Notebooks

The `notebooks/` folder has detailed interactive analysis if you want to explore further or customize visualizations.

To use:
```bash
pip install jupyter
jupyter notebook
```

Then open notebooks in order: 01, 02, 03, 04, 05, 06.

---

**Questions?** Check SETUP_GUIDE.md for detailed instructions.
