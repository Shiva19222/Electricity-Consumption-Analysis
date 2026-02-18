-- SQL Queries for Electricity Consumption Analysis
-- Updated for Original Dataset Structure
-- Optimized for Tableau Integration

-- ============================================
-- BASIC DATA EXPLORATION QUERIES
-- ============================================

-- 1. Dataset Overview
SELECT 
    'Dataset Overview' as metric,
    COUNT(*) as total_records,
    COUNT(DISTINCT state_id) as unique_states,
    COUNT(DISTINCT DATE(consumption_date)) as unique_dates,
    MIN(consumption_date) as start_date,
    MAX(consumption_date) as end_date,
    ROUND(SUM(usage_value), 2) as total_consumption
FROM consumption;

-- 2. Regional Distribution
SELECT 
    s.region,
    COUNT(DISTINCT s.state_name) as number_of_states,
    COUNT(*) as total_records,
    ROUND(SUM(c.usage_value), 2) as total_consumption,
    ROUND(AVG(c.usage_value), 2) as average_consumption,
    ROUND(MAX(c.usage_value), 2) as peak_consumption,
    ROUND(MIN(c.usage_value), 2) as minimum_consumption
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.region
ORDER BY total_consumption DESC;

-- ============================================
-- YEAR-OVER-YEAR COMPARISON (2019 vs 2020)
-- ============================================

-- 3. Year-over-Year Comparison by State
SELECT 
    s.state_name,
    s.region,
    ROUND(SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_value END), 2) as consumption_2019,
    ROUND(SUM(CASE WHEN YEAR(c.consumption_date) = 2020 THEN c.usage_value END), 2) as consumption_2020,
    ROUND(
        (SUM(CASE WHEN YEAR(c.consumption_date) = 2020 THEN c.usage_value END) - 
         SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_value END)) / 
        SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_value END) * 100, 2
    ) as yoy_change_percentage,
    ROUND(AVG(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_value END), 2) as avg_2019,
    ROUND(AVG(CASE WHEN YEAR(c.consumption_date) = 2020 THEN c.usage_value END), 2) as avg_2020
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY yoy_change_percentage DESC;

-- 4. Regional Year-over-Year Comparison
SELECT 
    s.region,
    ROUND(SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_value END), 2) as total_2019,
    ROUND(SUM(CASE WHEN YEAR(c.consumption_date) = 2020 THEN c.usage_value END), 2) as total_2020,
    ROUND(
        (SUM(CASE WHEN YEAR(c.consumption_date) = 2020 THEN c.usage_value END) - 
         SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_value END)) / 
        SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_value END) * 100, 2
    ) as regional_yoy_change,
    COUNT(DISTINCT s.state_name) as states_in_region
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.region
ORDER BY total_2020 DESC;

-- ============================================
-- MONTHLY TRENDS ANALYSIS
-- ============================================

-- 5. Monthly Consumption Trends (2019-2020)
SELECT 
    YEAR(c.consumption_date) as year,
    MONTH(c.consumption_date) as month,
    MONTHNAME(c.consumption_date) as month_name,
    ROUND(SUM(c.usage_value), 2) as monthly_total,
    ROUND(AVG(c.usage_value), 2) as daily_average,
    ROUND(MAX(c.usage_value), 2) as monthly_peak,
    ROUND(MIN(c.usage_value), 2) as monthly_minimum,
    COUNT(DISTINCT c.consumption_date) as days_in_month,
    COUNT(DISTINCT s.state_name) as active_states
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY YEAR(c.consumption_date), MONTH(c.consumption_date)
ORDER BY year, month;

