#!/usr/bin/env python3
"""
Data Import Script for Electricity Consumption Analysis
Updated for Original Dataset Structure
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Update with your MySQL password
    'database': 'electricity_consumption',
    'raise_on_warnings': True
}

def create_database_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            logging.info("Successfully connected to MySQL database")
            return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None

def parse_date(date_str):
    """Parse date in DD/MM/YYYY format"""
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').date()
    except ValueError:
        logging.error(f"Error parsing date: {date_str}")
        return None

def load_and_preprocess_data():
    """Load and preprocess the consumption data"""
    try:
        # Load the CSV file
        df = pd.read_csv('Consumption.csv')
        logging.info(f"Loaded dataset with {len(df)} records")
        
        # Display basic information
        logging.info(f"Columns: {list(df.columns)}")
        logging.info(f"Date range: {df['Dates'].min()} to {df['Dates'].max()}")
        logging.info(f"States/UTs: {df['States'].nunique()}")
        logging.info(f"Regions: {df['Regions'].unique()}")
        
        # Check for missing values
        missing_values = df.isnull().sum()
        if missing_values.any():
            logging.warning(f"Missing values found: {missing_values}")
        
        # Parse dates
        df['parsed_date'] = df['Dates'].apply(parse_date)
        
        # Remove rows with invalid dates
        invalid_dates = df['parsed_date'].isnull().sum()
        if invalid_dates > 0:
            logging.warning(f"Found {invalid_dates} records with invalid dates")
            df = df.dropna(subset=['parsed_date'])
        
        # Convert usage to numeric
        df['Usage'] = pd.to_numeric(df['Usage'], errors='coerce')
        
        # Remove rows with invalid usage values
        invalid_usage = df['Usage'].isnull().sum()
        if invalid_usage > 0:
            logging.warning(f"Found {invalid_usage} records with invalid usage values")
            df = df.dropna(subset=['Usage'])
        
        logging.info(f"After cleaning: {len(df)} valid records")
        return df
        
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None

def get_state_id(connection, state_name):
    """Get state ID from database"""
    try:
        cursor = connection.cursor()
        query = "SELECT state_id FROM states WHERE state_name = %s"
        cursor.execute(query, (state_name,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None
    except Error as e:
        logging.error(f"Error getting state ID for {state_name}: {e}")
        return None

def insert_consumption_data(connection, df):
    """Insert consumption data into database"""
    try:
        cursor = connection.cursor()
        
        # Prepare insert query
        insert_query = """
        INSERT INTO consumption (state_id, consumption_date, usage_value)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        usage_value = VALUES(usage_value)
        """
        
        # Count records to insert
        total_records = len(df)
        inserted_records = 0
        skipped_records = 0
        
        logging.info(f"Starting to insert {total_records} consumption records...")
        
        # Insert data row by row
        for index, row in df.iterrows():
            state_name = row['States']
            consumption_date = row['parsed_date']
            usage_value = row['Usage']
            
            # Get state ID
            state_id = get_state_id(connection, state_name)
            
            if state_id is None:
                logging.warning(f"State not found in database: {state_name}")
                skipped_records += 1
                continue
            
            # Insert record
            try:
                cursor.execute(insert_query, (state_id, consumption_date, usage_value))
                inserted_records += 1
                
                # Progress indicator
                if inserted_records % 1000 == 0:
                    logging.info(f"Inserted {inserted_records} records...")
                    
            except Error as e:
                logging.error(f"Error inserting record for {state_name} on {consumption_date}: {e}")
                skipped_records += 1
        
        # Commit changes
        connection.commit()
        cursor.close()
        
        logging.info(f"Successfully inserted {inserted_records} records")
        logging.info(f"Skipped {skipped_records} records")
        
        return inserted_records
        
    except Error as e:
        logging.error(f"Error inserting consumption data: {e}")
        connection.rollback()
        return 0

def update_summary_tables(connection):
    """Update summary tables and stored procedures"""
    try:
        cursor = connection.cursor()
        
        logging.info("Updating summary tables...")
        
        # Get unique dates from consumption data
        cursor.execute("SELECT DISTINCT consumption_date FROM consumption ORDER BY consumption_date")
        dates = cursor.fetchall()
        
        # Update regional summary for each date
        for date_tuple in dates:
            date = date_tuple[0]
            cursor.callproc('UpdateRegionalSummary', [date])
        
        # Get unique year-month combinations
        cursor.execute("""
            SELECT DISTINCT YEAR(consumption_date) as year, 
                          MONTH(consumption_date) as month 
            FROM consumption 
            ORDER BY year, month
        """)
        year_months = cursor.fetchall()
        
        # Update monthly trends for each year-month
        for year_month in year_months:
            year, month = year_month
            cursor.callproc('UpdateMonthlyTrends', [year, month])
        
        # Update lockdown impact
        cursor.callproc('UpdateLockdownImpact')
        
        connection.commit()
        cursor.close()
        
        logging.info("Summary tables updated successfully")
        
    except Error as e:
        logging.error(f"Error updating summary tables: {e}")
        connection.rollback()

def generate_data_insights(connection):
    """Generate and display data insights"""
    try:
        cursor = connection.cursor(dictionary=True)
        
        logging.info("Generating data insights...")
        
        # Total records
        cursor.execute("SELECT COUNT(*) as total_records FROM consumption")
        total_records = cursor.fetchone()['total_records']
        
        # Date range
        cursor.execute("SELECT MIN(consumption_date) as min_date, MAX(consumption_date) as max_date FROM consumption")
        date_range = cursor.fetchone()
        
        # States covered
        cursor.execute("SELECT COUNT(DISTINCT state_id) as states_covered FROM consumption")
        states_covered = cursor.fetchone()['states_covered']
        
        # Total consumption
        cursor.execute("SELECT SUM(usage_value) as total_consumption FROM consumption")
        total_consumption = cursor.fetchone()['total_consumption']
        
        # Average consumption
        cursor.execute("SELECT AVG(usage_value) as avg_consumption FROM consumption")
        avg_consumption = cursor.fetchone()['avg_consumption']
        
        # Peak consumption
        cursor.execute("SELECT MAX(usage_value) as peak_consumption FROM consumption")
        peak_consumption = cursor.fetchone()['peak_consumption']
        
        # Minimum consumption
        cursor.execute("SELECT MIN(usage_value) as min_consumption FROM consumption")
        min_consumption = cursor.fetchone()['min_consumption']
        
        # Regional breakdown
        cursor.execute("""
            SELECT s.region, SUM(c.usage_value) as regional_total
            FROM consumption c
            JOIN states s ON c.state_id = s.state_id
            GROUP BY s.region
            ORDER BY regional_total DESC
        """)
        regional_breakdown = cursor.fetchall()
        
        cursor.close()
        
        # Display insights
        print("\n" + "="*50)
        print("DATA INSIGHTS")
        print("="*50)
        print(f"Total Records: {total_records:,}")
        print(f"Date Range: {date_range['min_date']} to {date_range['max_date']}")
        print(f"States/UTs Covered: {states_covered}")
        print(f"Total Consumption: {total_consumption:,.2f} MWh")
        print(f"Average Daily Consumption: {avg_consumption:,.2f} MWh")
        print(f"Peak Consumption: {peak_consumption:,.2f} MWh")
        print(f"Minimum Consumption: {min_consumption:,.2f} MWh")
        
        print("\nRegional Breakdown:")
        for region in regional_breakdown:
            print(f"  {region['region']}: {region['regional_total']:,.2f} MWh")
        
        print("="*50)
        
    except Error as e:
        logging.error(f"Error generating insights: {e}")

def main():
    """Main function to import data"""
    logging.info("Starting data import process...")
    
    # Check if CSV file exists
    if not os.path.exists('Consumption.csv'):
        logging.error("Consumption.csv file not found!")
        return
    
    # Create database connection
    connection = create_database_connection()
    if not connection:
        logging.error("Failed to connect to database!")
        return
    
    try:
        # Load and preprocess data
        df = load_and_preprocess_data()
        if df is None:
            logging.error("Failed to load data!")
            return
        
        # Insert consumption data
        inserted_records = insert_consumption_data(connection, df)
        if inserted_records == 0:
            logging.error("No records were inserted!")
            return
        
        # Update summary tables
        update_summary_tables(connection)
        
        # Generate insights
        generate_data_insights(connection)
        
        logging.info("Data import completed successfully!")
        
    except Exception as e:
        logging.error(f"Error in main process: {e}")
        
    finally:
        if connection.is_connected():
            connection.close()
            logging.info("Database connection closed")

if __name__ == "__main__":
    main()
