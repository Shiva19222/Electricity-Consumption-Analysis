#!/usr/bin/env python3
"""
Tableau Electricity Consumption Data Import
Enhanced data processing for Tableau analysis
Supports both MySQL and SQL Server
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Database connections
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    print("Warning: MySQL connector not available. Install with: pip install mysql-connector-python")

try:
    import pyodbc
    SQLSERVER_AVAILABLE = True
except ImportError:
    SQLSERVER_AVAILABLE = False
    print("Warning: pyodbc not available. Install with: pip install pyodbc")

class TableauDataProcessor:
    def __init__(self, csv_file_path, db_type='mysql'):
        self.csv_file_path = csv_file_path
        self.db_type = db_type.lower()
        self.data = None
        self.processed_data = None
        
    def load_data(self):
        """Load CSV data"""
        try:
            print("📊 Loading electricity consumption data...")
            self.data = pd.read_csv(self.csv_file_path)
            print(f"✅ Loaded {len(self.data)} records")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def enhance_data(self):
        """Enhance data with Tableau-specific columns"""
        print("🔧 Enhancing data for Tableau analysis...")
        
        # Create a copy to avoid SettingWithCopyWarning
        df = self.data.copy()
        
        # Convert dates
        df['dates'] = pd.to_datetime(df['Dates'], format='%d/%m/%Y')
        
        # Extract date components
        df['year'] = df['dates'].dt.year
        df['month'] = df['dates'].dt.month
        df['month_name'] = df['dates'].dt.strftime('%B')
        df['quarter'] = df['dates'].dt.quarter
        df['quarter_name'] = 'Q' + df['quarter'].astype(str)
        df['day_of_week'] = df['dates'].dt.dayofweek
        df['day_name'] = df['dates'].dt.strftime('%A')
        df['week_of_year'] = df['dates'].dt.isocalendar().week
        
        # Season classification for India
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Summer'
            elif month in [6, 7, 8, 9]:
                return 'Monsoon'
            else:  # 10, 11
                return 'Post-Monsoon'
        
        df['season'] = df['month'].apply(get_season)
        df['is_summer'] = df['season'] == 'Summer'
        df['is_winter'] = df['season'] == 'Winter'
        df['is_monsoon'] = df['season'] == 'Monsoon'
        
        # COVID-19 Lockdown periods for India
        def get_lockdown_info(date):
            lockdown_periods = [
                ('2020-03-25', '2020-04-14', 'First Nationwide Lockdown'),
                ('2020-04-15', '2020-05-03', 'Second Nationwide Lockdown'),
                ('2020-05-04', '2020-05-18', 'Third Nationwide Lockdown'),
                ('2020-05-18', '2020-05-31', 'Fourth Nationwide Lockdown'),
                ('2020-06-01', '2020-06-30', 'Unlock Phase 1'),
                ('2020-07-01', '2020-07-31', 'Unlock Phase 2')
            ]
            
            for start, end, phase in lockdown_periods:
                if start <= date.strftime('%Y-%m-%d') <= end:
                    return True, phase
            return False, None
        
        lockdown_info = df['dates'].apply(lambda x: get_lockdown_info(x))
        df['is_lockdown'] = [info[0] for info in lockdown_info]
        df['lockdown_phase'] = [info[1] for info in lockdown_info]
        
        # Regional classification
        metro_cities = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
        df['is_metro'] = df['States'].isin(metro_cities)
        
        # Usage classification
        usage_stats = df['Usage'].describe()
        q1 = usage_stats['25%']
        q2 = usage_stats['50%']
        q3 = usage_stats['75%']
        
        def categorize_usage(usage):
            if usage <= q1:
                return 'Very Low', 'Critical'
            elif usage <= q2:
                return 'Low', 'Below Average'
            elif usage <= q3:
                return 'Medium', 'Average'
            else:
                return 'High', 'Above Average'
        
        usage_categories = df['Usage'].apply(categorize_usage)
        df['usage_category'] = [cat[0] for cat in usage_categories]
        df['usage_level'] = [level[1] for level in usage_categories]
        
        # Clean and standardize data
        df['Usage'] = pd.to_numeric(df['Usage'], errors='coerce')
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        
        # Remove rows with missing critical data
        df = df.dropna(subset=['Usage', 'dates', 'States'])
        
        self.processed_data = df
        print(f"✅ Enhanced data with {len(df)} records")
        return True
    
    def connect_mysql(self, host='localhost', user='root', password='', database='electricity_tableau_analysis'):
        """Connect to MySQL database"""
        if not MYSQL_AVAILABLE:
            raise Exception("MySQL connector not available")
        
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                charset='utf8mb4'
            )
            print("✅ Connected to MySQL database")
            return connection
        except Exception as e:
            print(f"❌ MySQL connection error: {e}")
            return None
    
    def connect_sqlserver(self, server='localhost\\SQLEXPRESS', database='electricity_tableau_analysis'):
        """Connect to SQL Server database"""
        if not SQLSERVER_AVAILABLE:
            raise Exception("SQL Server connector not available")
        
        try:
            connection_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
            connection = pyodbc.connect(connection_string)
            print("✅ Connected to SQL Server database")
            return connection
        except Exception as e:
            print(f"❌ SQL Server connection error: {e}")
            return None
    
    def import_to_mysql(self, connection):
        """Import data to MySQL"""
        try:
            cursor = connection.cursor()
            
            # Clear existing data
            print("🗑️ Clearing existing data...")
            cursor.execute("DELETE FROM consumption")
            connection.commit()
            
            # Prepare insert query
            insert_query = """
            INSERT INTO consumption (
                states, regions, latitude, longitude, dates, usage,
                year, month, month_name, quarter, quarter_name,
                day_of_week, day_name, week_of_year,
                is_lockdown, lockdown_phase, season,
                is_summer, is_winter, is_monsoon,
                is_metro, usage_category, usage_level
            ) VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s
            )
            """
            
            # Insert data in batches
            print("📥 Inserting data to MySQL...")
            batch_size = 1000
            total_rows = len(self.processed_data)
            
            for i in range(0, total_rows, batch_size):
                batch = self.processed_data.iloc[i:i+batch_size]
                
                data_to_insert = []
                for _, row in batch.iterrows():
                    data_to_insert.append((
                        row['States'], row['Regions'], row['latitude'], row['longitude'],
                        row['dates'], row['Usage'], row['year'], row['month'],
                        row['month_name'], row['quarter'], row['quarter_name'],
                        row['day_of_week'], row['day_name'], row['week_of_year'],
                        row['is_lockdown'], row['lockdown_phase'], row['season'],
                        row['is_summer'], row['is_winter'], row['is_monsoon'],
                        row['is_metro'], row['usage_category'], row['usage_level']
                    ))
                
                cursor.executemany(insert_query, data_to_insert)
                connection.commit()
                
                progress = min(i + batch_size, total_rows)
                print(f"📊 Progress: {progress}/{total_rows} ({progress/total_rows*100:.1f}%)")
            
            cursor.close()
            print(f"✅ Successfully imported {total_rows} records to MySQL")
            return True
            
        except Exception as e:
            print(f"❌ MySQL import error: {e}")
            return False
    
    def import_to_sqlserver(self, connection):
        """Import data to SQL Server"""
        try:
            cursor = connection.cursor()
            
            # Clear existing data
            print("🗑️ Clearing existing data...")
            cursor.execute("DELETE FROM consumption")
            connection.commit()
            
            # Prepare insert query
            insert_query = """
            INSERT INTO consumption (
                states, regions, latitude, longitude, dates, usage,
                year, month, month_name, quarter, quarter_name,
                day_of_week, day_name, week_of_year,
                is_lockdown, lockdown_phase, season,
                is_summer, is_winter, is_monsoon,
                is_metro, usage_category, usage_level
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Insert data in batches
            print("📥 Inserting data to SQL Server...")
            batch_size = 1000
            total_rows = len(self.processed_data)
            
            for i in range(0, total_rows, batch_size):
                batch = self.processed_data.iloc[i:i+batch_size]
                
                data_to_insert = []
                for _, row in batch.iterrows():
                    data_to_insert.append((
                        row['States'], row['Regions'], row['latitude'], row['longitude'],
                        row['dates'], row['Usage'], row['year'], row['month'],
                        row['month_name'], row['quarter'], row['quarter_name'],
                        row['day_of_week'], row['day_name'], row['week_of_year'],
                        row['is_lockdown'], row['lockdown_phase'], row['season'],
                        row['is_summer'], row['is_winter'], row['is_monsoon'],
                        row['is_metro'], row['usage_category'], row['usage_level']
                    ))
                
                cursor.executemany(insert_query, data_to_insert)
                connection.commit()
                
                progress = min(i + batch_size, total_rows)
                print(f"📊 Progress: {progress}/{total_rows} ({progress/total_rows*100:.1f}%)")
            
            cursor.close()
            print(f"✅ Successfully imported {total_rows} records to SQL Server")
            return True
            
        except Exception as e:
            print(f"❌ SQL Server import error: {e}")
            return False
    
    def import_data(self, **db_params):
        """Import data to database"""
        if self.processed_data is None:
            print("❌ No processed data available. Run enhance_data() first.")
            return False
        
        # Connect to database
        if self.db_type == 'mysql':
            connection = self.connect_mysql(**db_params)
            if connection:
                success = self.import_to_mysql(connection)
                connection.close()
                return success
        elif self.db_type == 'sqlserver':
            connection = self.connect_sqlserver(**db_params)
            if connection:
                success = self.import_to_sqlserver(connection)
                connection.close()
                return success
        else:
            print(f"❌ Unsupported database type: {self.db_type}")
            return False
    
    def generate_summary(self):
        """Generate data summary for Tableau documentation"""
        if self.processed_data is None:
            print("❌ No data available for summary")
            return
        
        print("\n📊 DATA SUMMARY FOR TABLEAU:")
        print("="*50)
        print(f"📈 Total Records: {len(self.processed_data):,}")
        print(f"🗓️ Date Range: {self.processed_data['dates'].min()} to {self.processed_data['dates'].max()}")
        print(f"🏛️ States: {self.processed_data['States'].nunique()}")
        print(f"🌍 Regions: {self.processed_data['Regions'].nunique()}")
        print(f"📊 Years: {sorted(self.processed_data['year'].unique())}")
        print(f"🌡️ Usage Range: {self.processed_data['Usage'].min():.2f} to {self.processed_data['Usage'].max():.2f}")
        print(f"🔒 Lockdown Records: {self.processed_data['is_lockdown'].sum():,}")
        print(f"🏙️ Metro Records: {self.processed_data['is_metro'].sum():,}")
        
        print("\n📊 USAGE BY YEAR:")
        yearly_usage = self.processed_data.groupby('year')['Usage'].agg(['sum', 'mean', 'count'])
        for year, stats in yearly_usage.iterrows():
            print(f"  {year}: {stats['sum']:,.2f} total, {stats['mean']:,.2f} avg, {stats['count']} records")
        
        print("\n📊 USAGE BY REGION:")
        regional_usage = self.processed_data.groupby('Regions')['Usage'].sum().sort_values(ascending=False)
        for region, usage in regional_usage.items():
            print(f"  {region}: {usage:,.2f}")
        
        print("\n📊 USAGE BY SEASON:")
        seasonal_usage = self.processed_data.groupby('season')['Usage'].agg(['sum', 'mean'])
        for season, stats in seasonal_usage.iterrows():
            print(f"  {season}: {stats['sum']:,.2f} total, {stats['mean']:,.2f} avg")

def main():
    """Main function"""
    print("🎊 Tableau Electricity Consumption Data Import")
    print("="*60)
    
    # Check if dataset exists
    csv_file = 'datasets/Consumption.csv'
    if not os.path.exists(csv_file):
        print(f"❌ Dataset not found: {csv_file}")
        print("Please ensure the dataset is in the datasets/ folder")
        return
    
    # Initialize processor
    processor = TableauDataProcessor(csv_file)
    
    # Load and enhance data
    if not processor.load_data():
        return
    
    if not processor.enhance_data():
        return
    
    # Generate summary
    processor.generate_summary()
    
    # Database selection
    print("\n🗄️ DATABASE SELECTION:")
    print("1. MySQL")
    print("2. SQL Server")
    
    choice = input("🤔 Choose database (1-2): ").strip()
    
    if choice == '1':
        # MySQL import
        print("\n🔧 MySQL Configuration:")
        host = input("Host (default: localhost): ").strip() or 'localhost'
        user = input("Username (default: root): ").strip() or 'root'
        password = input("Password (press Enter for none): ").strip()
        
        success = processor.import_data(
            host=host,
            user=user,
            password=password,
            database='electricity_tableau_analysis'
        )
        
        if success:
            print("\n✅ Data imported to MySQL successfully!")
            print("🎯 Ready for Tableau connection!")
            print("📊 Use the enhanced schema for comprehensive analysis")
    
    elif choice == '2':
        # SQL Server import
        print("\n🔧 SQL Server Configuration:")
        server = input("Server (default: localhost\\SQLEXPRESS): ").strip() or 'localhost\\SQLEXPRESS'
        
        success = processor.import_data(server=server)
        
        if success:
            print("\n✅ Data imported to SQL Server successfully!")
            print("🎯 Ready for Tableau connection!")
            print("📊 Use the enhanced schema for comprehensive analysis")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