-- 6. Month-over-Month Growth Rate
WITH monthly_data AS (
    SELECT 
        YEAR(c.consumption_date) as year,
        MONTH(c.consumption_date) as month,
        SUM(c.usage_value) as monthly_total
    FROM consumption c
    GROUP BY YEAR(c.consumption_date), MONTH(c.consumption_date)
),
lagged_data AS (
    SELECT 
        year,
        month,
        monthly_total,
        LAG(monthly_total) OVER (ORDER BY year, month) as previous_month_total
    FROM monthly_data
)
SELECT 
    year,
    month,
    monthly_total,
    previous_month_total,
    ROUND(((monthly_total - previous_month_total) / previous_month_total) * 100, 2) as mom_growth_percentage
FROM lagged_data
WHERE previous_month_total IS NOT NULL
ORDER BY year, month;

-- ============================================
-- TOP AND BOTTOM PERFORMERS
-- ============================================

-- 7. Top 10 States by Total Consumption
SELECT 
    s.state_name,
    s.region,
    ROUND(SUM(c.usage_value), 2) as total_consumption,
    ROUND(AVG(c.usage_value), 2) as average_consumption,
    ROUND(MAX(c.usage_value), 2) as peak_consumption,
    COUNT(*) as data_points,
    ROUND((SUM(c.usage_value) / (SELECT SUM(usage_value) FROM consumption)) * 100, 2) as market_share_percentage
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY total_consumption DESC
LIMIT 10;

-- 8. Bottom 10 States by Total Consumption
SELECT 
    s.state_name,
    s.region,
    ROUND(SUM(c.usage_value), 2) as total_consumption,
    ROUND(AVG(c.usage_value), 2) as average_consumption,
    ROUND(MAX(c.usage_value), 2) as peak_consumption,
    COUNT(*) as data_points,
    ROUND((SUM(c.usage_value) / (SELECT SUM(usage_value) FROM consumption)) * 100, 2) as market_share_percentage
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY total_consumption ASC
LIMIT 10;

-- 9. Top 5 States by Peak Consumption
SELECT 
    s.state_name,
    s.region,
    ROUND(MAX(c.usage_value), 2) as peak_consumption,
    ROUND(AVG(c.usage_value), 2) as average_consumption,
    c.consumption_date as peak_date
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region, c.consumption_date
HAVING peak_consumption = (
    SELECT MAX(usage_value) 
    FROM consumption c2 
    WHERE c2.state_id = c.state_id
)
ORDER BY peak_consumption DESC
LIMIT 5;

-- ============================================
-- COVID-19 LOCKDOWN IMPACT ANALYSIS
-- ============================================

-- 10. Lockdown Impact Analysis (March 25 - May 31, 2020)
SELECT 
    s.state_name,
    s.region,
    ROUND(AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END), 2) as pre_lockdown_avg,
    ROUND(AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END), 2) as during_lockdown_avg,
    ROUND(AVG(CASE WHEN c.consumption_date > '2020-05-31' THEN c.usage_value END), 2) as post_lockdown_avg,
    ROUND(
        ((AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END) - 
          AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END)) / 
         AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END)) * 100, 2
    ) as lockdown_impact_percentage,
    ROUND(
        ((AVG(CASE WHEN c.consumption_date > '2020-05-31' THEN c.usage_value END) - 
          AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END)) / 
         AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END)) * 100, 2
    ) as recovery_percentage
FROM consumption c
JOIN states s ON c.state_id = s.state_id
WHERE YEAR(c.consumption_date) = 2020
GROUP BY s.state_name, s.region
HAVING pre_lockdown_avg IS NOT NULL AND during_lockdown_avg IS NOT NULL
ORDER BY lockdown_impact_percentage ASC;

-- 11. Regional Lockdown Impact Summary
SELECT 
    s.region,
    ROUND(AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END), 2) as regional_pre_lockdown,
    ROUND(AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END), 2) as regional_during_lockdown,
    ROUND(AVG(CASE WHEN c.consumption_date > '2020-05-31' THEN c.usage_value END), 2) as regional_post_lockdown,
    ROUND(
        ((AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END) - 
          AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END)) / 
         AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END)) * 100, 2
    ) as regional_lockdown_impact
