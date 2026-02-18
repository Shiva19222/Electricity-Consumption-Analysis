-- Electricity Consumption Analysis SQL Queries
-- These queries are optimized for Tableau integration and data analysis

-- ============================================
-- 1. 2019 vs 2020 Consumption Comparison
-- ============================================

-- Year-over-year consumption comparison by state
SELECT 
    s.state_name,
    s.region,
    SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_mwh ELSE 0 END) as consumption_2019,
    SUM(CASE WHEN YEAR(c.consumption_date) = 2020 THEN c.usage_mwh ELSE 0 END) as consumption_2020,
    ROUND(
        ((SUM(CASE WHEN YEAR(c.consumption_date) = 2020 THEN c.usage_mwh ELSE 0 END) - 
          SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_mwh ELSE 0 END)) / 
         SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_mwh ELSE 0 END)) * 100, 2
    ) as percentage_change,
    ROUND(AVG(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_mwh ELSE NULL END), 2) as avg_2019,
    ROUND(AVG(CASE WHEN YEAR(c.consumption_date) = 2020 THEN c.usage_mwh ELSE NULL END), 2) as avg_2020
FROM consumption c
JOIN states s ON c.state_id = s.state_id
WHERE YEAR(c.consumption_date) IN (2019, 2020)
GROUP BY s.state_name, s.region
ORDER BY consumption_2020 DESC;

-- Regional consumption trends 2019 vs 2020
SELECT 
    s.region,
    SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_mwh ELSE 0 END) as total_2019,
    SUM(CASE WHEN YEAR(c.consumption_date) = 2020 THEN c.usage_mwh ELSE 0 END) as total_2020,
    ROUND(
        ((SUM(CASE WHEN YEAR(c.consumption_date) = 2020 THEN c.usage_mwh ELSE 0 END) - 
          SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_mwh ELSE 0 END)) / 
         SUM(CASE WHEN YEAR(c.consumption_date) = 2019 THEN c.usage_mwh ELSE 0 END)) * 100, 2
    ) as regional_growth_percentage
FROM consumption c
JOIN states s ON c.state_id = s.state_id
WHERE YEAR(c.consumption_date) IN (2019, 2020)
GROUP BY s.region
ORDER BY total_2020 DESC;

-- ============================================
-- 2. Total Consumption Analysis
-- ============================================

-- Overall consumption statistics
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT c.state_id) as states_covered,
    COUNT(DISTINCT s.region) as regions_covered,
    SUM(c.usage_mwh) as total_consumption_mwh,
    ROUND(AVG(c.usage_mwh), 2) as average_consumption_mwh,
    MAX(c.usage_mwh) as peak_consumption_mwh,
    MIN(c.usage_mwh) as minimum_consumption_mwh,
    ROUND(STDDEV(c.usage_mwh), 2) as consumption_std_dev
FROM consumption c
JOIN states s ON c.state_id = s.state_id;

-- Monthly total consumption trends
SELECT 
    YEAR(c.consumption_date) as analysis_year,
    MONTH(c.consumption_date) as analysis_month,
    DATE_FORMAT(c.consumption_date, '%Y-%m') as year_month,
    DATE_FORMAT(c.consumption_date, '%M %Y') as month_year_label,
    SUM(c.usage_mwh) as monthly_total,
    ROUND(AVG(c.usage_mwh), 2) as daily_average,
    MAX(c.usage_mwh) as monthly_peak,
    MIN(c.usage_mwh) as monthly_minimum,
    COUNT(*) as days_in_month,
    ROUND(
        (SUM(c.usage_mwh) - LAG(SUM(c.usage_mwh)) OVER (ORDER BY YEAR(c.consumption_date), MONTH(c.consumption_date))) / 
        LAG(SUM(c.usage_mwh)) OVER (ORDER BY YEAR(c.consumption_date), MONTH(c.consumption_date)) * 100, 2
    ) as month_over_month_change
FROM consumption c
GROUP BY YEAR(c.consumption_date), MONTH(c.consumption_date)
ORDER BY analysis_year, analysis_month;

-- ============================================
-- 3. Usage by Region Analysis
-- ============================================

-- Regional consumption breakdown
SELECT 
    s.region,
    SUM(c.usage_mwh) as total_consumption,
    ROUND(AVG(c.usage_mwh), 2) as average_consumption,
    MAX(c.usage_mwh) as peak_consumption,
    MIN(c.usage_mwh) as minimum_consumption,
    COUNT(DISTINCT c.state_id) as number_of_states,
    ROUND(SUM(c.usage_mwh) * 100.0 / (SELECT SUM(usage_mwh) FROM consumption), 2) as percentage_of_total,
    ROUND(STDDEV(c.usage_mwh), 2) as consumption_variance
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.region
ORDER BY total_consumption DESC;

