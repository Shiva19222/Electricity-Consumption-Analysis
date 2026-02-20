#!/usr/bin/env python3
"""
Professional Electric Vehicle Analysis Project
Automotive Analytics - Multi-Dataset Integration
"""

import os
import sys
import subprocess
from datetime import datetime

def check_requirements():
    """Check if required files exist"""
    required_files = [
        'ev_app.py',
        'ev_database_schema.sql',
        'ev_data_import.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   📄 {file}")
        return False
    
    print("✅ All required files found")
    return True

def check_datasets():
    """Check if EV datasets exist"""
    datasets_path = '../../datasets'
    required_datasets = [
        'ElectricCarData_Clean.csv',
        'electric_vehicle_charging_station_list.csv',
        'Cheapestelectriccars-EVDatabase.csv',
        'EVIndia.csv'
    ]
    
    missing_datasets = []
    for dataset in required_datasets:
        if not os.path.exists(os.path.join(datasets_path, dataset)):
            missing_datasets.append(dataset)
    
    if missing_datasets:
        print("❌ Missing EV datasets:")
        for dataset in missing_datasets:
            print(f"   📊 {dataset}")
        print(f"📁 Expected location: {datasets_path}")
        return False
    
    print("✅ All EV datasets found")
    return True

def setup_database():
    """Setup MySQL database"""
    print("🗄️ Setting up EV database...")
    try:
        result = subprocess.run(['mysql', '-u', 'root', '-p', '<', 'ev_database_schema.sql'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ EV Database setup completed")
            return True
        else:
            print(f"❌ Database setup failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return False

def import_data():
    """Import EV data"""
    print("📊 Importing EV datasets...")
    try:
        result = subprocess.run([sys.executable, 'ev_data_import.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ EV Data import completed")
            return True
        else:
            print(f"❌ Data import failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Data import error: {e}")
        return False

def launch_application():
    """Launch the EV web application"""
    print("🚗 Launching Electric Vehicle Analysis...")
    print("="*60)
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("📖 Data Story: http://localhost:5000/story")
    print("🔌 API Health: http://localhost:5000/api/ev/health")
    print("📈 Datasets: 4 integrated EV datasets")
    print("🎯 Focus: Market analysis, technology trends, charging infrastructure")
    print("="*60)
    
    try:
        subprocess.run([sys.executable, 'ev_app.py'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Application error: {e}")

def main():
    """Main execution function"""
    print("🚗 Electric Vehicle Analysis - Professional Project")
    print("="*60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check requirements
    if not check_requirements():
        return
    
    # Check datasets
    if not check_datasets():
        print("\n📥 Please download EV datasets first:")
        print("🔗 Link: https://drive.google.com/drive/folders/1Rkzdks6Us1Uq2SRB4nxMAb83jN5bpHll")
        print("📁 Save to: ../../datasets/")
        return
    
    # Ask user what to do
    print("🎯 Available Actions:")
    print("1. Setup Database & Import Data")
    print("2. Launch Web Application")
    print("3. Full Setup (Database + Data + App)")
    print("4. Exit")
    
    choice = input("\n🤔 Choose action (1-4): ").strip()
    
    if choice == '1':
        setup_database()
        import_data()
    elif choice == '2':
        launch_application()
    elif choice == '3':
        if setup_database() and import_data():
            launch_application()
    elif choice == '4':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
