#!/usr/bin/env python3
"""
EV Data Import Script for Electric Vehicle Analysis
Handles all 4 EV datasets with comprehensive data processing
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import logging
import os
from datetime import datetime

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
    'database': 'electric_vehicle_analysis',
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

def clean_numeric_value(value, default=0):
    """Clean and convert numeric values"""
    try:
        if pd.isna(value) or value == '' or value == '-':
            return default
        return float(str(value).replace(',', '').replace('$', '').strip())
    except:
        return default

def clean_string_value(value, default=''):
    """Clean string values"""
    try:
        if pd.isna(value) or value == '':
            return default
        return str(value).strip()
    except:
        return default

def import_ev_specifications(connection):
    """Import EV specifications data from ElectricCarData_Clean.csv"""
    try:
        logging.info("Importing EV specifications data...")
        
        # Load the main EV specifications dataset
        df = pd.read_csv('ElectricCarData_Clean.csv')
        logging.info(f"Loaded EV specifications: {len(df)} records")
        
        # Display column information
        logging.info(f"Columns: {list(df.columns)}")
        
        # Clean and preprocess data
        df_clean = pd.DataFrame()
        
        # Map common column names (adjust based on actual CSV structure)
        column_mapping = {
            'Brand': 'brand',
            'Model': 'model', 
            'Year': 'year',
            'Price': 'price',
            'Range': 'range_km',
            'TopSpeed': 'top_speed_kmh',
            'Acceleration': 'acceleration_0_100',
            'Battery': 'battery_capacity_kwh',
            'Efficiency': 'efficiency_km_kwh',
            'FastCharge': 'fast_charging_kw',
            'Drive': 'drive_type',
            'Seats': 'seats',
            'BodyStyle': 'body_type',
            'Segment': 'segment'
        }
        
        # Map columns based on actual CSV structure
        for col in df.columns:
            if col in column_mapping:
                df_clean[column_mapping[col]] = df[col]
        
        # Clean numeric columns
        numeric_columns = ['price', 'range_km', 'top_speed_kmh', 'acceleration_0_100', 
                        'battery_capacity_kwh', 'efficiency_km_kwh', 'fast_charging_kw', 'seats']
        
        for col in numeric_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].apply(clean_numeric_value)
        
        # Clean string columns
        string_columns = ['brand', 'model', 'drive_type', 'body_type', 'segment']
        for col in string_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].apply(clean_string_value)
        
        # Remove rows with missing essential data
        df_clean = df_clean.dropna(subset=['brand', 'model'])
        
        logging.info(f"After cleaning: {len(df_clean)} valid records")
        
        # Insert into database
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO ev_specifications 
        (brand, model, year, price, range_km, top_speed_kmh, acceleration_0_100, 
         battery_capacity_kwh, efficiency_km_kwh, fast_charging_kw, drive_type, 
         seats, body_type, segment)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        price = VALUES(price),
        range_km = VALUES(range_km),
        top_speed_kmh = VALUES(top_speed_kmh),
        acceleration_0_100 = VALUES(acceleration_0_100),
        battery_capacity_kwh = VALUES(battery_capacity_kwh),
        efficiency_km_kwh = VALUES(efficiency_km_kwh),
        fast_charging_kw = VALUES(fast_charging_kw),
        drive_type = VALUES(drive_type),
        seats = VALUES(seats),
        body_type = VALUES(body_type),
        segment = VALUES(segment)
        """
        
        inserted_count = 0
        for index, row in df_clean.iterrows():
            try:
                values = (
                    row.get('brand', ''),
                    row.get('model', ''),
                    int(row.get('year', 2020)),
                    row.get('price', 0),
                    row.get('range_km', 0),
                    row.get('top_speed_kmh', 0),
                    row.get('acceleration_0_100', 0),
                    row.get('battery_capacity_kwh', 0),
                    row.get('efficiency_km_kwh', 0),
                    row.get('fast_charging_kw', 0),
                    row.get('drive_type', ''),
                    int(row.get('seats', 5)),
                    row.get('body_type', ''),
                    row.get('segment', '')
                )
                cursor.execute(insert_query, values)
                inserted_count += 1
                
                if inserted_count % 100 == 0:
                    logging.info(f"Inserted {inserted_count} EV specifications...")
                    
            except Error as e:
                logging.warning(f"Error inserting EV spec {row.get('brand', 'Unknown')} {row.get('model', 'Unknown')}: {e}")
        
        connection.commit()
        cursor.close()
        logging.info(f"Successfully inserted {inserted_count} EV specifications")
        
    except Exception as e:
        logging.error(f"Error importing EV specifications: {e}")
        return False
    
    return True