-- Regional performance over time
SELECT 
    s.region,
    YEAR(c.consumption_date) as analysis_year,
    QUARTER(c.consumption_date) as quarter,
    SUM(c.usage_mwh) as quarterly_consumption,
    ROUND(AVG(c.usage_mwh), 2) as quarterly_average,
    MAX(c.usage_mwh) as quarterly_peak,
    COUNT(DISTINCT c.state_id) as active_states
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.region, YEAR(c.consumption_date), QUARTER(c.consumption_date)
ORDER BY s.region, analysis_year, quarter;

-- ============================================
-- 4. Top N and Bottom N States Analysis
-- ============================================

-- Top 10 states by total consumption
SELECT 
    s.state_name,
    s.region,
    SUM(c.usage_mwh) as total_consumption,
    ROUND(AVG(c.usage_mwh), 2) as average_consumption,
    MAX(c.usage_mwh) as peak_consumption,
    MIN(c.usage_mwh) as minimum_consumption,
    COUNT(*) as data_points,
    ROUND(SUM(c.usage_mwh) * 100.0 / (SELECT SUM(usage_mwh) FROM consumption), 2) as market_share_percentage
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY total_consumption DESC
LIMIT 10;

-- Bottom 10 states by total consumption
SELECT 
    s.state_name,
    s.region,
    SUM(c.usage_mwh) as total_consumption,
    ROUND(AVG(c.usage_mwh), 2) as average_consumption,
    MAX(c.usage_mwh) as peak_consumption,
    MIN(c.usage_mwh) as minimum_consumption,
    COUNT(*) as data_points,
    ROUND(SUM(c.usage_mwh) * 100.0 / (SELECT SUM(usage_mwh) FROM consumption), 2) as market_share_percentage
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY total_consumption ASC
LIMIT 10;

-- States with highest growth rate (2019 to 2020)
WITH state_yearly_consumption AS (
    SELECT 
        s.state_name,
        s.region,
        YEAR(c.consumption_date) as consumption_year,
        SUM(c.usage_mwh) as yearly_consumption
    FROM consumption c
    JOIN states s ON c.state_id = s.state_id
    WHERE YEAR(c.consumption_date) IN (2019, 2020)
    GROUP BY s.state_name, s.region, YEAR(c.consumption_date)
)
SELECT 
    t1.state_name,
    t1.region,
    t1.yearly_consumption as consumption_2019,
    t2.yearly_consumption as consumption_2020,
    ROUND(((t2.yearly_consumption - t1.yearly_consumption) / t1.yearly_consumption) * 100, 2) as growth_percentage
FROM state_yearly_consumption t1
JOIN state_yearly_consumption t2 ON t1.state_name = t2.state_name
WHERE t1.consumption_year = 2019 AND t2.consumption_year = 2020
ORDER BY growth_percentage DESC
LIMIT 10;

-- ============================================
-- 5. Month-wise Consumption Analysis
-- ============================================

-- Month-wise consumption for 2019 and 2020
SELECT 
    YEAR(c.consumption_date) as analysis_year,
    MONTH(c.consumption_date) as analysis_month,
    DATE_FORMAT(c.consumption_date, '%M') as month_name,
    SUM(c.usage_mwh) as monthly_total,
    ROUND(AVG(c.usage_mwh), 2) as daily_average,
    MAX(c.usage_mwh) as monthly_peak,
    MIN(c.usage_mwh) as monthly_minimum,
    COUNT(*) as number_of_days,
    COUNT(DISTINCT c.state_id) as states_reported
FROM consumption c
GROUP BY YEAR(c.consumption_date), MONTH(c.consumption_date), DATE_FORMAT(c.consumption_date, '%M')
ORDER BY analysis_year, analysis_month;

-- Seasonal consumption patterns
SELECT 
    CASE 
        WHEN MONTH(c.consumption_date) IN (12, 1, 2) THEN 'Winter'
        WHEN MONTH(c.consumption_date) IN (3, 4, 5) THEN 'Spring'
        WHEN MONTH(c.consumption_date) IN (6, 7, 8) THEN 'Summer'
        WHEN MONTH(c.consumption_date) IN (9, 10, 11) THEN 'Autumn'
    END as season,
    YEAR(c.consumption_date) as analysis_year,
    SUM(c.usage_mwh) as seasonal_total,
    ROUND(AVG(c.usage_mwh), 2) as daily_average,
    MAX(c.usage_mwh) as seasonal_peak,
    MIN(c.usage_mwh) as seasonal_minimum,
    COUNT(*) as days_in_season
