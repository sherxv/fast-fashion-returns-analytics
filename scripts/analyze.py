"""
Fast Fashion Returns Analysis
Complete data cleaning and analysis pipeline
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Setup
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
os.makedirs('../data/processed', exist_ok=True)
os.makedirs('../visuals', exist_ok=True)

print("="*70)
print("FAST FASHION RETURNS ANALYSIS")
print("="*70)

# ============================================
# STEP 1: LOAD & CLEAN DATA
# ============================================
print("\n[1/5] Loading data...")
df = pd.read_csv('data/raw/ecommerce_orders_synthetic.csv')
df_complaints = pd.read_csv('data/raw/complaints_aggregated.csv')
print(f"✅ Loaded {len(df):,} orders, {len(df_complaints):,} complaints")

print("\n[2/5] Cleaning data...")
# Convert dates
date_cols = ['order_date', 'dispatch_date', 'delivery_date', 
             'return_initiated_date', 'refund_completed_date']
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')

df_complaints['complaint_date'] = pd.to_datetime(df_complaints['complaint_date'])

# Convert booleans
df['is_returned'] = df['is_returned'].astype(bool)
df['sla_breach'] = df['sla_breach'].astype('boolean')

# Create derived features
df['total_delivery_days'] = (df['delivery_date'] - df['order_date']).dt.days
df['order_month'] = df['order_date'].dt.month_name()
df['is_metro'] = df['city_tier'] == 'Metro'
df['supply_chain_failure'] = ~df['delivery_status'].isin(['Delivered'])

print(f"✅ Data cleaned - {len(df):,} orders ready for analysis")

# Save cleaned data
df.to_csv('data/processed/orders_cleaned.csv', index=False)
df_returns = df[df['is_returned']].copy()
df_returns.to_csv('data/processed/returns_only.csv', index=False)
print(f"✅ Saved processed datasets")

# ============================================
# STEP 2: RETURNS ANALYSIS
# ============================================
print("\n[3/5] Analyzing returns...")

# Overall stats
total_orders = len(df)
total_returns = df['is_returned'].sum()
return_rate = (total_returns / total_orders * 100)

print(f"\n{'='*60}")
print("RETURNS OVERVIEW")
print(f"{'='*60}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Returns: {total_returns:,} ({return_rate:.1f}%)")
print(f"Date Range: {df['order_date'].min().strftime('%Y-%m-%d')} to {df['order_date'].max().strftime('%Y-%m-%d')}")

# Return rate by category
# SQL equivalent: SELECT category, COUNT(*), AVG(is_returned) FROM orders GROUP BY category
category_returns = df.groupby('category')['is_returned'].agg(['sum', 'count', 'mean'])
category_returns['return_rate_%'] = category_returns['mean'] * 100
category_returns = category_returns.sort_values('return_rate_%', ascending=False)

print(f"\nReturn Rate by Category:")
for cat in category_returns.index:
    rate = category_returns.loc[cat, 'return_rate_%']
    count = category_returns.loc[cat, 'sum']
    print(f"  {cat}: {rate:.1f}% ({count:,} returns)")

# Return rate by city tier
tier_returns = df.groupby('city_tier')['is_returned'].agg(['sum', 'mean'])
tier_returns['return_rate_%'] = tier_returns['mean'] * 100

print(f"\nReturn Rate by City Tier:")
for tier in tier_returns.index:
    rate = tier_returns.loc[tier, 'return_rate_%']
    print(f"  {tier}: {rate:.1f}%")

# Top return reasons
return_reasons = df_returns['return_reason'].value_counts()
print(f"\nTop Return Reasons:")
for reason, count in return_reasons.head(3).items():
    pct = (count / len(df_returns) * 100)
    print(f"  {reason}: {count:,} ({pct:.1f}%)")

# Chart: Return rates by category
plt.figure(figsize=(10, 6))
category_returns['return_rate_%'].plot(kind='barh', color='coral')
plt.xlabel('Return Rate (%)', fontsize=12)
plt.ylabel('Category', fontsize=12)
plt.title('Return Rate by Product Category', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('../visuals/return_rate_by_category.png', dpi=300, bbox_inches='tight')
plt.close()
print("\n✅ Chart saved: return_rate_by_category.png")

# ============================================
# STEP 3: REFUND ANALYSIS
# ============================================
print("\n[4/5] Analyzing refunds...")

avg_refund_days = df_returns['refund_delay_days'].mean()
sla_breaches = df_returns['sla_breach'].sum()
sla_breach_rate = (sla_breaches / len(df_returns) * 100)

print(f"\nRefund Performance:")
print(f"  Average processing time: {avg_refund_days:.1f} days")
print(f"  SLA breaches (>7 days): {sla_breaches:,} ({sla_breach_rate:.1f}%)")

# By payment method
payment_refund = df[df['is_returned']].groupby('payment_method')['refund_delay_days'].mean()
print(f"\nRefund Time by Payment Method:")
for method, days in payment_refund.items():
    print(f"  {method}: {days:.1f} days")

# Chart: Refund delay distribution
plt.figure(figsize=(12, 6))
plt.hist(df_returns['refund_delay_days'], bins=50, edgecolor='black', alpha=0.7, color='skyblue')
plt.axvline(7, color='red', linestyle='--', linewidth=2, label='SLA (7 days)')
plt.axvline(avg_refund_days, color='green', linestyle='--', linewidth=2, 
            label=f'Average ({avg_refund_days:.1f} days)')
plt.xlabel('Refund Processing Days', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Refund Delay Distribution', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('../visuals/refund_delay_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Chart saved: refund_delay_distribution.png")

# ============================================
# STEP 4: SUPPLY CHAIN & SENTIMENT
# ============================================
print("\n[5/5] Additional analysis...")

# Supply chain failures
failed_deliveries = df['supply_chain_failure'].sum()
failure_rate = (failed_deliveries / total_orders * 100)
print(f"\nSupply Chain:")
print(f"  Failed deliveries: {failed_deliveries:,} ({failure_rate:.1f}%)")

# Sentiment analysis
avg_sentiment = df_complaints['sentiment_score'].mean()
escalations = df_complaints['escalated'].sum()
escalation_rate = (escalations / len(df_complaints) * 100)

print(f"\nCustomer Sentiment:")
print(f"  Average score: {avg_sentiment:.1f} / 10")
print(f"  Escalated complaints: {escalations} ({escalation_rate:.1f}%)")

# Chart: Sentiment distribution
plt.figure(figsize=(12, 6))
plt.hist(df_complaints['sentiment_score'], bins=10, edgecolor='black', alpha=0.7, color='coral')
plt.axvline(avg_sentiment, color='red', linestyle='--', linewidth=2, 
            label=f'Average ({avg_sentiment:.1f})')
plt.xlabel('Sentiment Score (1=Negative, 10=Positive)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Customer Complaint Sentiment', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('../visuals/sentiment_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Chart saved: sentiment_distribution.png")

# ============================================
# SUMMARY
# ============================================
print("\n" + "="*70)
print("ANALYSIS COMPLETE - KEY FINDINGS")
print("="*70)

print(f"\n📊 RETURNS")
print(f"  • Overall rate: {return_rate:.1f}%")
print(f"  • Highest category: {category_returns.index[0]} ({category_returns.iloc[0]['return_rate_%']:.1f}%)")
print(f"  • Top reason: {return_reasons.index[0]} ({(return_reasons.iloc[0]/len(df_returns)*100):.1f}%)")
print(f"  • Metro vs Tier 3: {(tier_returns.loc['Metro', 'return_rate_%'] - tier_returns.loc['Tier3', 'return_rate_%']):.1f}% gap")

print(f"\n⏱️ REFUNDS")
print(f"  • Average time: {avg_refund_days:.1f} days")
print(f"  • SLA breaches: {sla_breach_rate:.1f}%")
print(f"  • COD vs Prepaid: {payment_refund['COD']:.1f} vs {payment_refund['Prepaid']:.1f} days")

print(f"\n🚚 SUPPLY CHAIN")
print(f"  • Failure rate: {failure_rate:.1f}%")

print(f"\n💬 SENTIMENT")
print(f"  • Average score: {avg_sentiment:.1f} / 10")
print(f"  • Escalation rate: {escalation_rate:.1f}%")

print("\n" + "="*70)
print("✅ Results saved to:")
print("  • data/processed/ (cleaned CSVs)")
print("  • visuals/ (3 charts)")
print("="*70)