def import_charging_stations(connection):
    """Import charging stations data"""
    try:
        logging.info("Importing charging stations data...")
        
        df = pd.read_csv('electric_vehicle_charging_station_list.csv')
        logging.info(f"Loaded charging stations: {len(df)} records")
        
        # Clean and preprocess data
        df_clean = pd.DataFrame()
        
        # Map columns (adjust based on actual CSV structure)
        column_mapping = {
            'StationName': 'station_name',
            'Address': 'address',
            'City': 'city',
            'State': 'state',
            'Country': 'country',
            'Latitude': 'latitude',
            'Longitude': 'longitude',
            'StationType': 'station_type',
            'Power': 'power_kw',
            'NumberOfPorts': 'number_of_ports',
            'ConnectorTypes': 'connector_types',
            'Status': 'status',
            'Operator': 'operator',
            'OpeningHours': 'opening_hours'
        }
        
        for col in df.columns:
            if col in column_mapping:
                df_clean[column_mapping[col]] = df[col]
        
        # Clean data
        if 'power_kw' in df_clean.columns:
            df_clean['power_kw'] = df_clean['power_kw'].apply(clean_numeric_value)
        if 'number_of_ports' in df_clean.columns:
            df_clean['number_of_ports'] = df_clean['number_of_ports'].apply(clean_numeric_value)
        
        string_columns = ['station_name', 'address', 'city', 'state', 'country', 
                       'station_type', 'connector_types', 'status', 'operator', 'opening_hours']
        for col in string_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].apply(clean_string_value)
        
        # Remove rows with missing essential data
        df_clean = df_clean.dropna(subset=['station_name', 'city'])
        
        logging.info(f"After cleaning: {len(df_clean)} valid charging stations")
        
        # Insert into database
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO charging_stations 
        (station_name, address, city, state, country, latitude, longitude, 
         station_type, power_kw, number_of_ports, connector_types, status, operator, opening_hours)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        address = VALUES(address),
        station_type = VALUES(station_type),
        power_kw = VALUES(power_kw),
        number_of_ports = VALUES(number_of_ports),
        connector_types = VALUES(connector_types),
        status = VALUES(status),
        operator = VALUES(operator),
        opening_hours = VALUES(opening_hours)
        """
        
        inserted_count = 0
        for index, row in df_clean.iterrows():
            try:
                values = (
                    row.get('station_name', ''),
                    row.get('address', ''),
                    row.get('city', ''),
                    row.get('state', ''),
                    row.get('country', ''),
                    row.get('latitude', 0),
                    row.get('longitude', 0),
                    row.get('station_type', ''),
                    row.get('power_kw', 0),
                    int(row.get('number_of_ports', 1)),
                    row.get('connector_types', ''),
                    row.get('status', ''),
                    row.get('operator', ''),
                    row.get('opening_hours', '')
                )
                cursor.execute(insert_query, values)
                inserted_count += 1
                
                if inserted_count % 100 == 0:
                    logging.info(f"Inserted {inserted_count} charging stations...")
                    
            except Error as e:
                logging.warning(f"Error inserting charging station {row.get('station_name', 'Unknown')}: {e}")
        
        connection.commit()
        cursor.close()
        logging.info(f"Successfully inserted {inserted_count} charging stations")
        
    except Exception as e:
        logging.error(f"Error importing charging stations: {e}")
        return False
    
    return True

def import_ev_market_database(connection):
    """Import EV market database (cheap electric cars)"""
    try:
        logging.info("Importing EV market database...")
        
        df = pd.read_csv('Cheapestelectriccars-EVDatabase.csv')
        logging.info(f"Loaded EV market database: {len(df)} records")
        
        # Clean and preprocess data
        df_clean = pd.DataFrame()
        
        # Map columns (adjust based on actual CSV structure)
        column_mapping = {
            'Brand': 'brand',
            'Model': 'model',
            'Year': 'year',
            'Price': 'price_usd',
            'PriceLocal': 'price_local',
            'Currency': 'currency',
            'Market': 'market',
            'Availability': 'availability',
            'DeliveryTime': 'delivery_time',
            'WarrantyYears': 'warranty_years',
            'BatteryWarrantyKm': 'battery_warranty_km'
        }
        
        for col in df.columns:
            if col in column_mapping:
                df_clean[column_mapping[col]] = df[col]
        
        # Clean numeric columns
        numeric_columns = ['price_usd', 'price_local', 'warranty_years', 'battery_warranty_km']
        for col in numeric_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].apply(clean_numeric_value)
        
        # Clean string columns
        string_columns = ['brand', 'model', 'currency', 'market', 'availability', 'delivery_time']
        for col in string_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].apply(clean_string_value)
        
        # Remove rows with missing essential data
        df_clean = df_clean.dropna(subset=['brand', 'model'])
        
        logging.info(f"After cleaning: {len(df_clean)} valid market records")
        
        # Insert into database
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO ev_market_database 
        (brand, model, year, price_usd, price_local, currency, market, 
         availability, delivery_time, warranty_years, battery_warranty_km)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        price_usd = VALUES(price_usd),
        price_local = VALUES(price_local),
        currency = VALUES(currency),
        market = VALUES(market),
        availability = VALUES(availability),
        delivery_time = VALUES(delivery_time),
        warranty_years = VALUES(warranty_years),
        battery_warranty_km = VALUES(battery_warranty_km)
        """
        
        inserted_count = 0
        for index, row in df_clean.iterrows():
            try:
                values = (
                    row.get('brand', ''),
                    row.get('model', ''),
                    int(row.get('year', 2020)),
                    row.get('price_usd', 0),
                    row.get('price_local', 0),
                    row.get('currency', ''),
                    row.get('market', ''),
                    row.get('availability', ''),
                    row.get('delivery_time', ''),
                    int(row.get('warranty_years', 0)),
                    int(row.get('battery_warranty_km', 0))
                )
                cursor.execute(insert_query, values)
                inserted_count += 1
                
                if inserted_count % 100 == 0:
                    logging.info(f"Inserted {inserted_count} market records...")
                    
            except Error as e:
                logging.warning(f"Error inserting market record {row.get('brand', 'Unknown')} {row.get('model', 'Unknown')}: {e}")
        
        connection.commit()
        cursor.close()
        logging.info(f"Successfully inserted {inserted_count} market records")
        
    except Exception as e:
        logging.error(f"Error importing EV market database: {e}")
        return False
    
    return True

