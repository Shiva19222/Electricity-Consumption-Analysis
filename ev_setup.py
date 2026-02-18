#!/usr/bin/env python3
"""
Quick Setup Script for Electric Vehicle Analysis Project
Automates database setup and data import for all 4 EV datasets
"""

import os
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_ev_files():
    """Check if all EV dataset files exist"""
    ev_files = [
        'ElectricCarData_Clean.csv',
        'electric_vehicle_charging_station_list.csv',
        'Cheapestelectriccars-EVDatabase.csv',
        'EVIndia.csv'
    ]
    
    missing_files = []
    existing_files = []
    
    for file in ev_files:
        if os.path.exists(file):
            existing_files.append(file)
            logging.info(f"✅ {file} found")
        else:
            missing_files.append(file)
            logging.error(f"❌ {file} not found")
    
    return existing_files, missing_files

def check_project_files():
    """Check if project files exist"""
    project_files = [
        'ev_database_schema.sql',
        'ev_data_import.py',
        'ev_app.py',
        'ev_sql_queries.sql'
    ]
    
    missing_project_files = []
    for file in project_files:
        if not os.path.exists(file):
            missing_project_files.append(file)
            logging.error(f"❌ Project file missing: {file}")
    
    return missing_project_files

def run_command(command, description):
    """Run a command and return success status"""
    logging.info(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"✅ {description} completed successfully")
            return True
        else:
            logging.error(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        logging.error(f"❌ {description} error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚗 ELECTRIC VEHICLE ANALYSIS PROJECT SETUP")
    print("="*60)
    
    # Check EV dataset files
    logging.info("📋 Checking EV dataset files...")
    existing_files, missing_files = check_ev_files()
    
    if missing_files:
        print("\n❌ MISSING EV DATASET FILES:")
        for file in missing_files:
            print(f"   📄 {file}")
        print("\n📥 Download Instructions:")
        print("   🔗 Link: https://drive.google.com/drive/folders/1Rkzdks6Us1Uq2SRB4nxMAb83jN5bpHll")
        print("   📁 Download all 4 CSV files to this directory")
        print("\n⏳ Please download missing files and run this script again.")
        return False
    
    # Check project files
    logging.info("📋 Checking project files...")
    missing_project_files = check_project_files()
    
    if missing_project_files:
        print("\n❌ MISSING PROJECT FILES:")
        for file in missing_project_files:
            print(f"   📄 {file}")
        print("\n⚠️  Some project files are missing. Please ensure all files are present.")
    
    # Check Python dependencies
    logging.info("🐍 Checking Python dependencies...")
    try:
        import mysql.connector
        import pandas
        import flask
        logging.info("✅ All Python dependencies are installed")
    except ImportError as e:
        logging.error(f"❌ Missing dependency: {e}")
        logging.error("Please run: pip install mysql-connector-python pandas flask flask-cors")
        return False
    
    # Database setup instructions
    print("\n🗄️ DATABASE SETUP:")
    print("="*40)
    print("1. Make sure MySQL is installed and running")
    print("2. Create database using:")
    print("   mysql -u root -p < ev_database_schema.sql")
    print("3. Update password in ev_data_import.py if needed")
    print("4. Import data using:")
    print("   python ev_data_import.py")
    
    # Ask user if they want to proceed with data import
    proceed = input("\n🤔 Do you want to proceed with data import now? (y/n): ").lower().strip()
    
    if proceed == 'y':
        # Run data import
        if run_command("python ev_data_import.py", "EV Data Import"):
            logging.info("✅ EV data import completed successfully")
        else:
            logging.error("❌ EV data import failed")
            return False
    
    # Web application setup
    print("\n🌐 WEB APPLICATION SETUP:")
    print("="*40)
    print("1. Run the EV Flask application:")
    print("   python ev_app.py")
    print("2. Open browser to: http://localhost:5000")
    print("3. Access dashboard: http://localhost:5000/dashboard")
    print("4. Access data story: http://localhost:5000/story")
    
    # Ask user if they want to start the web app
    start_app = input("\n🚀 Do you want to start the EV web application now? (y/n): ").lower().strip()
    
    if start_app == 'y':
        logging.info("🌐 Starting EV Flask application...")
        try:
            subprocess.run([sys.executable, "ev_app.py"])
        except KeyboardInterrupt:
            logging.info("👋 Application stopped by user")
        except Exception as e:
            logging.error(f"❌ Error starting application: {e}")
    
    print("\n✅ EV PROJECT SETUP COMPLETE!")
    print("="*60)
    print("🚗 Project Features:")
    print("• 4 EV datasets integrated")
    print("• Comprehensive database schema")
    print("• Interactive web dashboard")
    print("• Data story presentation")
    print("• REST API endpoints")
    print("• Tableau-ready queries")
    print("• India-specific analysis")
    print("• Charging infrastructure analysis")
    
    print("\n📁 Dataset Files:")
    print("• ElectricCarData_Clean.csv - Main EV specifications")
    print("• electric_vehicle_charging_station_list.csv - Charging stations")
    print("• Cheapestelectriccars-EVDatabase.csv - Market database")
    print("• EVIndia.csv - India-specific data")
    
    print("\n🔗 Access URLs:")
    print("• Main Site: http://localhost:5000/")
    print("• Dashboard: http://localhost:5000/dashboard")
    print("• Data Story: http://localhost:5000/story")
    print("• API Health: http://localhost:5000/api/ev/health")
    
    print("\n📊 Analysis Capabilities:")
    print("• Price vs Range analysis")
    print("• Brand comparison and market share")
    print("• Technology evolution trends")
    print("• Charging infrastructure mapping")
    print("• India market analysis")
    print("• Performance metrics")
    print("• Value for money analysis")
    
    return True

if __name__ == "__main__":
    main()