FROM consumption c
GROUP BY YEAR(c.consumption_date), 
    CASE 
        WHEN MONTH(c.consumption_date) IN (12, 1, 2) THEN 'Winter'
        WHEN MONTH(c.consumption_date) IN (3, 4, 5) THEN 'Spring'
        WHEN MONTH(c.consumption_date) IN (6, 7, 8) THEN 'Summer'
        WHEN MONTH(c.consumption_date) IN (9, 10, 11) THEN 'Autumn'
    END
ORDER BY analysis_year, 
    CASE 
        WHEN MONTH(c.consumption_date) IN (12, 1, 2) THEN 1
        WHEN MONTH(c.consumption_date) IN (3, 4, 5) THEN 2
        WHEN MONTH(c.consumption_date) IN (6, 7, 8) THEN 3
        WHEN MONTH(c.consumption_date) IN (9, 10, 11) THEN 4
    END;

-- ============================================
-- 6. Lockdown Impact Analysis
-- ============================================

-- Before, during, and after lockdown consumption comparison
SELECT 
    s.state_name,
    s.region,
    ROUND(AVG(CASE WHEN c.consumption_date < '2020-03-25' THEN c.usage_mwh END), 2) as pre_lockdown_avg,
    ROUND(AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_mwh END), 2) as during_lockdown_avg,
    ROUND(AVG(CASE WHEN c.consumption_date > '2020-05-31' THEN c.usage_mwh END), 2) as post_lockdown_avg,
    ROUND(
        ((AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_mwh END) - 
          AVG(CASE WHEN c.consumption_date < '2020-03-25' THEN c.usage_mwh END)) / 
         AVG(CASE WHEN c.consumption_date < '2020-03-25' THEN c.usage_mwh END)) * 100, 2
    ) as lockdown_impact_percentage,
    ROUND(
        ((AVG(CASE WHEN c.consumption_date > '2020-05-31' THEN c.usage_mwh END) - 
          AVG(CASE WHEN c.consumption_date < '2020-03-25' THEN c.usage_mwh END)) / 
         AVG(CASE WHEN c.consumption_date < '2020-03-25' THEN c.usage_mwh END)) * 100, 2
    ) as recovery_percentage
FROM consumption c
JOIN states s ON c.state_id = s.state_id
WHERE YEAR(c.consumption_date) = 2020
GROUP BY s.state_name, s.region
ORDER BY lockdown_impact_percentage;

-- Regional lockdown impact
SELECT 
    s.region,
    ROUND(AVG(CASE WHEN c.consumption_date < '2020-03-25' THEN c.usage_mwh END), 2) as pre_lockdown_avg,
    ROUND(AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_mwh END), 2) as during_lockdown_avg,
    ROUND(AVG(CASE WHEN c.consumption_date > '2020-05-31' THEN c.usage_mwh END), 2) as post_lockdown_avg,
    COUNT(DISTINCT c.state_id) as states_in_region
FROM consumption c
JOIN states s ON c.state_id = s.state_id
WHERE YEAR(c.consumption_date) = 2020
GROUP BY s.region
ORDER BY pre_lockdown_avg DESC;

-- ============================================
-- 7. Quarter-wise Usage Analysis
-- ============================================

-- Quarterly consumption by state
SELECT 
    s.state_name,
    s.region,
    YEAR(c.consumption_date) as analysis_year,
    QUARTER(c.consumption_date) as quarter,
    CONCAT('Q', QUARTER(c.consumption_date), ' ', YEAR(c.consumption_date)) as quarter_label,
    SUM(c.usage_mwh) as quarterly_consumption,
    ROUND(AVG(c.usage_mwh), 2) as quarterly_average,
    MAX(c.usage_mwh) as quarterly_peak,
    MIN(c.usage_mwh) as quarterly_minimum,
    COUNT(*) as days_in_quarter
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region, YEAR(c.consumption_date), QUARTER(c.consumption_date)
ORDER BY s.state_name, analysis_year, quarter;