FROM consumption c
JOIN states s ON c.state_id = s.state_id
WHERE YEAR(c.consumption_date) = 2020
GROUP BY s.region
ORDER BY regional_lockdown_impact ASC;

-- ============================================
-- SEASONAL PATTERNS ANALYSIS
-- ============================================

-- 12. Seasonal Consumption Patterns
SELECT 
    CASE 
        WHEN MONTH(c.consumption_date) IN (12, 1, 2) THEN 'Winter'
        WHEN MONTH(c.consumption_date) IN (3, 4, 5) THEN 'Summer'
        WHEN MONTH(c.consumption_date) IN (6, 7, 8, 9) THEN 'Monsoon'
        ELSE 'Post-Monsoon'
    END as season,
    YEAR(c.consumption_date) as year,
    ROUND(SUM(c.usage_value), 2) as seasonal_total,
    ROUND(AVG(c.usage_value), 2) as daily_average,
    ROUND(MAX(c.usage_value), 2) as seasonal_peak,
    ROUND(MIN(c.usage_value), 2) as seasonal_minimum,
    COUNT(DISTINCT c.consumption_date) as days_in_season,
    COUNT(DISTINCT s.state_name) as active_states
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY season, YEAR(c.consumption_date)
ORDER BY year, 
    CASE season 
        WHEN 'Winter' THEN 1
        WHEN 'Summer' THEN 2
        WHEN 'Monsoon' THEN 3
        WHEN 'Post-Monsoon' THEN 4
    END;

-- 13. Regional Seasonal Comparison
SELECT 
    s.region,
    CASE 
        WHEN MONTH(c.consumption_date) IN (12, 1, 2) THEN 'Winter'
        WHEN MONTH(c.consumption_date) IN (3, 4, 5) THEN 'Summer'
        WHEN MONTH(c.consumption_date) IN (6, 7, 8, 9) THEN 'Monsoon'
        ELSE 'Post-Monsoon'
    END as season,
    ROUND(SUM(c.usage_value), 2) as regional_seasonal_total,
    ROUND(AVG(c.usage_value), 2) as regional_daily_average,
    ROUND(MAX(c.usage_value), 2) as regional_seasonal_peak
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.region, season
ORDER BY s.region, 
    CASE season 
        WHEN 'Winter' THEN 1
        WHEN 'Summer' THEN 2
        WHEN 'Monsoon' THEN 3
        WHEN 'Post-Monsoon' THEN 4
    END;

-- ============================================
-- QUARTERLY ANALYSIS
-- ============================================

-- 14. Quarterly Consumption by State
SELECT 
    s.state_name,
    s.region,
    YEAR(c.consumption_date) as year,
    QUARTER(c.consumption_date) as quarter,
    CONCAT('Q', QUARTER(c.consumption_date)) as quarter_name,
    ROUND(SUM(c.usage_value), 2) as quarterly_total,
    ROUND(AVG(c.usage_value), 2) as quarterly_average,
    ROUND(MAX(c.usage_value), 2) as quarterly_peak,
    ROUND(MIN(c.usage_value), 2) as quarterly_minimum,
    COUNT(DISTINCT c.consumption_date) as days_in_quarter
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region, YEAR(c.consumption_date), QUARTER(c.consumption_date)
ORDER BY year, quarter, quarterly_total DESC;

-- 15. Regional Quarterly Trends
SELECT 
    s.region,
    YEAR(c.consumption_date) as year,
    QUARTER(c.consumption_date) as quarter,
    CONCAT('Q', QUARTER(c.consumption_date)) as quarter_name,
    ROUND(SUM(c.usage_value), 2) as regional_quarterly_total,
    ROUND(AVG(c.usage_value), 2) as regional_quarterly_average,
    COUNT(DISTINCT s.state_name) as active_states
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.region, YEAR(c.consumption_date), QUARTER(c.consumption_date)
ORDER BY year, quarter, regional_quarterly_total DESC;

