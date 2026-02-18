#!/usr/bin/env python3
"""
Professional Housing Market Analysis Project
Real Estate Analytics - Property Market Trends
"""

import os
import sys
import subprocess
from datetime import datetime

def check_requirements():
    """Check if required files exist"""
    print("🔍 Checking housing market project requirements...")
    
    # Check dataset
    dataset_path = '../../datasets/housing_market_data.csv'
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found: {dataset_path}")
        return False
    
    print("✅ Housing market dataset found")
    return True

def create_basic_structure():
    """Create basic project structure"""
    print("🏗️ Creating housing market project structure...")
    
    # Create basic files
    files_to_create = {
        'README.md': '''# 🏠 Housing Market Analysis

## 🎯 Project Overview
Real estate market trends and property price predictions.

## 📊 Dataset
- **Source:** housing_market_data.csv (2.4 MB)
- **Focus:** Property prices, market trends
- **Domain:** Real Estate Analytics

## 🚀 Quick Start
```bash
python run.py
```

## 📋 Features
- Price Trends Analysis
- Location Analysis
- Market Predictions
- Property Valuation
''',
        'app.py': '''from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/overview')
def overview():
    df = pd.read_csv('../../datasets/housing_market_data.csv')
    
    return jsonify({
        'total_properties': len(df),
        'avg_price': float(df['price'].mean()) if 'price' in df.columns else 0,
        'price_range': [float(df['price'].min()), float(df['price'].max())] if 'price' in df.columns else [0, 0],
        'locations': df['location'].unique().tolist() if 'location' in df.columns else []
    })

@app.route('/api/price-trends')
def price_trends():
    df = pd.read_csv('../../datasets/housing_market_data.csv')
    
    # Group by date or location (adjust based on actual columns)
    if 'date' in df.columns:
        trends = df.groupby('date')['price'].mean().reset_index()
        return jsonify(trends.to_dict('records'))
    else:
        return jsonify({'message': 'Date column not found'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
''',
        'requirements.txt': '''flask==2.3.3
pandas==2.1.4
numpy==1.24.3
matplotlib==3.7.2
seaborn==0.12.2
plotly==5.17.0
''',
        'templates/index.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Housing Market Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1>🏠 Housing Market Analysis</h1>
        <p>Real estate market trends and property price predictions</p>
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5>Price Trends</h5>
                        <p>Analyzing property market trends...</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5>Location Analysis</h5>
                        <p>Geographic property price analysis...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''
    }
    
    for file_path, content in files_to_create.items():
        # Create directory if needed
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write file
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Created: {file_path}")
    
    return True

def launch_application():
    """Launch the housing market analysis application"""
    print("🏠 Launching Housing Market Analysis...")
    print("="*60)
    print("📊 Dashboard: http://localhost:5000")
    print("📈 Dataset: Real estate market data")
    print("🎯 Focus: Price trends, location analysis")
    print("="*60)
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Application error: {e}")

def main():
    """Main execution function"""
    print("🏠 Housing Market Analysis - Professional Project")
    print("="*60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check requirements
    if not check_requirements():
        print("\n📥 Please ensure housing market dataset is available:")
        print("📁 Expected location: ../../datasets/housing_market_data.csv")
        return
    
    # Ask user what to do
    print("🎯 Available Actions:")
    print("1. Create Project Structure")
    print("2. Launch Application")
    print("3. Create Structure + Launch App")
    print("4. Exit")
    
    choice = input("\n🤔 Choose action (1-4): ").strip()
    
    if choice == '1':
        create_basic_structure()
    elif choice == '2':
        if os.path.exists('app.py'):
            launch_application()
        else:
            print("❌ Application not found. Run option 1 first.")
    elif choice == '3':
        if create_basic_structure():
            launch_application()
    elif choice == '4':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
