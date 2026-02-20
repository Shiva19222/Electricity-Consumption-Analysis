#!/usr/bin/env python3
"""
Professional Heart Disease Analysis Project
Healthcare Analytics - Medical Data Analysis
"""

import os
import sys
import subprocess
from datetime import datetime

def check_requirements():
    """Check if required files exist"""
    print("🔍 Checking heart disease project requirements...")
    
    # Check dataset
    dataset_path = '../../datasets/heart_disease_data.csv'
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found: {dataset_path}")
        return False
    
    print("✅ Heart disease dataset found")
    return True

def create_basic_structure():
    """Create basic project structure"""
    print("🏗️ Creating heart disease project structure...")
    
    # Create basic files
    files_to_create = {
        'README.md': '''# 🏥 Heart Disease Analysis

## 🎯 Project Overview
Medical data analysis for disease prediction and health risk assessment.

## 📊 Dataset
- **Source:** heart_disease_data.csv (32 KB)
- **Focus:** Medical indicators, risk factors
- **Domain:** Healthcare Analytics

## 🚀 Quick Start
```bash
python run.py
```

## 📋 Features
- Risk Assessment Analysis
- Medical Dashboard
- Predictive Modeling
- Health Insights
''',
        'app.py': '''from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

app = Flask(__name__)

# Load and prepare data
def load_and_prepare_data():
    df = pd.read_csv('../../datasets/heart_disease_data.csv')
    
    # Basic preprocessing
    # Handle missing values
    df = df.fillna(df.mean())
    
    # Feature preparation (adjust based on actual columns)
    X = df.drop('target', axis=1) if 'target' in df.columns else df.iloc[:, :-1]
    y = df['target'] if 'target' in df.columns else df.iloc[:, -1]
    
    return X, y, df.columns.tolist()

# Train model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model
    with open('heart_disease_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return model, accuracy

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/overview')
def overview():
    X, y, columns = load_and_prepare_data()
    
    return jsonify({
        'total_patients': len(X),
        'features': len(columns) - 1,
        'positive_cases': int(y.sum()),
        'negative_cases': int(len(y) - y.sum()),
        'columns': columns
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Load model
        if os.path.exists('heart_disease_model.pkl'):
            with open('heart_disease_model.pkl', 'rb') as f:
                model = pickle.load(f)
        else:
            return jsonify({'error': 'Model not trained'}), 500
        
        # Get data from request
        data = request.get_json()
        
        # Make prediction
        prediction = model.predict([data['features']])
        
        return jsonify({
            'prediction': int(prediction[0]),
            'risk_level': 'High' if prediction[0] == 1 else 'Low'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Train model on startup
    X, y, columns = load_and_prepare_data()
    model, accuracy = train_model(X, y)
    
    print(f"Model trained with accuracy: {accuracy:.2f}")
    app.run(debug=True, port=5000)
''',
        'requirements.txt': '''flask==2.3.3
pandas==2.1.4
numpy==1.24.3
scikit-learn==1.3.2
matplotlib==3.7.2
seaborn==0.12.2
''',
        'templates/index.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Heart Disease Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1>🏥 Heart Disease Analysis</h1>
        <p>Medical data analysis for disease prediction and health risk assessment</p>
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5>Patient Overview</h5>
                        <p>Analyzing medical indicators and risk factors...</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5>Risk Assessment</h5>
                        <p>Predictive modeling for heart disease risk...</p>
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
    """Launch the heart disease analysis application"""
    print("🏥 Launching Heart Disease Analysis...")
    print("="*60)
    print("📊 Dashboard: http://localhost:5000")
    print("📈 Dataset: Medical indicators and risk factors")
    print("🎯 Focus: Disease prediction, health insights")
    print("="*60)
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Application error: {e}")

def main():
    """Main execution function"""
    print("🏥 Heart Disease Analysis - Professional Project")
    print("="*60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check requirements
    if not check_requirements():
        print("\n📥 Please ensure heart disease dataset is available:")
        print("📁 Expected location: ../../datasets/heart_disease_data.csv")
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