-- ============================================
-- ADVANCED ANALYTICS QUERIES
-- ============================================

-- 16. Consumption Volatility Analysis
WITH state_stats AS (
    SELECT 
        s.state_name,
        s.region,
        AVG(c.usage_value) as avg_consumption,
        STDDEV(c.usage_value) as consumption_stddev,
        COUNT(*) as data_points
    FROM consumption c
    JOIN states s ON c.state_id = s.state_id
    GROUP BY s.state_name, s.region
    HAVING data_points >= 50  -- Ensure sufficient data points
)
SELECT 
    state_name,
    region,
    ROUND(avg_consumption, 2) as average_consumption,
    ROUND(consumption_stddev, 2) as consumption_volatility,
    ROUND((consumption_stddev / avg_consumption) * 100, 2) as volatility_percentage,
    data_points
FROM state_stats
ORDER BY volatility_percentage DESC;

-- 17. Peak Consumption Days Analysis
SELECT 
    c.consumption_date,
    DAYNAME(c.consumption_date) as day_of_week,
    ROUND(SUM(c.usage_value), 2) as daily_total,
    ROUND(AVG(c.usage_value), 2) as daily_average,
    COUNT(DISTINCT s.state_name) as active_states,
    COUNT(*) as total_records
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY c.consumption_date, DAYNAME(c.consumption_date)
ORDER BY daily_total DESC
LIMIT 20;

-- 18. Regional Performance Ranking
WITH regional_scores AS (
    SELECT 
        s.region,
        ROUND(SUM(c.usage_value), 2) as total_consumption,
        ROUND(AVG(c.usage_value), 2) as avg_consumption,
        ROUND(MAX(c.usage_value), 2) as peak_consumption,
        COUNT(DISTINCT s.state_name) as state_count,
        -- Calculate growth rate
        ROUND(
            (SUM(CASE WHEN YEAR(c.consumption_date) = 2020 THEN c.usage_value END) - 
             SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_value END)) / 
            SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_value END) * 100, 2
        ) as growth_rate
    FROM consumption c
    JOIN states s ON c.state_id = s.state_id
    GROUP BY s.region
)
SELECT 
    region,
    total_consumption,
    avg_consumption,
    peak_consumption,
    state_count,
    growth_rate,
    -- Calculate composite score (0-100)
    ROUND(
        (total_consumption / (SELECT MAX(total_consumption) FROM regional_scores)) * 40 +
        (growth_rate / (SELECT MAX(growth_rate) FROM regional_scores)) * 30 +
        (state_count / (SELECT MAX(state_count) FROM regional_scores)) * 30, 2
    ) as performance_score
FROM regional_scores
ORDER BY performance_score DESC;

-- ============================================
-- TABLEAU-SPECIFIC VIEWS
-- ============================================

-- 19. Tableau Dashboard View - Comprehensive
CREATE OR REPLACE VIEW tableau_dashboard_view AS
SELECT 
    s.state_name,
    s.region,
    s.latitude,
    s.longitude,
    c.consumption_date,
    YEAR(c.consumption_date) as year,
    MONTH(c.consumption_date) as month,
    MONTHNAME(c.consumption_date) as month_name,
    QUARTER(c.consumption_date) as quarter,
    DAYNAME(c.consumption_date) as day_of_week,
    c.usage_value,
    CASE 
        WHEN MONTH(c.consumption_date) IN (12, 1, 2) THEN 'Winter'
        WHEN MONTH(c.consumption_date) IN (3, 4, 5) THEN 'Summer'
        WHEN MONTH(c.consumption_date) IN (6, 7, 8, 9) THEN 'Monsoon'
        ELSE 'Post-Monsoon'
    END as season,
    CASE 
        WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN 'Lockdown'
        WHEN YEAR(c.consumption_date) = 2020 AND c.consumption_date > '2020-05-31' THEN 'Post-Lockdown'
        WHEN YEAR(c.consumption_date) = 2020 AND c.consumption_date < '2020-03-25' THEN 'Pre-Lockdown'
        ELSE 'Normal'
    END as period_type
