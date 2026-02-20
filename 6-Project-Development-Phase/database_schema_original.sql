-- Electricity Consumption Analysis Database Schema
-- Updated for Original Dataset Structure

-- Create database
CREATE DATABASE IF NOT EXISTS electricity_consumption;
USE electricity_consumption;

-- States table
CREATE TABLE IF NOT EXISTS states (
    state_id INT AUTO_INCREMENT PRIMARY KEY,
    state_name VARCHAR(100) NOT NULL UNIQUE,
    region VARCHAR(50) NOT NULL,
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Consumption table
CREATE TABLE IF NOT EXISTS consumption (
    consumption_id INT AUTO_INCREMENT PRIMARY KEY,
    state_id INT NOT NULL,
    consumption_date DATE NOT NULL,
    usage_value DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES states(state_id),
    INDEX idx_state_date (state_id, consumption_date),
    INDEX idx_date (consumption_date)
);

-- Regional summary table
CREATE TABLE IF NOT EXISTS regional_summary (
    summary_id INT AUTO_INCREMENT PRIMARY KEY,
    region VARCHAR(50) NOT NULL,
    summary_date DATE NOT NULL,
    total_usage DECIMAL(12,2) NOT NULL,
    average_usage DECIMAL(10,2) NOT NULL,
    max_usage DECIMAL(10,2) NOT NULL,
    min_usage DECIMAL(10,2) NOT NULL,
    state_count INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_region_date (region, summary_date)
);

-- Monthly trends table
CREATE TABLE IF NOT EXISTS monthly_trends (
    trend_id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    total_usage DECIMAL(12,2) NOT NULL,
    daily_average DECIMAL(10,2) NOT NULL,
    max_usage DECIMAL(10,2) NOT NULL,
    min_usage DECIMAL(10,2) NOT NULL,
    days_in_month INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_year_month (year, month)
);

-- Yearly summary table
CREATE TABLE IF NOT EXISTS yearly_summary (
    year_id INT AUTO_INCREMENT PRIMARY KEY,
    analysis_year INT NOT NULL,
    total_usage DECIMAL(12,2) NOT NULL,
    daily_average DECIMAL(10,2) NOT NULL,
    max_usage DECIMAL(10,2) NOT NULL,
    min_usage DECIMAL(10,2) NOT NULL,
    data_points INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_year (analysis_year)
);

-- Peak hours analysis table
CREATE TABLE IF NOT EXISTS peak_hours_analysis (
    peak_id INT AUTO_INCREMENT PRIMARY KEY,
    state_id INT NOT NULL,
    analysis_date DATE NOT NULL,
    peak_usage DECIMAL(10,2) NOT NULL,
    peak_hour INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES states(state_id),
    INDEX idx_state_peak (state_id, analysis_date)
);

-- Lockdown impact analysis table
CREATE TABLE IF NOT EXISTS lockdown_impact (
    impact_id INT AUTO_INCREMENT PRIMARY KEY,
    state_id INT NOT NULL,
    pre_lockdown_avg DECIMAL(10,2) NOT NULL,
    during_lockdown_avg DECIMAL(10,2) NOT NULL,
    post_lockdown_avg DECIMAL(10,2) NOT NULL,
    lockdown_impact_percentage DECIMAL(5,2) NOT NULL,
    recovery_percentage DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES states(state_id),
    INDEX idx_state_impact (state_id)
);

-- Performance metrics table
CREATE TABLE IF NOT EXISTS performance_metrics (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,2) NOT NULL,
    metric_unit VARCHAR(50) NOT NULL,
    calculation_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_metric_date (metric_name, calculation_date)
);

-- Views for Tableau integration

-- Regional consumption view
CREATE OR REPLACE VIEW v_regional_consumption AS
SELECT 
    s.region,
    YEAR(c.consumption_date) as analysis_year,
    MONTH(c.consumption_date) as analysis_month,
    SUM(c.usage_value) as regional_total,
    AVG(c.usage_value) as regional_average,
    MAX(c.usage_value) as regional_peak,
    MIN(c.usage_value) as regional_minimum,
    COUNT(DISTINCT s.state_id) as state_count
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.region, YEAR(c.consumption_date), MONTH(c.consumption_date);