def import_ev_india_data(connection):
    """Import India-specific EV data"""
    try:
        logging.info("Importing India EV data...")
        
        df = pd.read_csv('EVIndia.csv')
        logging.info(f"Loaded India EV data: {len(df)} records")
        
        # Clean and preprocess data
        df_clean = pd.DataFrame()
        
        # Map columns (adjust based on actual CSV structure)
        column_mapping = {
            'Brand': 'brand',
            'Model': 'model',
            'Variant': 'variant',
            'PriceINR': 'price_inr',
            'PriceUSD': 'price_usd',
            'Range': 'range_km',
            'Battery': 'battery_capacity_kwh',
            'ChargingTime': 'charging_time_hours',
            'TopSpeed': 'top_speed_kmh',
            'MotorPower': 'motor_power_kw',
            'SeatingCapacity': 'seating_capacity',
            'BootSpace': 'boot_space_liters',
            'SafetyRating': 'safety_rating',
            'LaunchDate': 'launch_date',
            'Sales2023': 'sales_2023',
            'Sales2024': 'sales_2024',
            'MarketShare': 'market_share_percentage'
        }
        
        for col in df.columns:
            if col in column_mapping:
                df_clean[column_mapping[col]] = df[col]
        
        # Clean numeric columns
        numeric_columns = ['price_inr', 'price_usd', 'range_km', 'battery_capacity_kwh', 
                        'charging_time_hours', 'top_speed_kmh', 'motor_power_kw', 
                        'seating_capacity', 'boot_space_liters', 'safety_rating', 
                        'sales_2023', 'sales_2024', 'market_share_percentage']
        
        for col in numeric_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].apply(clean_numeric_value)
        
        # Clean string columns
        string_columns = ['brand', 'model', 'variant']
        for col in string_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].apply(clean_string_value)
        
        # Handle date column
        if 'launch_date' in df_clean.columns:
            df_clean['launch_date'] = pd.to_datetime(df_clean['launch_date'], errors='coerce')
        
        # Remove rows with missing essential data
        df_clean = df_clean.dropna(subset=['brand', 'model'])
        
        logging.info(f"After cleaning: {len(df_clean)} valid India records")
        
        # Insert into database
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO ev_india_data 
        (brand, model, variant, price_inr, price_usd, range_km, battery_capacity_kwh, 
         charging_time_hours, top_speed_kmh, motor_power_kw, seating_capacity, 
         boot_space_liters, safety_rating, launch_date, sales_2023, sales_2024, market_share_percentage)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        price_inr = VALUES(price_inr),
        price_usd = VALUES(price_usd),
        range_km = VALUES(range_km),
        battery_capacity_kwh = VALUES(battery_capacity_kwh),
        charging_time_hours = VALUES(charging_time_hours),
        top_speed_kmh = VALUES(top_speed_kmh),
        motor_power_kw = VALUES(motor_power_kw),
        seating_capacity = VALUES(seating_capacity),
        boot_space_liters = VALUES(boot_space_liters),
        safety_rating = VALUES(safety_rating),
        launch_date = VALUES(launch_date),
        sales_2023 = VALUES(sales_2023),
        sales_2024 = VALUES(sales_2024),
        market_share_percentage = VALUES(market_share_percentage)
        """
        
        inserted_count = 0
        for index, row in df_clean.iterrows():
            try:
                values = (
                    row.get('brand', ''),
                    row.get('model', ''),
                    row.get('variant', ''),
                    row.get('price_inr', 0),
                    row.get('price_usd', 0),
                    row.get('range_km', 0),
                    row.get('battery_capacity_kwh', 0),
                    row.get('charging_time_hours', 0),
                    row.get('top_speed_kmh', 0),
                    row.get('motor_power_kw', 0),
                    int(row.get('seating_capacity', 5)),
                    int(row.get('boot_space_liters', 0)),
                    int(row.get('safety_rating', 0)),
                    row.get('launch_date'),
                    int(row.get('sales_2023', 0)),
                    int(row.get('sales_2024', 0)),
                    row.get('market_share_percentage', 0)
                )
                cursor.execute(insert_query, values)
                inserted_count += 1
                
                if inserted_count % 100 == 0:
                    logging.info(f"Inserted {inserted_count} India records...")
                    
            except Error as e:
                logging.warning(f"Error inserting India record {row.get('brand', 'Unknown')} {row.get('model', 'Unknown')}: {e}")
        
        connection.commit()
        cursor.close()
        logging.info(f"Successfully inserted {inserted_count} India records")
        
    except Exception as e:
        logging.error(f"Error importing India EV data: {e}")
        return False
    
    return True

def update_summary_tables(connection):
    """Update summary tables and run stored procedures"""
    try:
        cursor = connection.cursor()
        
        logging.info("Updating summary tables...")
        
        # Update brand performance
        cursor.callproc('UpdateBrandPerformance')
        
        # Update charging infrastructure
        cursor.callproc('UpdateChargingInfrastructure')
        
        # Update technology trends
        cursor.callproc('UpdateTechnologyTrends')
        
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
        
        logging.info("Generating EV data insights...")
        
        # EV specifications overview
        cursor.execute("SELECT COUNT(*) as total_models, COUNT(DISTINCT brand) as unique_brands FROM ev_specifications")
        ev_overview = cursor.fetchone()
        
        # Price range analysis
        cursor.execute("SELECT MIN(price) as min_price, MAX(price) as max_price, AVG(price) as avg_price FROM ev_specifications")
        price_analysis = cursor.fetchone()
        
        # Range analysis
        cursor.execute("SELECT MIN(range_km) as min_range, MAX(range_km) as max_range, AVG(range_km) as avg_range FROM ev_specifications")
        range_analysis = cursor.fetchone()
        
        # Charging stations overview
        cursor.execute("SELECT COUNT(*) as total_stations, COUNT(DISTINCT city) as cities_covered FROM charging_stations")
        charging_overview = cursor.fetchone()
        
        # India market overview
        cursor.execute("SELECT COUNT(*) as total_models, SUM(sales_2024) as total_sales_2024 FROM ev_india_data WHERE sales_2024 > 0")
        india_overview = cursor.fetchone()
        
        cursor.close()
        
        # Display insights
        print("\n" + "="*60)
        print("ELECTRIC VEHICLE ANALYSIS - DATA INSIGHTS")
        print("="*60)
        print(f"🚗 EV Specifications:")
        print(f"   Total Models: {ev_overview['total_models']:,}")
        print(f"   Unique Brands: {ev_overview['unique_brands']}")
        print(f"   Price Range: ${price_analysis['min_price']:,.0f} - ${price_analysis['max_price']:,.0f}")
        print(f"   Average Price: ${price_analysis['avg_price']:,.0f}")
        print(f"   Range Range: {range_analysis['min_range']:.0f} - {range_analysis['max_range']:.0f} km")
        print(f"   Average Range: {range_analysis['avg_range']:.0f} km")
        
        print(f"\n🔌 Charging Infrastructure:")
        print(f"   Total Stations: {charging_overview['total_stations']:,}")
        print(f"   Cities Covered: {charging_overview['cities_covered']:,}")
        
        if india_overview['total_models'] > 0:
            print(f"\n🇮🇳 India Market:")
            print(f"   Available Models: {india_overview['total_models']}")
            print(f"   Total Sales 2024: {india_overview['total_sales_2024']:,}")
        
        print("="*60)
        
    except Error as e:
        logging.error(f"Error generating insights: {e}")

def main():
    """Main function to import all EV data"""
    logging.info("Starting EV data import process...")
    
    # Check if required files exist
    required_files = [
        'ElectricCarData_Clean.csv',
        'electric_vehicle_charging_station_list.csv',
        'Cheapestelectriccars-EVDatabase.csv',
        'EVIndia.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        logging.error(f"Missing required files: {missing_files}")
        logging.error("Please download all 4 EV dataset files first!")
        return
    
    # Create database connection
    connection = create_database_connection()
    if not connection:
        logging.error("Failed to connect to database!")
        return
    
    try:
        # Import all datasets
        success_count = 0
        
        if import_ev_specifications(connection):
            success_count += 1
        
        if import_charging_stations(connection):
            success_count += 1
        
        if import_ev_market_database(connection):
            success_count += 1
        
        if import_ev_india_data(connection):
            success_count += 1
        
        logging.info(f"Successfully imported {success_count}/4 datasets")
        
        if success_count > 0:
            # Update summary tables
            update_summary_tables(connection)
            
            # Generate insights
            generate_data_insights(connection)
        
        logging.info("EV data import completed successfully!")
        
    except Exception as e:
        logging.error(f"Error in main import process: {e}")
        
    finally:
        if connection.is_connected():
            connection.close()
            logging.info("Database connection closed")

if __name__ == "__main__":
    main()
