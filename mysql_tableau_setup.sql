-- MySQL Setup for Tableau Connection
-- Execute in MySQL Workbench

-- Create database
CREATE DATABASE IF NOT EXISTS electricity_tableau_analysis;
USE electricity_tableau_analysis;

-- Create consumption table
CREATE TABLE IF NOT EXISTS consumption (
    id INT AUTO_INCREMENT PRIMARY KEY,
    states VARCHAR(100) NOT NULL,
    regions VARCHAR(50) NOT NULL,
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(10,8) NOT NULL,
    dates DATE NOT NULL,
    usage DECIMAL(12,4) NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INT NOT NULL,
    quarter_name VARCHAR(20) NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    week_of_year INT NOT NULL,
    is_lockdown BOOLEAN DEFAULT FALSE,
    lockdown_phase VARCHAR(50),
    season VARCHAR(20) NOT NULL,
    is_summer BOOLEAN DEFAULT FALSE,
    is_winter BOOLEAN DEFAULT FALSE,
    is_monsoon BOOLEAN DEFAULT FALSE,
    is_metro BOOLEAN DEFAULT FALSE,
    usage_category VARCHAR(20) NOT NULL,
    usage_level VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_dates ON consumption(dates);
CREATE INDEX idx_states ON consumption(states);
CREATE INDEX idx_regions ON consumption(regions);
CREATE INDEX idx_year ON consumption(year);
CREATE INDEX idx_month ON consumption(month);
CREATE INDEX idx_usage ON consumption(usage);

-- Import data (run this after creating table)
LOAD DATA LOCAL INFILE 'datasets/Tableau_Ready_Data.csv'
INTO TABLE consumption
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT 'Tableau setup completed!' as status;