-- State-wise yearly consumption view
CREATE OR REPLACE VIEW v_state_yearly_consumption AS
SELECT 
    s.state_name,
    s.region,
    YEAR(c.consumption_date) as analysis_year,
    SUM(c.usage_value) as total_consumption,
    AVG(c.usage_value) as average_consumption,
    MAX(c.usage_value) as peak_consumption,
    MIN(c.usage_value) as minimum_consumption,
    COUNT(*) as data_points
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region, YEAR(c.consumption_date);

-- Monthly trends view
CREATE OR REPLACE VIEW v_monthly_trends AS
SELECT 
    YEAR(c.consumption_date) as analysis_year,
    MONTH(c.consumption_date) as analysis_month,
    MONTHNAME(c.consumption_date) as month_name,
    SUM(c.usage_value) as monthly_total,
    AVG(c.usage_value) as daily_average,
    MAX(c.usage_value) as monthly_peak,
    MIN(c.usage_value) as monthly_minimum,
    COUNT(DISTINCT c.consumption_date) as days_in_month
FROM consumption c
GROUP BY YEAR(c.consumption_date), MONTH(c.consumption_date);

-- Top states by consumption view
CREATE OR REPLACE VIEW v_top_states_consumption AS
SELECT 
    s.state_name,
    s.region,
    SUM(c.usage_value) as total_consumption,
    AVG(c.usage_value) as average_consumption,
    MAX(c.usage_value) as peak_consumption,
    MIN(c.usage_value) as minimum_consumption,
    COUNT(*) as data_points,
    ROUND((SUM(c.usage_value) / (SELECT SUM(usage_value) FROM consumption)) * 100, 2) as market_share_percentage
FROM consumption c
JOIN states s ON c.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY total_consumption DESC;

-- Lockdown impact view
CREATE OR REPLACE VIEW v_lockdown_impact AS
SELECT 
    s.state_name,
    s.region,
    AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END) as pre_lockdown_avg,
    AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END) as during_lockdown_avg,
    AVG(CASE WHEN c.consumption_date > '2020-05-31' THEN c.usage_value END) as post_lockdown_avg,
    ROUND(
        ((AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END) - 
          AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END)) / 
         AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END)) * 100, 2
    ) as lockdown_impact_percentage
FROM consumption c
JOIN states s ON c.state_id = s.state_id
WHERE YEAR(c.consumption_date) = 2020
GROUP BY s.state_name, s.region;

-- Stored procedures for data processing

DELIMITER //

-- Update regional summary procedure
CREATE PROCEDURE UpdateRegionalSummary(IN target_date DATE)
BEGIN
    INSERT INTO regional_summary (region, summary_date, total_usage, average_usage, max_usage, min_usage, state_count)
    SELECT 
        s.region,
        target_date,
        SUM(c.usage_value),
        AVG(c.usage_value),
        MAX(c.usage_value),
        MIN(c.usage_value),
        COUNT(DISTINCT s.state_id)
    FROM consumption c
    JOIN states s ON c.state_id = s.state_id
    WHERE c.consumption_date = target_date
    GROUP BY s.region
    ON DUPLICATE KEY UPDATE
        total_usage = VALUES(total_usage),
        average_usage = VALUES(average_usage),
        max_usage = VALUES(max_usage),
        min_usage = VALUES(min_usage),
        state_count = VALUES(state_count);
END //

-- Update monthly trends procedure
CREATE PROCEDURE UpdateMonthlyTrends(IN target_year INT, IN target_month INT)
BEGIN
    INSERT INTO monthly_trends (year, month, month_name, total_usage, daily_average, max_usage, min_usage, days_in_month)
    SELECT 
        target_year,
        target_month,
        MONTHNAME(CONCAT(target_year, '-', target_month, '-01')),
        SUM(usage_value),
        AVG(usage_value),
        MAX(usage_value),
        MIN(usage_value),
        COUNT(DISTINCT consumption_date)
    FROM consumption
    WHERE YEAR(consumption_date) = target_year AND MONTH(consumption_date) = target_month
    GROUP BY target_year, target_month
    ON DUPLICATE KEY UPDATE
        total_usage = VALUES(total_usage),
        daily_average = VALUES(daily_average),
        max_usage = VALUES(max_usage),
        min_usage = VALUES(min_usage),
        days_in_month = VALUES(days_in_month);
