-- Electric Vehicle Analysis SQL Queries
-- Comprehensive EV Market Analysis for Tableau Integration

-- ============================================
-- EV MARKET OVERVIEW QUERIES
-- ============================================

-- 1. Overall EV Market Overview
SELECT 
    'EV Market Overview' as metric,
    COUNT(*) as total_models,
    COUNT(DISTINCT brand) as unique_brands,
    COUNT(DISTINCT segment) as segments_covered,
    ROUND(MIN(price), 2) as minimum_price,
    ROUND(MAX(price), 2) as maximum_price,
    ROUND(AVG(price), 2) as average_price,
    ROUND(MIN(range_km), 2) as minimum_range,
    ROUND(MAX(range_km), 2) as maximum_range,
    ROUND(AVG(range_km), 2) as average_range,
    ROUND(AVG(battery_capacity_kwh), 2) as average_battery_capacity
FROM ev_specifications;

-- 2. Brand Market Share Analysis
SELECT 
    brand,
    COUNT(*) as total_models,
    ROUND(AVG(price), 2) as average_price,
    ROUND(AVG(range_km), 2) as average_range,
    ROUND(AVG(battery_capacity_kwh), 2) as average_battery,
    COUNT(DISTINCT segment) as segments_covered,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ev_specifications)), 2) as market_share_percentage,
    MIN(year) as first_model_year,
    MAX(year) as latest_model_year
FROM ev_specifications
GROUP BY brand
ORDER BY total_models DESC;

-- ============================================
-- PRICE ANALYSIS QUERIES
-- ============================================

-- 3. Price Range Distribution
SELECT 
    CASE 
        WHEN price < 30000 THEN 'Budget (< $30k)'
        WHEN price BETWEEN 30000 AND 60000 THEN 'Mid-Range ($30k-$60k)'
        WHEN price BETWEEN 60000 AND 100000 THEN 'Premium ($60k-$100k)'
        ELSE 'Luxury (> $100k)'
    END as price_category,
    COUNT(*) as model_count,
    COUNT(DISTINCT brand) as unique_brands,
    ROUND(AVG(price), 2) as avg_price_in_category,
    ROUND(AVG(range_km), 2) as avg_range_in_category,
    ROUND(AVG(battery_capacity_kwh), 2) as avg_battery_in_category,
    MIN(price) as min_price_in_category,
    MAX(price) as max_price_in_category
FROM ev_specifications
GROUP BY 
    CASE 
        WHEN price < 30000 THEN 'Budget (< $30k)'
        WHEN price BETWEEN 30000 AND 60000 THEN 'Mid-Range ($30k-$60k)'
        WHEN price BETWEEN 60000 AND 100000 THEN 'Premium ($60k-$100k)'
        ELSE 'Luxury (> $100k)'
    END
ORDER BY avg_price_in_category;

-- 4. Price vs Range Analysis
SELECT 
    brand,
    model,
    year,
    price,
    range_km,
    battery_capacity_kwh,
    efficiency_km_kwh,
    ROUND(price / range_km, 2) as price_per_km_range,
    ROUND(range_km / battery_capacity_kwh, 2) as range_per_kwh_battery,
    CASE 
        WHEN price < 30000 THEN 'Budget'
        WHEN price BETWEEN 30000 AND 60000 THEN 'Mid-Range'
        WHEN price BETWEEN 60000 AND 100000 THEN 'Premium'
        ELSE 'Luxury'
    END as price_category,
    CASE 
        WHEN range_km < 200 THEN 'Short Range'
        WHEN range_km BETWEEN 200 AND 400 THEN 'Medium Range'
        WHEN range_km BETWEEN 400 AND 600 THEN 'Long Range'
        ELSE 'Ultra Long Range'
    END as range_category
FROM ev_specifications
ORDER BY price;

-- 5. Best Value EVs (Price vs Range)
SELECT 
    brand,
    model,
    price,
    range_km,
    battery_capacity_kwh,
    ROUND(price / range_km, 2) as price_per_km_range,
    ROUND(range_km / battery_capacity_kwh, 2) as efficiency_score,
    ROUND((range_km * 1000) / price, 2) as value_score
FROM ev_specifications
WHERE price > 0 AND range_km > 0
ORDER BY value_score DESC
LIMIT 20;

