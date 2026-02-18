-- Electric Vehicle Analysis Database Schema
-- Comprehensive EV Market Analysis Project

-- Create database
CREATE DATABASE IF NOT EXISTS electric_vehicle_analysis;
USE electric_vehicle_analysis;

-- Electric Car Specifications Table (Main Dataset)
CREATE TABLE IF NOT EXISTS ev_specifications (
    spec_id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    range_km DECIMAL(8,2) NOT NULL,
    top_speed_kmh DECIMAL(8,2) NOT NULL,
    acceleration_0_100 DECIMAL(6,2) NOT NULL,
    battery_capacity_kwh DECIMAL(8,2) NOT NULL,
    efficiency_km_kwh DECIMAL(6,2) NOT NULL,
    fast_charging_kw DECIMAL(8,2) NOT NULL,
    drive_type VARCHAR(50),
    seats INT NOT NULL,
    body_type VARCHAR(50),
    segment VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_brand (brand),
    INDEX idx_year (year),
    INDEX idx_price (price),
    INDEX idx_range (range_km),
    INDEX idx_brand_model (brand, model)
);

-- Charging Stations Table
CREATE TABLE IF NOT EXISTS charging_stations (
    station_id INT AUTO_INCREMENT PRIMARY KEY,
    station_name VARCHAR(200) NOT NULL,
    address TEXT,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    station_type VARCHAR(50),
    power_kw DECIMAL(8,2),
    number_of_ports INT,
    connector_types TEXT,
    status VARCHAR(50),
    operator VARCHAR(100),
    opening_hours VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_city (city),
    INDEX idx_state (state),
    INDEX idx_location (latitude, longitude),
    INDEX idx_power (power_kw)
);

-- EV Market Database Table (Cheap Electric Cars)
CREATE TABLE IF NOT EXISTS ev_market_database (
    market_id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    price_usd DECIMAL(10,2) NOT NULL,
    price_local DECIMAL(10,2),
    currency VARCHAR(10),
    market VARCHAR(100),
    availability VARCHAR(50),
    delivery_time VARCHAR(100),
    warranty_years INT,
    battery_warranty_km INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_brand (brand),
    INDEX idx_price_usd (price_usd),
    INDEX idx_market (market)
);

-- India EV Specific Data Table
CREATE TABLE IF NOT EXISTS ev_india_data (
    india_id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    variant VARCHAR(100),
    price_inr DECIMAL(12,2) NOT NULL,
    price_usd DECIMAL(10,2),
    range_km DECIMAL(8,2),
    battery_capacity_kwh DECIMAL(8,2),
    charging_time_hours DECIMAL(6,2),
    top_speed_kmh DECIMAL(8,2),
    motor_power_kw DECIMAL(8,2),
    seating_capacity INT,
    boot_space_liters INT,
    safety_rating INT,
    launch_date DATE,
    sales_2023 INT,
    sales_2024 INT,
    market_share_percentage DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_brand (brand),
    INDEX idx_price_inr (price_inr),
    INDEX idx_sales_2024 (sales_2024),
    INDEX idx_launch_date (launch_date)
);

-- Brand Performance Summary Table
CREATE TABLE IF NOT EXISTS brand_performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(100) NOT NULL UNIQUE,
    total_models INT NOT NULL,
    avg_price DECIMAL(10,2) NOT NULL,
    avg_range DECIMAL(8,2) NOT NULL,
    price_range_min DECIMAL(10,2) NOT NULL,
    price_range_max DECIMAL(10,2) NOT NULL,
    range_min DECIMAL(8,2) NOT NULL,
    range_max DECIMAL(8,2) NOT NULL,
    market_share_percentage DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_market_share (market_share_percentage)
);