END //

-- Update lockdown impact procedure
CREATE PROCEDURE UpdateLockdownImpact()
BEGIN
    INSERT INTO lockdown_impact (state_id, pre_lockdown_avg, during_lockdown_avg, post_lockdown_avg, lockdown_impact_percentage, recovery_percentage)
    SELECT 
        s.state_id,
        AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END),
        AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END),
        AVG(CASE WHEN c.consumption_date > '2020-05-31' THEN c.usage_value END),
        ROUND(
            ((AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END) - 
              AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END)) / 
             AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END)) * 100, 2
        ),
        ROUND(
            ((AVG(CASE WHEN c.consumption_date > '2020-05-31' THEN c.usage_value END) - 
              AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END)) / 
             AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END)) * 100, 2
        )
    FROM states s
    LEFT JOIN consumption c ON s.state_id = c.state_id
    WHERE YEAR(c.consumption_date) = 2020
    GROUP BY s.state_id
    ON DUPLICATE KEY UPDATE
        pre_lockdown_avg = VALUES(pre_lockdown_avg),
        during_lockdown_avg = VALUES(during_lockdown_avg),
        post_lockdown_avg = VALUES(post_lockdown_avg),
        lockdown_impact_percentage = VALUES(lockdown_impact_percentage),
        recovery_percentage = VALUES(recovery_percentage);
END //

DELIMITER ;

-- Insert states data based on original dataset
INSERT IGNORE INTO states (state_name, region, latitude, longitude) VALUES
('Punjab', 'NR', 31.51997398, 75.98000281),
('Haryana', 'NR', 28.45000633, 77.01999101),
('Rajasthan', 'NR', 26.44999921, 74.63998124),
('Delhi', 'NR', 28.6699929, 77.23000403),
('UP', 'NR', 27.59998069, 78.05000565),
('Uttarakhand', 'NR', 30.32040895, 78.05000565),
('HP', 'NR', 31.10002545, 77.16659704),
('J&K', 'NR', 33.45, 76.24),
('Chandigarh', 'NR', 30.71999697, 76.78000565),
('Chhattisgarh', 'WR', 22.09042035, 82.15998734),
('Gujarat', 'WR', 22.2587, 71.1924),
('MP', 'WR', 21.30039105, 76.13001949),
('Maharashtra', 'WR', 19.25023195, 73.16017493),
('Goa', 'WR', 15.491997, 73.81800065),
('DNH', 'WR', 20.26657819, 73.0166178),
('Andhra Pradesh', 'SR', 14.7504291, 78.57002559),
('Telangana', 'SR', 18.1124, 79.0193),
('Karnataka', 'SR', 12.57038129, 76.91999711),
('Kerala', 'SR', 8.900372741, 76.56999263),
('Tamil Nadu', 'SR', 12.92038576, 79.15004187),
('Pondy', 'SR', 11.93499371, 79.83000037),
('Bihar', 'ER', 25.78541445, 87.4799727),
('Jharkhand', 'ER', 23.80039349, 86.41998572),
('Odisha', 'ER', 19.82042971, 85.90001746),
('West Bengal', 'ER', 22.58039044, 88.32994665),
('Sikkim', 'ER', 27.3333303, 88.6166475),
('Arunachal Pradesh', 'NER', 27.10039878, 93.61660071),
('Assam', 'NER', 26.7499809, 94.21666744),
('Manipur', 'NER', 24.79997072, 93.95001705),
('Meghalaya', 'NER', 25.57049217, 91.8800142),
('Mizoram', 'NER', 23.71039899, 92.72001461),
('Nagaland', 'NER', 25.6669979, 94.11657019),
('Tripura', 'NER', 23.83540428, 91.27999914);

-- Create indexes for better performance
CREATE INDEX idx_consumption_date ON consumption(consumption_date);
CREATE INDEX idx_states_region ON states(region);
CREATE INDEX idx_regional_summary_date ON regional_summary(summary_date);
CREATE INDEX idx_monthly_trends_date ON monthly_trends(year, month);

-- Show table structure
SHOW TABLES;