-- ============================================
-- TECHNOLOGY & PERFORMANCE ANALYSIS
-- ============================================

-- 6. Technology Evolution by Year
SELECT 
    year,
    COUNT(*) as total_models,
    COUNT(DISTINCT brand) as unique_brands,
    ROUND(AVG(battery_capacity_kwh), 2) as avg_battery_capacity,
    ROUND(AVG(range_km), 2) as avg_range,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(AVG(efficiency_km_kwh), 2) as avg_efficiency,
    ROUND(AVG(fast_charging_kw), 2) as avg_charging_speed,
    MIN(price) as min_price_year,
    MAX(price) as max_price_year,
    MIN(range_km) as min_range_year,
    MAX(range_km) as max_range_year
FROM ev_specifications
GROUP BY year
ORDER BY year;

-- 7. Performance Metrics Analysis
SELECT 
    brand,
    model,
    top_speed_kmh,
    acceleration_0_100,
    range_km,
    battery_capacity_kwh,
    efficiency_km_kwh,
    fast_charging_kw,
    ROUND(top_speed_kmh / acceleration_0_100, 2) as performance_score,
    ROUND(range_km / battery_capacity_kwh, 2) as range_efficiency,
    ROUND(fast_charging_kw / battery_capacity_kwh * 100, 2) as charging_ratio
FROM ev_specifications
WHERE top_speed_kmh > 0 AND acceleration_0_100 > 0
ORDER BY performance_score DESC
LIMIT 15;

-- 8. Battery Technology Analysis
SELECT 
    CASE 
        WHEN battery_capacity_kwh < 40 THEN 'Small (< 40 kWh)'
        WHEN battery_capacity_kwh BETWEEN 40 AND 60 THEN 'Medium (40-60 kWh)'
        WHEN battery_capacity_kwh BETWEEN 60 AND 100 THEN 'Large (60-100 kWh)'
        ELSE 'Extra Large (> 100 kWh)'
    END as battery_category,
    COUNT(*) as model_count,
    COUNT(DISTINCT brand) as unique_brands,
    ROUND(AVG(battery_capacity_kwh), 2) as avg_battery_size,
    ROUND(AVG(range_km), 2) as avg_range_by_battery,
    ROUND(AVG(price), 2) as avg_price_by_battery,
    ROUND(AVG(efficiency_km_kwh), 2) as avg_efficiency_by_battery
FROM ev_specifications
GROUP BY 
    CASE 
        WHEN battery_capacity_kwh < 40 THEN 'Small (< 40 kWh)'
        WHEN battery_capacity_kwh BETWEEN 40 AND 60 THEN 'Medium (40-60 kWh)'
        WHEN battery_capacity_kwh BETWEEN 60 AND 100 THEN 'Large (60-100 kWh)'
        ELSE 'Extra Large (> 100 kWh)'
    END
ORDER BY avg_battery_size;

-- ============================================
-- BRAND COMPARISON QUERIES
-- ============================================

-- 9. Top Brands by Average Range
SELECT 
    brand,
    COUNT(*) as total_models,
    ROUND(AVG(range_km), 2) as avg_range,
    ROUND(MAX(range_km), 2) as max_range,
    ROUND(MIN(range_km), 2) as min_range,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(AVG(battery_capacity_kwh), 2) as avg_battery,
    COUNT(DISTINCT segment) as segments_covered
FROM ev_specifications
GROUP BY brand
HAVING total_models >= 3
ORDER BY avg_range DESC
LIMIT 10;

-- 10. Brand Price Positioning
SELECT 
    brand,
    COUNT(*) as total_models,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(MIN(price), 2) as entry_level_price,
    ROUND(MAX(price), 2) as premium_price,
    ROUND(AVG(range_km), 2) as avg_range,
    CASE 
        WHEN AVG(price) < 40000 THEN 'Budget Brand'
        WHEN AVG(price) BETWEEN 40000 AND 70000 THEN 'Mainstream Brand'
        WHEN AVG(price) BETWEEN 70000 AND 100000 THEN 'Premium Brand'
        ELSE 'Luxury Brand'
    END as brand_positioning
FROM ev_specifications
GROUP BY brand
ORDER BY avg_price;