FROM consumption c
JOIN states s ON c.state_id = s.state_id;

-- 20. Tableau KPI View
CREATE OR REPLACE VIEW tableau_kpi_view AS
SELECT 
    'Total Consumption' as kpi_name,
    ROUND(SUM(usage_value), 2) as kpi_value,
    'MWh' as unit
FROM consumption
UNION ALL
SELECT 
    'Average Daily Consumption' as kpi_name,
    ROUND(AVG(usage_value), 2) as kpi_value,
    'MWh' as unit
FROM consumption
UNION ALL
SELECT 
    'Peak Consumption' as kpi_name,
    ROUND(MAX(usage_value), 2) as kpi_value,
    'MWh' as unit
FROM consumption
UNION ALL
SELECT 
    'Total States' as kpi_name,
    COUNT(DISTINCT state_id) as kpi_value,
    'Count' as unit
FROM consumption
UNION ALL
SELECT 
    'Data Period (Days)' as kpi_name,
    COUNT(DISTINCT consumption_date) as kpi_value,
    'Days' as unit
FROM consumption;

-- ============================================
-- PERFORMANCE TESTING QUERIES
-- ============================================

-- 21. Query Performance Test - Large Dataset
SELECT 
    s.state_name,
    s.region,
    COUNT(*) as record_count,
    ROUND(SUM(c.usage_value), 2) as total_consumption,
    ROUND(AVG(c.usage_value), 2) as avg_consumption,
    MIN(c.consumption_date) as first_date,
    MAX(c.consumption_date) as last_date
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY total_consumption DESC;

-- 22. Index Usage Verification
EXPLAIN SELECT 
    s.state_name,
    s.region,
    c.consumption_date,
    c.usage_value
FROM consumption c
JOIN states s ON c.state_id = s.state_id
WHERE c.consumption_date BETWEEN '2019-01-01' AND '2020-12-31'
AND s.region = 'NR'
ORDER BY c.consumption_date;

-- ============================================
-- DATA VALIDATION QUERIES
-- ============================================

-- 23. Data Quality Check
SELECT 
    'Missing Values' as check_type,
    COUNT(*) as total_records,
    COUNT(CASE WHEN usage_value IS NULL THEN 1 END) as null_usage,
    COUNT(CASE WHEN consumption_date IS NULL THEN 1 END) as null_dates,
    COUNT(CASE WHEN usage_value < 0 THEN 1 END) as negative_values,
    COUNT(CASE WHEN usage_value = 0 THEN 1 END) as zero_values
FROM consumption;

-- 24. Date Range Validation
SELECT 
    'Date Range Check' as check_type,
    MIN(consumption_date) as earliest_date,
    MAX(consumption_date) as latest_date,
    COUNT(DISTINCT consumption_date) as unique_dates,
    COUNT(*) as total_records,
    COUNT(*) / COUNT(DISTINCT consumption_date) as avg_records_per_day
FROM consumption;

-- ============================================
-- EXPORT AND REPORTING QUERIES
-- ============================================

-- 25. State-wise Monthly Report
SELECT 
    s.state_name,
    s.region,
    YEAR(c.consumption_date) as year,
    MONTHNAME(c.consumption_date) as month,
    ROUND(SUM(c.usage_value), 2) as monthly_consumption,
    ROUND(AVG(c.usage_value), 2) as daily_average,
    MAX(c.usage_value) as peak_consumption,
    MIN(c.usage_value) as minimum_consumption,
    COUNT(DISTINCT c.consumption_date) as days_reported
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region, YEAR(c.consumption_date), MONTH(c.consumption_date)
ORDER BY s.state_name, year, month;
