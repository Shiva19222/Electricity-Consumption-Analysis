-- =====================================================
-- SQL Server Version - Tableau Electricity Analysis
-- Execute in SQL Server Management Studio
-- =====================================================

-- Create database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'electricity_tableau_analysis')
BEGIN
    CREATE DATABASE electricity_tableau_analysis;
END
GO

USE electricity_tableau_analysis;
GO

-- Create consumption table
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
GO

-- Create indexes
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
GO

-- Insert regional data
INSERT INTO regional_info (region_name, region_code, total_states, is_north, is_south, is_east, is_west, is_central, is_northeast) VALUES
('North', 'N', 8, 1, 0, 0, 0, 0, 0),
('South', 'S', 5, 0, 1, 0, 0, 0, 0),
('East', 'E', 8, 0, 0, 1, 0, 0, 0),
('West', 'W', 4, 0, 0, 0, 1, 0, 0),
('Central', 'C', 2, 0, 0, 0, 0, 1, 0),
('Northeast', 'NE', 8, 0, 0, 0, 0, 0, 1);
GO

-- Insert lockdown periods
INSERT INTO lockdown_periods (lockdown_name, start_date, end_date, lockdown_level, affected_states, description) VALUES
('First Nationwide Lockdown', '2020-03-25', '2020-04-14', 'National', 'All States', 'Complete nationwide lockdown'),
('Second Nationwide Lockdown', '2020-04-15', '2020-05-03', 'National', 'All States', 'Extended nationwide lockdown'),
('Third Nationwide Lockdown', '2020-05-04', '2020-05-18', 'National', 'All States', 'Partial nationwide lockdown'),
('Fourth Nationwide Lockdown', '2020-05-18', '2020-05-31', 'National', 'All States', 'Relaxed nationwide lockdown'),
('Unlock Phase 1', '2020-06-01', '2020-06-30', 'National', 'All States', 'Gradual reopening phase 1'),
('Unlock Phase 2', '2020-07-01', '2020-07-31', 'National', 'All States', 'Gradual reopening phase 2');
GO

PRINT 'SQL Server schema created successfully!';
PRINT 'Ready for data import with tableau_data_import.py';
PRINT 'Choose option 2 for SQL Server when running the import script';