-- 11. Brand Technology Leadership
SELECT 
    brand,
    COUNT(*) as total_models,
    ROUND(AVG(battery_capacity_kwh), 2) as avg_battery,
    ROUND(AVG(fast_charging_kw), 2) as avg_charging_speed,
    ROUND(AVG(efficiency_km_kwh), 2) as avg_efficiency,
    MAX(fast_charging_kw) as max_charging_speed,
    COUNT(CASE WHEN fast_charging_kw > 150 THEN 1 END) as ultra_fast_models,
    ROUND(AVG(top_speed_kmh), 2) as avg_top_speed
FROM ev_specifications
WHERE fast_charging_kw > 0
GROUP BY brand
ORDER BY avg_charging_speed DESC
LIMIT 10;

-- ============================================
-- SEGMENT ANALYSIS QUERIES
-- ============================================

-- 12. Segment-wise Analysis
SELECT 
    segment,
    COUNT(*) as total_models,
    COUNT(DISTINCT brand) as unique_brands,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(MIN(price), 2) as min_price_segment,
    ROUND(MAX(price), 2) as max_price_segment,
    ROUND(AVG(range_km), 2) as avg_range,
    ROUND(AVG(battery_capacity_kwh), 2) as avg_battery,
    ROUND(AVG(seats), 2) as avg_seats
FROM ev_specifications
WHERE segment IS NOT NULL AND segment != ''
GROUP BY segment
ORDER BY total_models DESC;

-- 13. Segment Price Range Analysis
SELECT 
    segment,
    price_category,
    COUNT(*) as model_count,
    ROUND(AVG(price), 2) as avg_price_in_segment,
    ROUND(AVG(range_km), 2) as avg_range_in_segment,
    COUNT(DISTINCT brand) as brands_in_segment
FROM (
    SELECT 
        segment,
        price,
        range_km,
        brand,
        CASE 
            WHEN price < 30000 THEN 'Budget'
            WHEN price BETWEEN 30000 AND 60000 THEN 'Mid-Range'
            WHEN price BETWEEN 60000 AND 100000 THEN 'Premium'
            ELSE 'Luxury'
        END as price_category
    FROM ev_specifications
    WHERE segment IS NOT NULL AND segment != ''
) as segment_data
GROUP BY segment, price_category
ORDER BY segment, avg_price_in_segment;

-- ============================================
-- CHARGING INFRASTRUCTURE ANALYSIS
-- ============================================

-- 14. Charging Infrastructure Overview
SELECT 
    'Charging Infrastructure' as metric,
    COUNT(*) as total_stations,
    COUNT(DISTINCT city) as cities_covered,
    COUNT(DISTINCT state) as states_covered,
    COUNT(DISTINCT country) as countries_covered,
    COALESCE(SUM(number_of_ports), 0) as total_ports,
    ROUND(AVG(power_kw), 2) as avg_power_kw,
    MAX(power_kw) as max_power_kw,
    COUNT(DISTINCT operator) as unique_operators
FROM charging_stations;

-- 15. City-wise Charging Infrastructure
SELECT 
    city,
    state,
    country,
    COUNT(*) as total_stations,
    COALESCE(SUM(number_of_ports), 0) as total_ports,
    ROUND(AVG(power_kw), 2) as avg_power_kw,
    MAX(power_kw) as max_power_kw,
    COUNT(DISTINCT operator) as unique_operators,
    GROUP_CONCAT(DISTINCT connector_types) as available_connectors
FROM charging_stations
GROUP BY city, state, country
ORDER BY total_stations DESC
LIMIT 20;

-- 16. Charging Power Analysis
SELECT 
    CASE 
        WHEN power_kw < 22 THEN 'Slow Charging (< 22 kW)'
        WHEN power_kw BETWEEN 22 AND 50 THEN 'Fast Charging (22-50 kW)'
        WHEN power_kw BETWEEN 50 AND 150 THEN 'Rapid Charging (50-150 kW)'
        ELSE 'Ultra-Fast Charging (> 150 kW)'
    END as charging_category,
    COUNT(*) as station_count,
    COUNT(DISTINCT city) as cities_covered,
    ROUND(AVG(number_of_ports), 2) as avg_ports_per_station,
    MAX(power_kw) as max_power_in_category
