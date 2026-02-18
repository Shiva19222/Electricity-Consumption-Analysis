#!/usr/bin/env python3
"""
Basic Tableau Data Preparation - Minimal Dependencies
Creates enhanced CSV for Tableau without any database connections
"""

import pandas as pd
import os
from datetime import datetime

def prepare_tableau_data():
    """Prepare data for Tableau with basic pandas"""
    print("🎊 Basic Tableau Data Preparation")
    print("="*50)
    
    # Check dataset
    csv_file = 'datasets/Consumption.csv'
    if not os.path.exists(csv_file):
        print(f"❌ Dataset not found: {csv_file}")
        print("Please ensure Consumption.csv is in the datasets folder")
        return False
    
    try:
        # Load data
        print("📊 Loading data...")
        df = pd.read_csv(csv_file)
        print(f"✅ Loaded {len(df)} records")
        
        # Basic date processing
        print("🔧 Processing dates...")
        df['dates'] = pd.to_datetime(df['Dates'], format='%d/%m/%Y', errors='coerce')
        df['year'] = df['dates'].dt.year
        df['month'] = df['dates'].dt.month
        df['month_name'] = df['dates'].dt.strftime('%B')
        df['quarter'] = df['dates'].dt.quarter
        df['quarter_name'] = 'Q' + df['quarter'].astype(str)
        
        # Basic seasonal classification
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Summer'
            elif month in [6, 7, 8, 9]:
                return 'Monsoon'
            else:
                return 'Post-Monsoon'
        
        df['season'] = df['month'].apply(get_season)
        
        # Basic lockdown detection
        df['is_lockdown'] = ((df['dates'] >= '2020-03-25') & (df['dates'] <= '2020-07-31'))
        df['lockdown_phase'] = df['is_lockdown'].apply(lambda x: 'Lockdown' if x else 'Normal')
        
        # Basic metro detection
        metro_states = ['Delhi', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'West Bengal', 'Telangana']
        df['is_metro'] = df['States'].isin(metro_states)
        
        # Clean data
        df = df.dropna(subset=['Usage', 'dates', 'States'])
        
        # Save enhanced data
        output_file = 'datasets/Tableau_Ready_Data.csv'
        df.to_csv(output_file, index=False)
        print(f"✅ Enhanced data saved: {output_file}")
        
        # Create simple summary
        print("📊 Creating summary...")
        summary = df.groupby(['year', 'Regions'])['Usage'].sum().reset_index()
        summary.to_csv('datasets/Quick_Summary.csv', index=False)
        print("✅ Summary saved: datasets/Quick_Summary.csv")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_simple_instructions():
    """Create simple Tableau instructions"""
    instructions = """
# Simple Tableau Instructions

## 📊 Files Created:
1. Tableau_Ready_Data.csv - Enhanced main dataset
2. Quick_Summary.csv - Quick summary by year and region

## 🔗 Tableau Steps:
1. Open Tableau Desktop
2. Click "Connect" → "To a File" → "Text File"
3. Select "Tableau_Ready_Data.csv"
4. Create visualizations:

### Required Visualizations (12):
1. 2019 State Consumption: Filter year=2019, bar chart by States
2. 2020 State Consumption: Filter year=2020, bar chart by States
3. Total Consumption: SUM(Usage) summary
4. Usage by Region: Pie chart by Regions
5. Top N States: Ranking by SUM(Usage)
6. Month-wise: Line chart by month_name
7. Regional Analysis: Map by Regions
8. Lockdown Impact: Compare is_lockdown=True/False
9. Region-wise States: Filled map by States
10. Quarter Usage: Bar chart by quarter_name
11. Metro Analysis: Filter is_metro=True
12. Year Comparison: Side-by-side bars by year

## 🚀 Next Steps:
1. Connect Tableau to CSV files
2. Create 12 visualizations
3. Build dashboard
4. Create story
5. Publish to Tableau Public
6. Update Flask app URLs
"""
    
    with open('datasets/Simple_Tableau_Guide.txt', 'w') as f:
        f.write(instructions)
    print("✅ Guide created: datasets/Simple_Tableau_Guide.txt")

def main():
    """Main function"""
    print("🎊 Basic Tableau Data Preparation")
    print("="*50)
    
    if prepare_tableau_data():
        create_simple_instructions()
        print("\n✅ Success! Files ready for Tableau")
        print("\n📋 Next Steps:")
        print("1. Open Tableau Desktop")
        print("2. Connect to: datasets/Tableau_Ready_Data.csv")
        print("3. Create 12 visualizations")
        print("4. Build dashboard and story")
        print("5. Publish to Tableau Public")
        print("\n📖 Guide: datasets/Simple_Tableau_Guide.txt")
    else:
        print("\n❌ Failed to prepare data")

if __name__ == "__main__":
    main()