-- Regional quarterly trends
SELECT 
    s.region,
    YEAR(c.consumption_date) as analysis_year,
    QUARTER(c.consumption_date) as quarter,
    CONCAT('Q', QUARTER(c.consumption_date), ' ', YEAR(c.consumption_date)) as quarter_label,
    SUM(c.usage_mwh) as regional_quarterly_total,
    ROUND(AVG(c.usage_mwh), 2) as regional_quarterly_average,
    MAX(c.usage_mwh) as regional_quarterly_peak,
    COUNT(DISTINCT c.state_id) as active_states,
    ROUND(
        (SUM(c.usage_mwh) - LAG(SUM(c.usage_mwh)) OVER (PARTITION BY s.region ORDER BY YEAR(c.consumption_date), QUARTER(c.consumption_date))) / 
        LAG(SUM(c.usage_mwh)) OVER (PARTITION BY s.region ORDER BY YEAR(c.consumption_date), QUARTER(c.consumption_date)) * 100, 2
    ) as quarter_over_quarter_change
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.region, YEAR(c.consumption_date), QUARTER(c.consumption_date)
ORDER BY s.region, analysis_year, quarter;

-- ============================================
-- 8. Usage by Year Analysis
-- ============================================

-- Annual consumption summary
SELECT 
    YEAR(c.consumption_date) as analysis_year,
    SUM(c.usage_mwh) as annual_consumption,
    ROUND(AVG(c.usage_mwh), 2) as daily_average,
    MAX(c.usage_mwh) as annual_peak,
    MIN(c.usage_mwh) as annual_minimum,
    COUNT(*) as total_days,
    COUNT(DISTINCT c.state_id) as states_reported,
    ROUND(STDDEV(c.usage_mwh), 2) as consumption_variance,
    ROUND(
        (SUM(c.usage_mwh) - LAG(SUM(c.usage_mwh)) OVER (ORDER BY YEAR(c.consumption_date))) / 
        LAG(SUM(c.usage_mwh)) OVER (ORDER BY YEAR(c.consumption_date)) * 100, 2
    ) as year_over_year_growth
FROM consumption c
GROUP BY YEAR(c.consumption_date)
ORDER BY analysis_year;

-- State-wise annual performance
SELECT 
    s.state_name,
    s.region,
    YEAR(c.consumption_date) as analysis_year,
    SUM(c.usage_mwh) as annual_consumption,
    ROUND(AVG(c.usage_mwh), 2) as daily_average,
    MAX(c.usage_mwh) as annual_peak,
    MIN(c.usage_mwh) as annual_minimum,
    COUNT(*) as days_reported,
    RANK() OVER (PARTITION BY YEAR(c.consumption_date) ORDER BY SUM(c.usage_mwh) DESC) as consumption_rank
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region, YEAR(c.consumption_date)
ORDER BY analysis_year, consumption_rank;

-- ============================================
-- 9. Advanced Analytics Queries
-- ============================================

-- Peak consumption days analysis
SELECT 
    c.consumption_date,
    s.state_name,
    s.region,
    c.usage_mwh,
    RANK() OVER (PARTITION BY s.state_name ORDER BY c.usage_mwh DESC) as state_rank,
    RANK() OVER (ORDER BY c.usage_mwh DESC) as overall_rank,
    DAYOFWEEK(c.consumption_date) as day_of_week,
    CASE 
        WHEN DAYOFWEEK(c.consumption_date) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type
FROM consumption c
JOIN states s ON c.state_id = s.state_id
ORDER BY c.usage_mwh DESC
LIMIT 50;

-- Consumption volatility analysis
SELECT 
    s.state_name,
    s.region,
    ROUND(AVG(c.usage_mwh), 2) as average_consumption,
    ROUND(STDDEV(c.usage_mwh), 2) as consumption_volatility,
    ROUND(STDDEV(c.usage_mwh) / AVG(c.usage_mwh) * 100, 2) as volatility_percentage,
    MAX(c.usage_mwh) as peak_consumption,
    MIN(c.usage_mwh) as minimum_consumption,
    ROUND((MAX(c.usage_mwh) - MIN(c.usage_mwh)) / AVG(c.usage_mwh) * 100, 2) as range_percentage
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY volatility_percentage DESC;

-- Weekend vs Weekday consumption patterns
SELECT 
    s.state_name,
    s.region,
    ROUND(AVG(CASE WHEN c.is_weekend = TRUE THEN c.usage_mwh END), 2) as weekend_average,
    ROUND(AVG(CASE WHEN c.is_weekend = FALSE THEN c.usage_mwh END), 2) as weekday_average,
    ROUND(
        ((AVG(CASE WHEN c.is_weekend = TRUE THEN c.usage_mwh END) - 
          AVG(CASE WHEN c.is_weekend = FALSE THEN c.usage_mwh END)) / 
         AVG(CASE WHEN c.is_weekend = FALSE THEN c.usage_mwh END)) * 100, 2
    ) as weekend_weekday_difference_percentage
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY weekend_weekday_difference_percentage DESC;
