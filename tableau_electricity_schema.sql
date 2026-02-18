-- =====================================================
-- Tableau-Based Electricity Consumption Analysis - Enhanced Schema
-- Supports both MySQL and SQL Server
-- =====================================================

-- For MySQL
CREATE DATABASE IF NOT EXISTS electricity_tableau_analysis;
USE electricity_tableau_analysis;

-- For SQL Server (uncomment if using SQL Server)
-- IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'electricity_tableau_analysis')
-- BEGIN
--     CREATE DATABASE electricity_tableau_analysis;
-- END
-- GO
-- USE electricity_tableau_analysis;
-- GO

-- =====================================================
-- Main Consumption Table - Enhanced for Tableau Analysis
-- =====================================================

-- MySQL Version
CREATE TABLE IF NOT EXISTS consumption (
    id INT AUTO_INCREMENT PRIMARY KEY,
    states VARCHAR(100) NOT NULL,
    regions VARCHAR(50) NOT NULL,
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(10,8) NOT NULL,
    dates DATE NOT NULL,
    usage DECIMAL(12,4) NOT NULL,
    
    -- Enhanced columns for Tableau analysis
    year INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INT NOT NULL,
    quarter_name VARCHAR(20) NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    week_of_year INT NOT NULL,
    
    -- COVID-19 Lockdown Analysis
    is_lockdown BOOLEAN DEFAULT FALSE,
    lockdown_phase VARCHAR(50),
    
    -- Seasonal Analysis
    season VARCHAR(20) NOT NULL,
    is_summer BOOLEAN DEFAULT FALSE,
    is_winter BOOLEAN DEFAULT FALSE,
    is_monsoon BOOLEAN DEFAULT FALSE,
    
    -- Regional Classification
    is_metro BOOLEAN DEFAULT FALSE,
    is_tier1 BOOLEAN DEFAULT FALSE,
    is_tier2 BOOLEAN DEFAULT FALSE,
    is_tier3 BOOLEAN DEFAULT FALSE,
    
    -- Usage Classification
    usage_category VARCHAR(20) NOT NULL,
    usage_level VARCHAR(20) NOT NULL,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes for Tableau Performance
    INDEX idx_dates (dates),
    INDEX idx_states (states),
    INDEX idx_regions (regions),
    INDEX idx_year (year),
    INDEX idx_month (month),
    INDEX idx_quarter (quarter),
    INDEX idx_usage (usage),
    INDEX idx_year_month (year, month),
    INDEX idx_state_year (states, year),
    INDEX idx_region_year (regions, year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SQL Server Version (uncomment if using SQL Server)
/*
CREATE TABLE consumption (
    id INT IDENTITY(1,1) PRIMARY KEY,
    states NVARCHAR(100) NOT NULL,
    regions NVARCHAR(50) NOT NULL,
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(10,8) NOT NULL,
    dates DATE NOT NULL,
    usage DECIMAL(12,4) NOT NULL,
    
    -- Enhanced columns for Tableau analysis
    year INT NOT NULL,
    month INT NOT NULL,
    month_name NVARCHAR(20) NOT NULL,
    quarter INT NOT NULL,
    quarter_name NVARCHAR(20) NOT NULL,
    day_of_week INT NOT NULL,
    day_name NVARCHAR(20) NOT NULL,
    week_of_year INT NOT NULL,
    
    -- COVID-19 Lockdown Analysis
    is_lockdown BIT DEFAULT 0,
    lockdown_phase NVARCHAR(50),
    
    -- Seasonal Analysis
    season NVARCHAR(20) NOT NULL,
    is_summer BIT DEFAULT 0,
    is_winter BIT DEFAULT 0,
    is_monsoon BIT DEFAULT 0,
    
    -- Regional Classification
    is_metro BIT DEFAULT 0,
    is_tier1 BIT DEFAULT 0,
    is_tier2 BIT DEFAULT 0,
    is_tier3 BIT DEFAULT 0,
    
    -- Usage Classification
    usage_category NVARCHAR(20) NOT NULL,
    usage_level NVARCHAR(20) NOT NULL,
    
    -- Timestamps
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Create indexes for SQL Server
CREATE INDEX idx_dates ON consumption(dates);
CREATE INDEX idx_states ON consumption(states);
CREATE INDEX idx_regions ON consumption(regions);
CREATE INDEX idx_year ON consumption(year);
CREATE INDEX idx_month ON consumption(month);
CREATE INDEX idx_quarter ON consumption(quarter);
CREATE INDEX idx_usage ON consumption(usage);
CREATE INDEX idx_year_month ON consumption(year, month);
CREATE INDEX idx_state_year ON consumption(states, year);
CREATE INDEX idx_region_year ON consumption(regions, year);
*/

-- =====================================================
-- Regional Reference Table
-- =====================================================

-- MySQL Version
CREATE TABLE IF NOT EXISTS regional_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL UNIQUE,
    region_code VARCHAR(10) NOT NULL,
    total_states INT NOT NULL,
    total_population BIGINT,
    area_sq_km DECIMAL(12,2),
    is_north BOOLEAN DEFAULT FALSE,
    is_south BOOLEAN DEFAULT FALSE,
    is_east BOOLEAN DEFAULT FALSE,
    is_west BOOLEAN DEFAULT FALSE,
    is_central BOOLEAN DEFAULT FALSE,
    is_northeast BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SQL Server Version (uncomment if using SQL Server)
/*
CREATE TABLE regional_info (
    id INT IDENTITY(1,1) PRIMARY KEY,
    region_name NVARCHAR(50) NOT NULL UNIQUE,
    region_code NVARCHAR(10) NOT NULL,
    total_states INT NOT NULL,
    total_population BIGINT,
    area_sq_km DECIMAL(12,2),
    is_north BIT DEFAULT 0,
    is_south BIT DEFAULT 0,
    is_east BIT DEFAULT 0,
    is_west BIT DEFAULT 0,
    is_central BIT DEFAULT 0,
    is_northeast BIT DEFAULT 0,
    
    created_at DATETIME DEFAULT GETDATE()
);
*/

-- =====================================================
-- State Reference Table
-- =====================================================

-- MySQL Version
CREATE TABLE IF NOT EXISTS state_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state_name VARCHAR(100) NOT NULL UNIQUE,
    state_code VARCHAR(10) NOT NULL,
    region VARCHAR(50) NOT NULL,
    capital VARCHAR(50),
    population BIGINT,
    area_sq_km DECIMAL(12,2),
    is_metro BOOLEAN DEFAULT FALSE,
    is_tier1 BOOLEAN DEFAULT FALSE,
    is_tier2 BOOLEAN DEFAULT FALSE,
    is_tier3 BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (region) REFERENCES regional_info(region_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SQL Server Version (uncomment if using SQL Server)
/*
CREATE TABLE state_info (
    id INT IDENTITY(1,1) PRIMARY KEY,
    state_name NVARCHAR(100) NOT NULL UNIQUE,
    state_code NVARCHAR(10) NOT NULL,
    region NVARCHAR(50) NOT NULL,
    capital NVARCHAR(50),
    population BIGINT,
    area_sq_km DECIMAL(12,2),
    is_metro BIT DEFAULT 0,
    is_tier1 BIT DEFAULT 0,
    is_tier2 BIT DEFAULT 0,
    is_tier3 BIT DEFAULT 0,
    
    created_at DATETIME DEFAULT GETDATE()
);
*/

-- =====================================================
-- Lockdown Periods Table (COVID-19 Analysis)
-- =====================================================

-- MySQL Version
CREATE TABLE IF NOT EXISTS lockdown_periods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lockdown_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    lockdown_level ENUM('National', 'State', 'District', 'City') NOT NULL,
    affected_states TEXT,
    description TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SQL Server Version (uncomment if using SQL Server)
/*
CREATE TABLE lockdown_periods (
    id INT IDENTITY(1,1) PRIMARY KEY,
    lockdown_name NVARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    lockdown_level NVARCHAR(50) NOT NULL,
    affected_states NVARCHAR(MAX),
    description NVARCHAR(MAX),
    
    created_at DATETIME DEFAULT GETDATE()
);
*/

-- =====================================================
-- Insert Reference Data
-- =====================================================

-- Regional Data
INSERT INTO regional_info (region_name, region_code, total_states, is_north, is_south, is_east, is_west, is_central, is_northeast) VALUES
('North', 'N', 8, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE),
('South', 'S', 5, FALSE, TRUE, FALSE, FALSE, FALSE, FALSE),
('East', 'E', 8, FALSE, FALSE, TRUE, FALSE, FALSE, FALSE),
('West', 'W', 4, FALSE, FALSE, FALSE, TRUE, FALSE, FALSE),
('Central', 'C', 2, FALSE, FALSE, FALSE, FALSE, TRUE, FALSE),
('Northeast', 'NE', 8, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE);

-- Lockdown Periods (COVID-19)
INSERT INTO lockdown_periods (lockdown_name, start_date, end_date, lockdown_level, affected_states, description) VALUES
('First Nationwide Lockdown', '2020-03-25', '2020-04-14', 'National', 'All States', 'Complete nationwide lockdown'),
('Second Nationwide Lockdown', '2020-04-15', '2020-05-03', 'National', 'All States', 'Extended nationwide lockdown'),
('Third Nationwide Lockdown', '2020-05-04', '2020-05-18', 'National', 'All States', 'Partial nationwide lockdown'),
('Fourth Nationwide Lockdown', '2020-05-18', '2020-05-31', 'National', 'All States', 'Relaxed nationwide lockdown'),
('Unlock Phase 1', '2020-06-01', '2020-06-30', 'National', 'All States', 'Gradual reopening phase 1'),
('Unlock Phase 2', '2020-07-01', '2020-07-31', 'National', 'All States', 'Gradual reopening phase 2');

-- =====================================================
-- Views for Tableau Analysis
-- =====================================================

-- View 1: Year-over-Year Comparison
CREATE OR REPLACE VIEW yearly_consumption AS
SELECT 
    year,
    SUM(usage) as total_usage,
    AVG(usage) as avg_usage,
    MIN(usage) as min_usage,
    MAX(usage) as max_usage,
    COUNT(*) as record_count
FROM consumption
GROUP BY year
ORDER BY year;

-- View 2: Monthly Trends
CREATE OR REPLACE VIEW monthly_consumption AS
SELECT 
    year,
    month,
    month_name,
    SUM(usage) as total_usage,
    AVG(usage) as avg_usage,
    MIN(usage) as min_usage,
    MAX(usage) as max_usage,
    COUNT(*) as record_count
FROM consumption
GROUP BY year, month, month_name
ORDER BY year, month;

-- View 3: Regional Analysis
CREATE OR REPLACE VIEW regional_consumption AS
SELECT 
    regions,
    year,
    SUM(usage) as total_usage,
    AVG(usage) as avg_usage,
    COUNT(DISTINCT states) as state_count,
    COUNT(*) as record_count
FROM consumption
GROUP BY regions, year
ORDER BY regions, year;

-- View 4: State-wise Analysis
CREATE OR REPLACE VIEW state_consumption AS
SELECT 
    states,
    regions,
    year,
    SUM(usage) as total_usage,
    AVG(usage) as avg_usage,
    MIN(usage) as min_usage,
    MAX(usage) as max_usage,
    COUNT(*) as record_count
FROM consumption
GROUP BY states, regions, year
ORDER BY regions, total_usage DESC;

-- View 5: Lockdown Impact Analysis
CREATE OR REPLACE VIEW lockdown_impact AS
SELECT 
    states,
    regions,
    is_lockdown,
    SUM(usage) as total_usage,
    AVG(usage) as avg_usage,
    COUNT(*) as record_count
FROM consumption
GROUP BY states, regions, is_lockdown
ORDER BY regions, is_lockdown DESC;

-- View 6: Seasonal Analysis
CREATE OR REPLACE VIEW seasonal_consumption AS
SELECT 
    season,
    year,
    SUM(usage) as total_usage,
    AVG(usage) as avg_usage,
    COUNT(*) as record_count
FROM consumption
GROUP BY season, year
ORDER BY season, year;

-- View 7: Top N States by Usage
CREATE OR REPLACE VIEW top_states_by_usage AS
SELECT 
    states,
    regions,
    SUM(usage) as total_usage,
    AVG(usage) as avg_usage,
    RANK() OVER (ORDER BY SUM(usage) DESC) as usage_rank
FROM consumption
GROUP BY states, regions
ORDER BY total_usage DESC;

-- View 8: Bottom N States by Usage
CREATE OR REPLACE VIEW bottom_states_by_usage AS
SELECT 
    states,
    regions,
    SUM(usage) as total_usage,
    AVG(usage) as avg_usage,
    RANK() OVER (ORDER BY SUM(usage) ASC) as usage_rank
FROM consumption
GROUP BY states, regions
ORDER BY total_usage ASC;

-- =====================================================
-- Stored Procedures for Tableau Data Refresh
-- =====================================================

-- MySQL Version
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS refresh_tableau_data()
BEGIN
    -- Refresh materialized views or aggregated tables
    -- This can be called from Tableau for data refresh
    SELECT 'Tableau data refresh completed' as status;
END //

DELIMITER ;

-- SQL Server Version (uncomment if using SQL Server)
/*
CREATE PROCEDURE refresh_tableau_data
AS
BEGIN
    -- Refresh materialized views or aggregated tables
    -- This can be called from Tableau for data refresh
    SELECT 'Tableau data refresh completed' as status;
END
GO
*/

-- =====================================================
-- Sample Data Validation Queries
-- =====================================================

-- Query 1: Check data completeness
SELECT 
    'Data Completeness Check' as metric,
    COUNT(*) as total_records,
    COUNT(DISTINCT states) as unique_states,
    COUNT(DISTINCT regions) as unique_regions,
    MIN(dates) as start_date,
    MAX(dates) as end_date,
    SUM(usage) as total_usage
FROM consumption;

-- Query 2: Check lockdown data
SELECT 
    'Lockdown Data Check' as metric,
    COUNT(CASE WHEN is_lockdown = TRUE THEN 1 END) as lockdown_records,
    COUNT(CASE WHEN is_lockdown = FALSE THEN 1 END) as normal_records,
    ROUND(COUNT(CASE WHEN is_lockdown = TRUE THEN 1 END) * 100.0 / COUNT(*), 2) as lockdown_percentage
FROM consumption;

-- =====================================================
-- Performance Optimization for Tableau
-- =====================================================

-- Create summary tables for faster Tableau performance
CREATE TABLE IF NOT EXISTS consumption_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    states VARCHAR(100) NOT NULL,
    regions VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    quarter INT NOT NULL,
    total_usage DECIMAL(12,4) NOT NULL,
    avg_usage DECIMAL(12,4) NOT NULL,
    min_usage DECIMAL(12,4) NOT NULL,
    max_usage DECIMAL(12,4) NOT NULL,
    record_count INT NOT NULL,
    
    INDEX idx_year_month (year, month),
    INDEX idx_state_year (states, year),
    INDEX idx_region_year (regions, year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Populate summary table
INSERT INTO consumption_summary (states, regions, year, month, quarter, total_usage, avg_usage, min_usage, max_usage, record_count)
SELECT 
    states,
    regions,
    year,
    month,
    quarter,
    SUM(usage) as total_usage,
    AVG(usage) as avg_usage,
    MIN(usage) as min_usage,
    MAX(usage) as max_usage,
    COUNT(*) as record_count
FROM consumption
GROUP BY states, regions, year, month, quarter;

-- =====================================================
-- Tableau Connection Information
-- =====================================================

-- Connection string for MySQL:
-- Server: localhost
-- Port: 3306
-- Database: electricity_tableau_analysis
-- Username: root
-- Password: [your_password]

-- Connection string for SQL Server:
-- Server: localhost\SQLEXPRESS
-- Database: electricity_tableau_analysis
-- Authentication: Windows Authentication or SQL Server Authentication
-- Username: [your_username]
-- Password: [your_password]

-- =====================================================
-- Tableau Recommended Fields
-- =====================================================

-- Dimensions:
-- states, regions, dates, year, month, month_name, quarter, quarter_name
-- day_of_week, day_name, week_of_year, season, lockdown_phase
-- usage_category, usage_level, is_metro, is_lockdown

-- Measures:
-- usage, total_usage, avg_usage, min_usage, max_usage
-- record_count, state_count, usage_rank

-- Recommended Tableau Calculations:
-- 1. Year-over-Year Growth: (SUM([usage]) - LOOKUP(SUM([usage]), -1)) / LOOKUP(SUM([usage]), -1)
-- 2. Month-over-Month Growth: (SUM([usage]) - LOOKUP(SUM([usage]), -1)) / LOOKUP(SUM([usage]), -1)
-- 3. Lockdown Impact: SUM(IF [is_lockdown] THEN [usage] END) / SUM([usage])
-- 4. Seasonal Index: SUM([usage]) / WINDOW_AVG(SUM([usage]))
-- 5. Top N Performance: RANK(SUM([usage]), 'desc')

SELECT 'Tableau Schema Setup Complete' as status;
