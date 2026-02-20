#!/usr/bin/env python3
"""
Simple Tableau Data Import - No Database Required
Creates enhanced CSV files for Tableau direct import
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def enhance_data_for_tableau():
    """Enhance data for Tableau without database"""
    print("🎊 Simple Tableau Data Enhancement")
    print("="*50)
    
    # Load original data
    csv_file = 'datasets/Consumption.csv'
    if not os.path.exists(csv_file):
        print(f"❌ Dataset not found: {csv_file}")
        return False
    
    print("📊 Loading electricity consumption data...")
    df = pd.read_csv(csv_file)
    print(f"✅ Loaded {len(df)} records")
    
    # Create enhanced dataframe
    print("🔧 Enhancing data for Tableau...")
    
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
    
    # COVID-19 Lockdown periods
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
    
    # Clean data
    df['Usage'] = pd.to_numeric(df['Usage'], errors='coerce')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df = df.dropna(subset=['Usage', 'dates', 'States'])
    
    # Save enhanced data
    output_file = 'datasets/Consumption_Enhanced_Tableau.csv'
    df.to_csv(output_file, index=False)
    print(f"✅ Enhanced data saved to: {output_file}")
    
    # Create summary files for Tableau
    create_summary_files(df)
    
    return True

def create_summary_files(df):
    """Create summary files for Tableau"""
    print("📊 Creating summary files for Tableau...")
    
    # Yearly summary
    yearly_summary = df.groupby(['year']).agg({
        'Usage': ['sum', 'mean', 'min', 'max', 'count']
    }).round(2)
    yearly_summary.columns = ['Total_Usage', 'Avg_Usage', 'Min_Usage', 'Max_Usage', 'Record_Count']
    yearly_summary.to_csv('datasets/yearly_summary.csv')
    
    # Monthly summary
    monthly_summary = df.groupby(['year', 'month', 'month_name']).agg({
        'Usage': ['sum', 'mean', 'count']
    }).round(2)
    monthly_summary.columns = ['Total_Usage', 'Avg_Usage', 'Record_Count']
    monthly_summary.to_csv('datasets/monthly_summary.csv')
    
    # Regional summary
    regional_summary = df.groupby(['Regions', 'year']).agg({
        'Usage': ['sum', 'mean', 'count'],
        'States': 'nunique'
    }).round(2)
    regional_summary.columns = ['Total_Usage', 'Avg_Usage', 'Record_Count', 'State_Count']
    regional_summary.to_csv('datasets/regional_summary.csv')
    
    # State summary
    state_summary = df.groupby(['States', 'Regions', 'year']).agg({
        'Usage': ['sum', 'mean', 'min', 'max', 'count']
    }).round(2)
    state_summary.columns = ['Total_Usage', 'Avg_Usage', 'Min_Usage', 'Max_Usage', 'Record_Count']
    state_summary.to_csv('datasets/state_summary.csv')
    
    # Lockdown summary
    lockdown_summary = df.groupby(['is_lockdown', 'year']).agg({
        'Usage': ['sum', 'mean', 'count']
    }).round(2)
    lockdown_summary.columns = ['Total_Usage', 'Avg_Usage', 'Record_Count']
    lockdown_summary.to_csv('datasets/lockdown_summary.csv')
    
    print("✅ Summary files created:")
    print("   - yearly_summary.csv")
    print("   - monthly_summary.csv")
    print("   - regional_summary.csv")
    print("   - state_summary.csv")
    print("   - lockdown_summary.csv")

def create_tableau_guide():
    """Create Tableau connection guide"""
    guide = """
# Tableau Connection Guide - CSV Files

## 📊 Files Created:
1. Consumption_Enhanced_Tableau.csv - Main enhanced dataset
2. yearly_summary.csv - Yearly consumption summary
3. monthly_summary.csv - Monthly consumption summary
4. regional_summary.csv - Regional consumption summary
5. state_summary.csv - State consumption summary
6. lockdown_summary.csv - Lockdown impact summary

## 🔗 Tableau Connection Steps:

### Option 1: Connect to CSV Files
1. Open Tableau Desktop
2. Click "Connect" -> "To a File" -> "Text File"
3. Select "Consumption_Enhanced_Tableau.csv"
4. Tableau will automatically detect fields
5. Click "Sheet 1" to start creating visualizations

### Option 2: Connect Multiple CSV Files
1. Open Tableau Desktop
2. Click "Connect" -> "To a File" -> "Text File"
3. Select multiple CSV files (Ctrl+Click)
4. Use "Relationship" or "Union" to combine data
5. Create relationships based on common fields

## 📋 Available Fields:
- States, Regions, latitude, longitude
- dates, year, month, month_name, quarter, quarter_name
- day_of_week, day_name, week_of_year
- is_lockdown, lockdown_phase, season
- is_summer, is_winter, is_monsoon, is_metro
- usage_category, usage_level, Usage

## 🎯 Recommended Visualizations:
1. 2019 State Consumption - Bar chart
2. 2020 State Consumption - Bar chart
3. Total Consumption - Summary card
4. Usage by Region - Pie chart
5. Top N and Bottom N States - Ranking
6. Month-wise Consumption - Line chart
7. Regional Consumption - Heat map
8. Lockdown Impact - Comparison chart
9. Region-wise State Usage - Filled map
10. Quarter Usage - Bar chart
11. Metro City Usage - Scatter plot
12. Year-over-Year - Side-by-side bars

## 🚀 Next Steps:
1. Connect Tableau to the CSV files
2. Create the 12 required visualizations
3. Build interactive dashboard
4. Create 5-scene story
5. Publish to Tableau Public
6. Update Flask app with Tableau URLs
"""
    
    with open('datasets/tableau_connection_guide.txt', 'w') as f:
        f.write(guide)
    print("✅ Tableau connection guide created: datasets/tableau_connection_guide.txt")

def main():
    """Main function"""
    print("🎊 Simple Tableau Data Enhancement - No Database Required")
    print("="*60)
    
    # Enhance data
    if enhance_data_for_tableau():
        print("\n✅ Data enhancement completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Open Tableau Desktop")
        print("2. Connect to: datasets/Consumption_Enhanced_Tableau.csv")
        print("3. Create 12 required visualizations")
        print("4. Build dashboard and story")
        print("5. Publish to Tableau Public")
        print("6. Run Flask app: python tableau_flask_app.py")
        
        print("\n📊 Files Ready for Tableau:")
        print("- datasets/Consumption_Enhanced_Tableau.csv (Main data)")
        print("- datasets/yearly_summary.csv")
        print("- datasets/monthly_summary.csv")
        print("- datasets/regional_summary.csv")
        print("- datasets/state_summary.csv")
        print("- datasets/lockdown_summary.csv")
        
        print("\n📖 Guide: datasets/tableau_connection_guide.txt")
    else:
        print("❌ Data enhancement failed")

if __name__ == "__main__":
    main()
