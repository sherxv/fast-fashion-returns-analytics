-- ============================================
-- MASTER SQL QUERIES FILE
-- Fast Fashion Returns & Supply Chain Analytics
-- ============================================
-- This file contains all SQL queries used in the analysis module
-- Database: PostgreSQL (can be adapted for MySQL, SQLite, etc.)
-- ============================================

-- ====================
-- MODULE 2: RETURNS FUNNEL ANALYSIS
-- ====================

-- Query 2.1: Return rate by category
SELECT 
    category,
    COUNT(*) as total_orders,
    SUM(CASE WHEN is_returned = TRUE THEN 1 ELSE 0 END) as returns,
    ROUND(AVG(CASE WHEN is_returned = TRUE THEN 1.0 ELSE 0.0 END) * 100, 2) as return_rate_pct
FROM orders
GROUP BY category
ORDER BY return_rate_pct DESC;

-- Query 2.2: Return rate by city tier
SELECT 
    city_tier,
    COUNT(*) as total_orders,
    SUM(CASE WHEN is_returned = TRUE THEN 1 ELSE 0 END) as returns,
    ROUND(AVG(CASE WHEN is_returned = TRUE THEN 1.0 ELSE 0.0 END) * 100, 2) as return_rate_pct
FROM orders
GROUP BY city_tier
ORDER BY return_rate_pct DESC;

-- Query 2.3: Top return reasons
SELECT 
    return_reason,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM orders
WHERE is_returned = TRUE
GROUP BY return_reason
ORDER BY count DESC;

-- ====================
-- MODULE 3: FULFILLMENT ERROR ANALYSIS
-- ====================

-- Query 3.1: Overall fulfillment error rate
SELECT 
    COUNT(*) as total_returns,
    SUM(CASE WHEN return_reason = 'Wrong Product Shipped' THEN 1 ELSE 0 END) as fulfillment_errors,
    ROUND(SUM(CASE WHEN return_reason = 'Wrong Product Shipped' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) as error_rate_pct
FROM orders
WHERE is_returned = TRUE;

-- Query 3.2: Error rate by warehouse
SELECT 
    warehouse,
    COUNT(*) as total_returns,
    SUM(CASE WHEN return_reason = 'Wrong Product Shipped' THEN 1 ELSE 0 END) as errors,
    ROUND(SUM(CASE WHEN return_reason = 'Wrong Product Shipped' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) as error_rate_pct
FROM orders
WHERE is_returned = TRUE
GROUP BY warehouse
ORDER BY error_rate_pct DESC;

-- ====================
-- MODULE 4: REFUND DELAY ANALYSIS
-- ====================

-- Query 4.1: Overall refund performance
SELECT 
    COUNT(*) as total_returns,
    AVG(refund_delay_days) as avg_delay_days,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY refund_delay_days) as median_delay_days,
    SUM(CASE WHEN sla_breach = TRUE THEN 1 ELSE 0 END) as sla_breaches,
    ROUND(AVG(CASE WHEN sla_breach = TRUE THEN 1.0 ELSE 0.0 END) * 100, 2) as breach_rate_pct
FROM orders
WHERE is_returned = TRUE;

-- Query 4.2: Refund performance by payment method
SELECT 
    payment_method,
    COUNT(*) as returns,
    ROUND(AVG(refund_delay_days), 2) as avg_delay,
    SUM(CASE WHEN sla_breach = TRUE THEN 1 ELSE 0 END) as breaches,
    ROUND(AVG(CASE WHEN sla_breach = TRUE THEN 1.0 ELSE 0.0 END) * 100, 2) as breach_rate_pct
FROM orders
WHERE is_returned = TRUE
GROUP BY payment_method;

-- ====================
-- MODULE 5: SUPPLY CHAIN LEAKAGE
-- ====================

-- Query 5.1: Overall supply chain performance
SELECT 
    COUNT(*) as total_orders,
    SUM(CASE WHEN delivery_status = 'Delivered' THEN 1 ELSE 0 END) as successful,
    SUM(CASE WHEN delivery_status != 'Delivered' THEN 1 ELSE 0 END) as failed,
    ROUND(SUM(CASE WHEN delivery_status != 'Delivered' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) as failure_rate_pct
FROM orders;

-- Query 5.2: Failure rate by city tier
SELECT 
    city_tier,
    COUNT(*) as total_orders,
    SUM(CASE WHEN delivery_status != 'Delivered' THEN 1 ELSE 0 END) as failures,
    ROUND(SUM(CASE WHEN delivery_status != 'Delivered' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) as failure_rate_pct
FROM orders
GROUP BY city_tier
ORDER BY failure_rate_pct DESC;

-- ====================
-- MODULE 6: SENTIMENT ANALYSIS
-- ====================

-- Query 6.1: Overall sentiment metrics
SELECT 
    COUNT(*) as total_complaints,
    ROUND(AVG(sentiment_score), 2) as avg_sentiment,
    SUM(CASE WHEN escalated = TRUE THEN 1 ELSE 0 END) as escalations,
    ROUND(AVG(CASE WHEN escalated = TRUE THEN 1.0 ELSE 0.0 END) * 100, 2) as escalation_rate_pct
FROM complaints;

-- Query 6.2: Sentiment by complaint type
SELECT 
    complaint_type,
    COUNT(*) as count,
    ROUND(AVG(sentiment_score), 2) as avg_sentiment,
    SUM(CASE WHEN escalated = TRUE THEN 1 ELSE 0 END) as escalations
FROM complaints
GROUP BY complaint_type
ORDER BY avg_sentiment;

-- ====================
-- BONUS: ADVANCED ANALYTICS QUERIES
-- ====================

-- Executive Dashboard Query: Overall KPIs
SELECT 
    'Orders' as metric,
    COUNT(*) as value,
    NULL as percentage
FROM orders

UNION ALL

SELECT 
    'Delivered',
    SUM(CASE WHEN delivery_status = 'Delivered' THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN delivery_status = 'Delivered' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2)
FROM orders

UNION ALL

SELECT 
    'Returns',
    SUM(CASE WHEN is_returned = TRUE THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN is_returned = TRUE THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2)
FROM orders

UNION ALL

SELECT 
    'SLA Breaches',
    SUM(CASE WHEN sla_breach = TRUE THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN sla_breach = TRUE THEN 1.0 ELSE 0.0 END) / (SELECT COUNT(*) FROM orders WHERE is_returned = TRUE) * 100, 2)
FROM orders;

-- Cohort Analysis: Return rate by month
SELECT 
    DATE_TRUNC('month', order_date) as order_month,
    COUNT(*) as total_orders,
    SUM(CASE WHEN is_returned = TRUE THEN 1 ELSE 0 END) as returns,
    ROUND(AVG(CASE WHEN is_returned = TRUE THEN 1.0 ELSE 0.0 END) * 100, 2) as return_rate_pct,
    ROUND(AVG(CASE WHEN sla_breach = TRUE THEN 1.0 ELSE 0.0 END) * 100, 2) as sla_breach_pct
FROM orders
GROUP BY order_month
ORDER BY order_month;

-- ============================================
-- END OF QUERIES
-- ============================================