-- Charging Infrastructure Summary Table
CREATE TABLE IF NOT EXISTS charging_infrastructure (
    infra_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    total_stations INT NOT NULL,
    total_ports INT NOT NULL,
    avg_power_kw DECIMAL(8,2) NOT NULL,
    max_power_kw DECIMAL(8,2) NOT NULL,
    station_density_per_100k_population DECIMAL(8,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_city (city),
    INDEX idx_total_stations (total_stations)
);

-- Price Range Analysis Table
CREATE TABLE IF NOT EXISTS price_range_analysis (
    range_id INT AUTO_INCREMENT PRIMARY KEY,
    price_category VARCHAR(50) NOT NULL,
    min_price DECIMAL(10,2) NOT NULL,
    max_price DECIMAL(10,2) NOT NULL,
    avg_range DECIMAL(8,2) NOT NULL,
    model_count INT NOT NULL,
    top_brands TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_price_category (price_category)
);

-- Technology Trends Table
CREATE TABLE IF NOT EXISTS technology_trends (
    trend_id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    avg_battery_capacity DECIMAL(8,2) NOT NULL,
    avg_range DECIMAL(8,2) NOT NULL,
    avg_price DECIMAL(10,2) NOT NULL,
    total_models INT NOT NULL,
    new_brands INT NOT NULL,
    avg_efficiency DECIMAL(6,2) NOT NULL,
    avg_fast_charging DECIMAL(8,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_year (year)
);

-- Views for Tableau Integration

-- Comprehensive EV Analysis View
CREATE OR REPLACE VIEW v_ev_comprehensive_analysis AS
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
    ROUND(s.battery_capacity_kwh / s.range_km * 100, 2) as consumption_per_100km
FROM ev_specifications s;

-- Brand Comparison View
CREATE OR REPLACE VIEW v_brand_comparison AS
SELECT 
    s.brand,
    COUNT(*) as total_models,
    ROUND(AVG(s.price), 2) as avg_price,
    ROUND(MIN(s.price), 2) as min_price,
    ROUND(MAX(s.price), 2) as max_price,
    ROUND(AVG(s.range_km), 2) as avg_range,
    ROUND(MIN(s.range_km), 2) as min_range,
    ROUND(MAX(s.range_km), 2) as max_range,
    ROUND(AVG(s.battery_capacity_kwh), 2) as avg_battery,
    ROUND(AVG(s.efficiency_km_kwh), 2) as avg_efficiency,
    ROUND(AVG(s.fast_charging_kw), 2) as avg_charging_speed,
    COUNT(DISTINCT s.segment) as segments_covered,
    MIN(s.year) as first_model_year,
    MAX(s.year) as latest_model_year
FROM ev_specifications s
GROUP BY s.brand
ORDER BY total_models DESC;

-- Price vs Range Analysis View
CREATE OR REPLACE VIEW v_price_range_analysis AS
SELECT 
    s.brand,
    s.model,
    s.year,
    s.price,
    s.range_km,
    s.battery_capacity_kwh,
    s.efficiency_km_kwh,
    s.fast_charging_kw,
    ROUND(s.price / s.range_km, 2) as price_per_km_range,
    ROUND(s.range_km / s.battery_capacity_kwh, 2) as range_per_kwh,
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
    END as range_category
FROM ev_specifications s
ORDER BY s.price;

-- Charging Infrastructure View
CREATE OR REPLACE VIEW v_charging_infrastructure AS
SELECT 
    cs.city,
    cs.state,
    cs.country,
    COUNT(*) as total_stations,
    SUM(cs.number_of_ports) as total_ports,
    ROUND(AVG(cs.power_kw), 2) as avg_power_kw,
    MAX(cs.power_kw) as max_power_kw,
    COUNT(DISTINCT cs.operator) as unique_operators,
    COUNT(DISTINCT cs.connector_types) as connector_types_count,
    GROUP_CONCAT(DISTINCT cs.connector_types) as available_connectors
FROM charging_stations cs
GROUP BY cs.city, cs.state, cs.country
ORDER BY total_stations DESC;

-- India Market Analysis View
CREATE OR REPLACE VIEW v_india_market_analysis AS
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
    END as price_category_inr
FROM ev_india_data ei
WHERE ei.sales_2024 > 0
ORDER BY ei.sales_2024 DESC;

-- Technology Evolution View
CREATE OR REPLACE VIEW v_technology_evolution AS
SELECT 
    s.year,
    COUNT(*) as total_models,
    ROUND(AVG(s.battery_capacity_kwh), 2) as avg_battery_capacity,
    ROUND(AVG(s.range_km), 2) as avg_range,
    ROUND(AVG(s.price), 2) as avg_price,
    ROUND(AVG(s.efficiency_km_kwh), 2) as avg_efficiency,
    ROUND(AVG(s.fast_charging_kw), 2) as avg_charging_speed,
    COUNT(DISTINCT s.brand) as unique_brands,
    MIN(s.price) as min_price_year,
    MAX(s.price) as max_price_year,
    MIN(s.range_km) as min_range_year,
    MAX(s.range_km) as max_range_year
FROM ev_specifications s
GROUP BY s.year
ORDER BY s.year;

-- Stored Procedures for Data Analysis

DELIMITER //

-- Update Brand Performance Procedure
CREATE PROCEDURE UpdateBrandPerformance()
BEGIN
    INSERT INTO brand_performance (brand, total_models, avg_price, avg_range, price_range_min, price_range_max, range_min, range_max)
    SELECT 
        brand,
        COUNT(*),
        ROUND(AVG(price), 2),
        ROUND(AVG(range_km), 2),
        ROUND(MIN(price), 2),
        ROUND(MAX(price), 2),
        ROUND(MIN(range_km), 2),
        ROUND(MAX(range_km), 2)
    FROM ev_specifications
    GROUP BY brand
    ON DUPLICATE KEY UPDATE
        total_models = VALUES(total_models),
        avg_price = VALUES(avg_price),
        avg_range = VALUES(avg_range),
        price_range_min = VALUES(price_range_min),
        price_range_max = VALUES(price_range_max),
        range_min = VALUES(range_min),
        range_max = VALUES(range_max);
END //

-- Update Charging Infrastructure Summary Procedure
CREATE PROCEDURE UpdateChargingInfrastructure()
BEGIN
    INSERT INTO charging_infrastructure (city, state, total_stations, total_ports, avg_power_kw, max_power_kw)
    SELECT 
        city,
        state,
        COUNT(*),
        COALESCE(SUM(number_of_ports), 0),
        ROUND(AVG(power_kw), 2),
        MAX(power_kw)
    FROM charging_stations
    GROUP BY city, state
    ON DUPLICATE KEY UPDATE
        total_stations = VALUES(total_stations),
        total_ports = VALUES(total_ports),
        avg_power_kw = VALUES(avg_power_kw),
        max_power_kw = VALUES(max_power_kw);
END //

-- Update Technology Trends Procedure
CREATE PROCEDURE UpdateTechnologyTrends()
BEGIN
    INSERT INTO technology_trends (year, avg_battery_capacity, avg_range, avg_price, total_models, new_brands, avg_efficiency, avg_fast_charging)
    SELECT 
        year,
        ROUND(AVG(battery_capacity_kwh), 2),
        ROUND(AVG(range_km), 2),
        ROUND(AVG(price), 2),
        COUNT(*),
        COUNT(DISTINCT brand),
        ROUND(AVG(efficiency_km_kwh), 2),
        ROUND(AVG(fast_charging_kw), 2)
    FROM ev_specifications
    GROUP BY year
    ON DUPLICATE KEY UPDATE
        avg_battery_capacity = VALUES(avg_battery_capacity),
        avg_range = VALUES(avg_range),
        avg_price = VALUES(avg_price),
        total_models = VALUES(total_models),
        new_brands = VALUES(new_brands),
        avg_efficiency = VALUES(avg_efficiency),
        avg_fast_charging = VALUES(avg_fast_charging);
END //

DELIMITER ;

-- Create indexes for better performance
CREATE INDEX idx_ev_spec_brand_year ON ev_specifications(brand, year);
CREATE INDEX idx_charging_station_location ON charging_stations(latitude, longitude);
CREATE INDEX idx_ev_india_brand_sales ON ev_india_data(brand, sales_2024);

-- Show table structure
SHOW TABLES;