FROM charging_stations
WHERE power_kw > 0
GROUP BY 
    CASE 
        WHEN power_kw < 22 THEN 'Slow Charging (< 22 kW)'
        WHEN power_kw BETWEEN 22 AND 50 THEN 'Fast Charging (22-50 kW)'
        WHEN power_kw BETWEEN 50 AND 150 THEN 'Rapid Charging (50-150 kW)'
        ELSE 'Ultra-Fast Charging (> 150 kW)'
    END
ORDER BY avg_ports_per_station DESC;

-- ============================================
-- INDIA-SPECIFIC ANALYSIS
-- ============================================

-- 17. India EV Market Overview
SELECT 
    'India EV Market' as metric,
    COUNT(*) as total_models,
    COUNT(DISTINCT brand) as unique_brands,
    ROUND(AVG(price_inr), 2) as avg_price_inr,
    ROUND(AVG(price_usd), 2) as avg_price_usd,
    ROUND(AVG(range_km), 2) as avg_range,
    SUM(sales_2024) as total_sales_2024,
    SUM(sales_2023) as total_sales_2023,
    ROUND(AVG(market_share_percentage), 2) as avg_market_share
FROM ev_india_data
WHERE sales_2024 > 0;

-- 18. Top Selling EVs in India
SELECT 
    brand,
    model,
    price_inr,
    price_usd,
    range_km,
    battery_capacity_kwh,
    sales_2023,
    sales_2024,
    ROUND(((sales_2024 - sales_2023) / sales_2023) * 100, 2) as sales_growth_percentage,
    market_share_percentage,
    CASE 
        WHEN price_inr < 1000000 THEN 'Budget'
        WHEN price_inr BETWEEN 1000000 AND 2000000 THEN 'Mid-Range'
        WHEN price_inr BETWEEN 2000000 AND 4000000 THEN 'Premium'
        ELSE 'Luxury'
    END as price_category_inr
FROM ev_india_data
WHERE sales_2024 > 0
ORDER BY sales_2024 DESC
LIMIT 15;

-- 19. India Market Price Segmentation
SELECT 
    CASE 
        WHEN price_inr < 1000000 THEN 'Budget (< ₹10L)'
        WHEN price_inr BETWEEN 1000000 AND 2000000 THEN 'Mid-Range (₹10L-₹20L)'
        WHEN price_inr BETWEEN 2000000 AND 4000000 THEN 'Premium (₹20L-₹40L)'
        ELSE 'Luxury (> ₹40L)'
    END as price_segment,
    COUNT(*) as model_count,
    COUNT(DISTINCT brand) as unique_brands,
    ROUND(AVG(price_inr), 2) as avg_price_in_segment,
    ROUND(AVG(range_km), 2) as avg_range_in_segment,
    SUM(sales_2024) as total_sales_2024,
    ROUND(AVG(market_share_percentage), 2) as avg_market_share
FROM ev_india_data
WHERE sales_2024 > 0
GROUP BY 
    CASE 
        WHEN price_inr < 1000000 THEN 'Budget (< ₹10L)'
        WHEN price_inr BETWEEN 1000000 AND 2000000 THEN 'Mid-Range (₹10L-₹20L)'
        WHEN price_inr BETWEEN 2000000 AND 4000000 THEN 'Premium (₹20L-₹40L)'
        ELSE 'Luxury (> ₹40L)'
    END
ORDER BY total_sales_2024 DESC;

-- ============================================
-- ADVANCED ANALYTICS QUERIES
-- ============================================

-- 20. EV Affordability Index
SELECT 
    brand,
    model,
    price,
    range_km,
    battery_capacity_kwh,
    efficiency_km_kwh,
    ROUND((range_km * 1000) / price, 2) as affordability_index,
    ROUND(range_km / battery_capacity_kwh, 2) as battery_efficiency,
    ROUND(price / range_km, 2) as cost_per_km,
    CASE 
        WHEN price < 30000 THEN 'Budget'
        WHEN price BETWEEN 30000 AND 60000 THEN 'Mid-Range'
        WHEN price BETWEEN 60000 AND 100000 THEN 'Premium'
        ELSE 'Luxury'
    END as price_category,
    ROW_NUMBER() OVER (ORDER BY (range_km * 1000) / price DESC) as affordability_rank
FROM ev_specifications
WHERE price > 0 AND range_km > 0
ORDER BY affordability_index DESC;

