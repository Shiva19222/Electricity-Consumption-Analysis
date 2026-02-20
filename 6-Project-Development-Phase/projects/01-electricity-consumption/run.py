#!/usr/bin/env python3
"""
Professional Electricity Consumption Analysis Project
Energy Analytics - Complete Production Application
"""

import os
import sys
import subprocess
from datetime import datetime

def check_requirements():
    """Check if required files exist"""
    required_files = [
        'app_original.py',
        'database_schema_original.sql',
        'data_import_original.py'
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

def setup_database():
    """Setup MySQL database"""
    print("🗄️ Setting up database...")
    try:
        result = subprocess.run(['mysql', '-u', 'root', '-p', '<', 'database_schema_original.sql'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Database setup completed")
            return True
        else:
            print(f"❌ Database setup failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return False

def import_data():
    """Import consumption data"""
    print("📊 Importing data...")
    try:
        result = subprocess.run([sys.executable, 'data_import_original.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Data import completed")
            return True
        else:
            print(f"❌ Data import failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Data import error: {e}")
        return False

def launch_application():
    """Launch the web application"""
    print("🚀 Launching Electricity Consumption Analysis...")
    print("="*60)
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("📖 Data Story: http://localhost:5000/story")
    print("🔌 API Health: http://localhost:5000/api/health")
    print("📈 Dataset: 16,599 electricity consumption records")
    print("🎯 Focus: COVID-19 impact, regional patterns, trends")
    print("="*60)
    
    try:
        subprocess.run([sys.executable, 'app_original.py'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Application error: {e}")

def main():
    """Main execution function"""
    print("⚡ Electricity Consumption Analysis - Professional Project")
    print("="*60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check requirements
    if not check_requirements():
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
