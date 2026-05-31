"""
Synthetic Data Generator for Fast Fashion E-commerce Returns Analysis
Based on real India industry benchmarks (2024-25)

Industry Context:
- Overall return rate: 10.4% of orders
- Fashion return rate: 25-40% depending on category
- Metro vs Tier 2/3 behavior differences
- Size mismatch is #1 reason (53% of returns)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)


# CONFIGURATION - Based on Real India Data


NUM_ORDERS = 50000  # 50K orders for meaningful analysis

# Product categories with realistic distribution
CATEGORIES = {
    'Tops': 0.35,          # T-shirts, shirts, blouses
    'Bottoms': 0.20,       # Jeans, trousers, skirts
    'Dresses': 0.15,       # One-piece dresses
    'Footwear': 0.18,      # Shoes, sandals
    'Accessories': 0.12    # Bags, jewelry, scarves
}

# Return rates by category (from industry data)
RETURN_RATES = {
    'Tops': 0.28,
    'Bottoms': 0.32,
    'Dresses': 0.54,       # Highest return rate
    'Footwear': 0.27,
    'Accessories': 0.12    # Lowest return rate
}

# City tiers and distribution
CITY_TIERS = {
    'Metro': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata'],
    'Tier2': ['Jaipur', 'Lucknow', 'Nagpur', 'Indore', 'Coimbatore', 'Kochi', 'Visakhapatnam'],
    'Tier3': ['Nashik', 'Rajkot', 'Raipur', 'Bhubaneswar', 'Ranchi', 'Mysore', 'Guwahati']
}

TIER_DISTRIBUTION = {
    'Metro': 0.55,         # 55% of orders from metros
    'Tier2': 0.30,
    'Tier3': 0.15
}

# Return reasons based on industry data
RETURN_REASONS = {
    'Size/Fit Issue': 0.53,        # Most common
    'Wrong Product Shipped': 0.15,  # Fulfillment error
    'Quality/Damage': 0.18,
    'Changed Mind': 0.10,           # Bracketing behavior
    'Color Mismatch': 0.04
}

# Warehouses (representing different regions)
WAREHOUSES = ['WH_Mumbai', 'WH_Delhi', 'WH_Bangalore', 'WH_Kolkata', 'WH_Hyderabad']

# Payment methods
PAYMENT_METHODS = {
    'Prepaid': 0.60,
    'COD': 0.40
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_order_id():
    """Generate realistic order IDs"""
    return f"ORD{random.randint(100000, 999999)}"

def get_city_tier(city):
    """Return tier for a given city"""
    for tier, cities in CITY_TIERS.items():
        if city in cities:
            return tier
    return 'Metro'  # Default

def generate_date(start_date, end_date):
    """Generate random date between start and end"""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def should_return(category, tier):
    """Determine if order should be returned based on category and tier"""
    base_rate = RETURN_RATES[category]
    
    # Metro cities have slightly higher return rates (bracketing behavior)
    if tier == 'Metro':
        base_rate *= 1.15
    elif tier == 'Tier3':
        base_rate *= 0.85
    
    return random.random() < base_rate

def get_refund_delay_days(payment_method):
    """
    Generate refund processing time
    Industry benchmark: Should be within 7 days
    15-20% exceed SLA
    """
    if payment_method == 'COD':
        # COD refunds tend to be faster (no payment gateway involved)
        delay = np.random.gamma(shape=2, scale=1.5)
    else:
        # Prepaid refunds take longer
        delay = np.random.gamma(shape=3, scale=2)
    
    # Add occasional outliers (severe delays)
    if random.random() < 0.10:  # 10% get severe delays
        delay += np.random.uniform(10, 30)
    
    return int(delay)


# DATA GENERATION


print("Generating synthetic dataset based on India fast fashion industry data...")
print(f"Total orders: {NUM_ORDERS:,}")

# Initialize data storage
orders_data = []

# Date range: Last 6 months
end_date = datetime(2025, 4, 1)
start_date = end_date - timedelta(days=180)

for i in range(NUM_ORDERS):
    if i % 10000 == 0:
        print(f"Generated {i:,} orders...")
    
    # Generate order details
    order_id = generate_order_id()
    order_date = generate_date(start_date, end_date)
    
    # Select category based on distribution
    category = np.random.choice(list(CATEGORIES.keys()), p=list(CATEGORIES.values()))
    
    # Select city and tier
    tier = np.random.choice(list(TIER_DISTRIBUTION.keys()), p=list(TIER_DISTRIBUTION.values()))
    city = random.choice(CITY_TIERS[tier])
    
    # Order value (in INR)
    base_prices = {
        'Tops': (499, 1999),
        'Bottoms': (799, 2999),
        'Dresses': (999, 3999),
        'Footwear': (699, 3499),
        'Accessories': (299, 1499)
    }
    order_value = random.randint(*base_prices[category])
    
    # Warehouse (usually closest to city)
    warehouse_mapping = {
        'Mumbai': 'WH_Mumbai', 'Delhi': 'WH_Delhi', 'Bangalore': 'WH_Bangalore',
        'Chennai': 'WH_Bangalore', 'Hyderabad': 'WH_Hyderabad', 'Kolkata': 'WH_Kolkata'
    }
    warehouse = warehouse_mapping.get(city, random.choice(WAREHOUSES))
    
    # Payment method
    payment_method = np.random.choice(list(PAYMENT_METHODS.keys()), p=list(PAYMENT_METHODS.values()))
    
    # Delivery status and dates
    dispatch_date = order_date + timedelta(days=random.randint(1, 3))
    
    # Supply chain leakage simulation
    # 5% of orders have issues in transit
    supply_chain_issue = random.random() < 0.05
    
    if supply_chain_issue:
        delivery_status = np.random.choice(['Lost in Transit', 'Damaged in Transit', 'RTO'])
        delivery_date = None
    else:
        # Normal delivery: 3-7 days for metro, 5-10 days for tier 2/3
        if tier == 'Metro':
            delivery_days = random.randint(3, 7)
        elif tier == 'Tier2':
            delivery_days = random.randint(4, 9)
        else:
            delivery_days = random.randint(6, 12)
        
        delivery_date = dispatch_date + timedelta(days=delivery_days)
        delivery_status = 'Delivered'
    
    # Determine if order will be returned
    is_returned = should_return(category, tier) if delivery_status == 'Delivered' else False
    
    if is_returned:
        # Generate return details
        return_initiated_date = delivery_date + timedelta(days=random.randint(1, 15))
        return_reason = np.random.choice(list(RETURN_REASONS.keys()), p=list(RETURN_REASONS.values()))
        
        # Refund processing
        refund_delay = get_refund_delay_days(payment_method)
        refund_completed_date = return_initiated_date + timedelta(days=refund_delay)
        refund_status = 'Completed' if refund_delay <= 15 else 'Pending'
        sla_breach = refund_delay > 7
        
    else:
        return_initiated_date = None
        return_reason = None
        refund_completed_date = None
        refund_status = None
        sla_breach = None
    
    # Append to dataset
    orders_data.append({
        'order_id': order_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'category': category,
        'order_value': order_value,
        'city': city,
        'city_tier': tier,
        'warehouse': warehouse,
        'payment_method': payment_method,
        'dispatch_date': dispatch_date.strftime('%Y-%m-%d') if dispatch_date else None,
        'delivery_date': delivery_date.strftime('%Y-%m-%d') if delivery_date else None,
        'delivery_status': delivery_status,
        'is_returned': is_returned,
        'return_initiated_date': return_initiated_date.strftime('%Y-%m-%d') if return_initiated_date else None,
        'return_reason': return_reason,
        'refund_completed_date': refund_completed_date.strftime('%Y-%m-%d') if refund_completed_date else None,
        'refund_status': refund_status,
        'refund_delay_days': refund_delay if is_returned else None,
        'sla_breach': sla_breach
    })

# Create DataFrame
df_orders = pd.DataFrame(orders_data)

print(f"\nDataset generated successfully!")
print(f"Total orders: {len(df_orders):,}")
print(f"Total returns: {df_orders['is_returned'].sum():,} ({df_orders['is_returned'].mean()*100:.1f}%)")
print(f"Supply chain issues: {(df_orders['delivery_status'] != 'Delivered').sum():,}")

# Save to CSV
output_path = 'data/raw/ecommerce_orders_synthetic.csv'
df_orders.to_csv(output_path, index=False)
print(f"\nSaved to: {output_path}")


# GENERATE COMPLAINTS DATASET


print("\n" + "="*60)
print("Generating customer complaints dataset...")

complaints_data = []
complaint_templates = {
    'wrong_product': [
        "Ordered size M, received size L",
        "Wrong color delivered - ordered blue, got black",
        "Completely different item in the package",
        "Received used/worn product instead of new"
    ],
    'refund_delay': [
        "Return initiated 15 days ago, still no refund",
        "Customer support not responding about refund status",
        "Money stuck for 3 weeks, very disappointed",
        "Refund promised in 7 days, been waiting for a month"
    ],
    'quality_damage': [
        "Product arrived torn and damaged",
        "Poor quality material, not as shown in photos",
        "Stitching came apart after one wear",
        "Fabric is cheap quality, not worth the price"
    ],
    'size_fit': [
        "Size chart is completely wrong",
        "Fit is terrible, runs very small",
        "Ordered usual size but doesn't fit at all",
        "Size inconsistency across different products"
    ]
}

for i in range(300):  # Generate 300 complaint samples
    complaint_type = random.choice(list(complaint_templates.keys()))
    complaint_text = random.choice(complaint_templates[complaint_type])
    complaint_date = generate_date(start_date, end_date)
    
    # Sentiment score (1-10, where 1 is most negative)
    sentiment_scores = {
        'wrong_product': (2, 4),
        'refund_delay': (1, 3),
        'quality_damage': (2, 5),
        'size_fit': (3, 6)
    }
    sentiment = random.randint(*sentiment_scores[complaint_type])
    
    complaints_data.append({
        'complaint_id': f"CMPL{i+1:04d}",
        'complaint_date': complaint_date.strftime('%Y-%m-%d'),
        'complaint_type': complaint_type,
        'complaint_text': complaint_text,
        'sentiment_score': sentiment,
        'escalated': random.random() < 0.25  # 25% get escalated
    })

df_complaints = pd.DataFrame(complaints_data)
complaints_path = 'data/raw/complaints_aggregated.csv'
df_complaints.to_csv(complaints_path, index=False)
print(f"Complaints dataset saved to: {complaints_path}")
print(f"Total complaints: {len(df_complaints)}")

print("\n" + "="*60)
print("✅ ALL DATASETS GENERATED SUCCESSFULLY!")
print("\nNext steps:")
print("1. Review the generated CSVs in data/raw/")
print("2. Start with notebook: 01_data_cleaning.ipynb")
print("3. Run the analyze.py now")