-- 21. Technology Adoption Timeline
SELECT 
    year,
    COUNT(*) as new_models,
    COUNT(DISTINCT brand) as new_brands,
    ROUND(AVG(battery_capacity_kwh), 2) as avg_battery_new,
    ROUND(AVG(range_km), 2) as avg_range_new,
    ROUND(AVG(price), 2) as avg_price_new,
    LAG(COUNT(*)) OVER (ORDER BY year) as previous_year_models,
    ROUND(((COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY year)) / LAG(COUNT(*)) OVER (ORDER BY year)) * 100, 2) as year_over_year_growth
FROM ev_specifications
GROUP BY year
ORDER BY year;

-- 22. Market Saturation Analysis
SELECT 
    brand,
    COUNT(*) as total_models,
    COUNT(DISTINCT segment) as segments_covered,
    COUNT(DISTINCT year) as years_active,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(AVG(range_km), 2) as avg_range,
    ROUND(COUNT(DISTINCT segment) * 100.0 / (SELECT COUNT(DISTINCT segment) FROM ev_specifications WHERE segment IS NOT NULL), 2) as segment_coverage_percentage,
    CASE 
        WHEN COUNT(DISTINCT segment) >= 4 THEN 'Diversified Portfolio'
        WHEN COUNT(DISTINCT segment) >= 2 THEN 'Focused Portfolio'
        ELSE 'Specialized Portfolio'
    END as portfolio_strategy
FROM ev_specifications
WHERE segment IS NOT NULL AND segment != ''
GROUP BY brand
ORDER BY segment_coverage_percentage DESC;

-- ============================================
-- TABLEAU-SPECIFIC VIEWS
-- ============================================

-- 23. Comprehensive EV Dashboard View
CREATE OR REPLACE VIEW tableau_ev_dashboard AS
SELECT 
    s.brand,
    s.model,
    s.year,
    s.price,
    s.range_km,
    s.top_speed_kmh,
    s.acceleration_0_100,
    s.battery_capacity_kwh,
    s.efficiency_km_kwh,
    s.fast_charging_kw,
    s.drive_type,
    s.seats,
    s.body_type,
    s.segment,
    CASE 
        WHEN s.price < 30000 THEN 'Budget'
        WHEN s.price BETWEEN 30000 AND 60000 THEN 'Mid-Range'
        WHEN s.price BETWEEN 60000 AND 100000 THEN 'Premium'
        ELSE 'Luxury'
    END as price_category,
    CASE 
        WHEN s.range_km < 200 THEN 'Short Range'
        WHEN s.range_km BETWEEN 200 AND 400 THEN 'Medium Range'
        WHEN s.range_km BETWEEN 400 AND 600 THEN 'Long Range'
        ELSE 'Ultra Long Range'
    END as range_category,
    ROUND(s.price / s.range_km, 2) as price_per_km_range,
    ROUND(s.range_km / s.battery_capacity_kwh, 2) as range_per_kwh,
    ROUND((s.range_km * 1000) / s.price, 2) as value_score
FROM ev_specifications s;

-- 24. Charging Infrastructure Dashboard View
CREATE OR REPLACE VIEW tableau_charging_dashboard AS
SELECT 
    cs.station_name,
    cs.city,
    cs.state,
    cs.country,
    cs.latitude,
    cs.longitude,
    cs.power_kw,
    cs.number_of_ports,
    cs.station_type,
    cs.operator,
    cs.connector_types,
    cs.status,
    CASE 
        WHEN cs.power_kw < 22 THEN 'Slow Charging'
        WHEN cs.power_kw BETWEEN 22 AND 50 THEN 'Fast Charging'
        WHEN cs.power_kw BETWEEN 50 AND 150 THEN 'Rapid Charging'
        ELSE 'Ultra-Fast Charging'
    END as charging_speed_category
FROM charging_stations cs;

-- 25. India Market Dashboard View
CREATE OR REPLACE VIEW tableau_india_dashboard AS
SELECT 
    ei.brand,
    ei.model,
    ei.price_inr,
    ei.price_usd,
    ei.range_km,
    ei.battery_capacity_kwh,
    ei.sales_2023,
    ei.sales_2024,
    ROUND(((ei.sales_2024 - ei.sales_2023) / ei.sales_2023) * 100, 2) as sales_growth_percentage,
    ei.market_share_percentage,
    CASE 
        WHEN ei.price_inr < 1000000 THEN 'Budget'
        WHEN ei.price_inr BETWEEN 1000000 AND 2000000 THEN 'Mid-Range'
        WHEN ei.price_inr BETWEEN 2000000 AND 4000000 THEN 'Premium'
        ELSE 'Luxury'
    END as price_category_inr,
    ROUND(ei.price_inr / 100000, 2) as price_in_lakhs
