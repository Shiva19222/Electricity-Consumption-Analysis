#!/usr/bin/env python3
"""
Professional Cosmetics Insights Analysis Project
Retail Analytics - Beauty Industry Analysis
"""

import os
import sys
import subprocess
from datetime import datetime

def check_requirements():
    """Check if required files exist"""
    print("🔍 Checking cosmetics project requirements...")
    
    # Check dataset
    dataset_path = '../../datasets/cosmetics.csv'
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found: {dataset_path}")
        return False
    
    print("✅ Cosmetics dataset found")
    return True

def create_basic_structure():
    """Create basic project structure"""
    print("🏗️ Creating cosmetics project structure...")
    
    # Create basic files
    files_to_create = {
        'README.md': '''# 🧴 Cosmetics Insights Analysis

## 🎯 Project Overview
Beauty industry analytics with consumer preferences and market trend analysis.

## 📊 Dataset
- **Source:** cosmetics.csv (1.1 MB)
- **Focus:** Consumer preferences, market trends
- **Domain:** Retail Analytics

## 🚀 Quick Start
```bash
python run.py
```

## 📋 Features
- Brand Performance Analysis
- Customer Segmentation
- Market Trend Identification
- Product Category Analysis
''',
        'app.py': '''from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/overview')
def overview():
    # Load cosmetics data
    df = pd.read_csv('../../datasets/cosmetics.csv')
    
    return jsonify({
        'total_products': len(df),
        'unique_brands': df['brand'].nunique() if 'brand' in df.columns else 0,
        'categories': df['category'].unique().tolist() if 'category' in df.columns else []
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
''',
        'requirements.txt': '''flask==2.3.3
pandas==2.1.4
matplotlib==3.7.2
seaborn==0.12.2
''',
        'templates/index.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Cosmetics Insights</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1>🧴 Cosmetics Insights Analysis</h1>
        <p>Beauty industry analytics and market trends</p>
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5>Dataset Overview</h5>
                        <p>Analyzing cosmetics industry data...</p>
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
    """Launch the cosmetics analysis application"""
    print("🧴 Launching Cosmetics Insights Analysis...")
    print("="*60)
    print("📊 Dashboard: http://localhost:5000")
    print("📈 Dataset: Beauty industry consumer data")
    print("🎯 Focus: Brand performance, market trends")
    print("="*60)
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Application error: {e}")

def main():
    """Main execution function"""
    print("🧴 Cosmetics Insights Analysis - Professional Project")
    print("="*60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check requirements
    if not check_requirements():
        print("\n📥 Please ensure cosmetics dataset is available:")
        print("📁 Expected location: ../../datasets/cosmetics.csv")
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