FROM ev_india_data ei
WHERE ei.sales_2024 > 0;

-- ============================================
-- PERFORMANCE TESTING QUERIES
-- ============================================

-- 26. Query Performance Test - Large Dataset
SELECT 
    s.brand,
    s.model,
    s.price,
    s.range_km,
    s.battery_capacity_kwh,
    s.efficiency_km_kwh,
    s.segment,
    s.year,
    ROUND(s.price / s.range_km, 2) as cost_per_km
FROM ev_specifications s
WHERE s.price > 0 AND s.range_km > 0
ORDER BY cost_per_km ASC
LIMIT 100;

-- 27. Index Usage Verification
EXPLAIN SELECT 
    brand, 
    model, 
    price, 
    range_km, 
    battery_capacity_kwh
FROM ev_specifications
WHERE price BETWEEN 30000 AND 60000
AND range_km > 300
ORDER BY price;

-- ============================================
-- DATA VALIDATION QUERIES
-- ============================================

-- 28. Data Quality Check - EV Specifications
SELECT 
    'EV Specifications Data Quality' as check_type,
    COUNT(*) as total_records,
    COUNT(CASE WHEN price IS NULL OR price <= 0 THEN 1 END) as invalid_price,
    COUNT(CASE WHEN range_km IS NULL OR range_km <= 0 THEN 1 END) as invalid_range,
    COUNT(CASE WHEN battery_capacity_kwh IS NULL OR battery_capacity_kwh <= 0 THEN 1 END) as invalid_battery,
    COUNT(CASE WHEN brand IS NULL OR brand = '' THEN 1 END) as invalid_brand,
    COUNT(CASE WHEN model IS NULL OR model = '' THEN 1 END) as invalid_model,
    ROUND(AVG(price), 2) as avg_price_check,
    ROUND(AVG(range_km), 2) as avg_range_check
FROM ev_specifications;

-- 29. Data Quality Check - Charging Stations
SELECT 
    'Charging Stations Data Quality' as check_type,
    COUNT(*) as total_stations,
    COUNT(CASE WHEN latitude IS NULL OR longitude IS NULL THEN 1 END) as missing_coordinates,
    COUNT(CASE WHEN city IS NULL OR city = '' THEN 1 END) as missing_city,
    COUNT(CASE WHEN power_kw IS NULL OR power_kw <= 0 THEN 1 END) as invalid_power,
    COUNT(CASE WHEN number_of_ports IS NULL OR number_of_ports <= 0 THEN 1 END) as invalid_ports,
    COUNT(DISTINCT city) as unique_cities,
    COUNT(DISTINCT state) as unique_states
FROM charging_stations;

-- ============================================
-- EXPORT AND REPORTING QUERIES
-- ============================================

-- 30. Brand Performance Report
SELECT 
    s.brand,
    COUNT(*) as total_models,
    ROUND(AVG(s.price), 2) as average_price,
    ROUND(MIN(s.price), 2) as minimum_price,
    ROUND(MAX(s.price), 2) as maximum_price,
    ROUND(AVG(s.range_km), 2) as average_range,
    ROUND(MIN(s.range_km), 2) as minimum_range,
    ROUND(MAX(s.range_km), 2) as maximum_range,
    ROUND(AVG(s.battery_capacity_kwh), 2) as average_battery,
    COUNT(DISTINCT s.segment) as segments_covered,
    MIN(s.year) as first_model_year,
    MAX(s.year) as latest_model_year,
    COUNT(CASE WHEN s.price < 30000 THEN 1 END) as budget_models,
    COUNT(CASE WHEN s.price BETWEEN 30000 AND 60000 THEN 1 END) as mid_range_models,
    COUNT(CASE WHEN s.price BETWEEN 60000 AND 100000 THEN 1 END) as premium_models,
    COUNT(CASE WHEN s.price > 100000 THEN 1 END) as luxury_models
FROM ev_specifications s
GROUP BY s.brand
ORDER BY total_models DESC;
