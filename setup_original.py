#!/usr/bin/env python3
"""
Quick Setup Script for Original Dataset
Automates database setup and data import
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

def check_file_exists(filename):
    """Check if file exists"""
    if os.path.exists(filename):
        logging.info(f"✅ {filename} found")
        return True
    else:
        logging.error(f"❌ {filename} not found")
        return False

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
    print("🚀 ELECTRICITY CONSUMPTION ANALYSIS - ORIGINAL DATASET SETUP")
    print("="*60)
    
    # Check required files
    logging.info("📋 Checking required files...")
    required_files = [
        'Consumption.csv',
        'database_schema_original.sql',
        'data_import_original.py',
        'app_original.py'
    ]
    
    all_files_exist = True
    for file in required_files:
        if not check_file_exists(file):
            all_files_exist = False
    
    if not all_files_exist:
        logging.error("❌ Some required files are missing. Please ensure all files are present.")
        return False
    
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
    print("\n📊 DATABASE SETUP REQUIRED:")
    print("="*40)
    print("1. Make sure MySQL is installed and running")
    print("2. Create database using:")
    print("   mysql -u root -p < database_schema_original.sql")
    print("3. Update password in data_import_original.py if needed")
    print("4. Import data using:")
    print("   python data_import_original.py")
    
    # Ask user if they want to proceed with data import
    proceed = input("\n🤔 Do you want to proceed with data import now? (y/n): ").lower().strip()
    
    if proceed == 'y':
        # Run data import
        if run_command("python data_import_original.py", "Data Import"):
            logging.info("✅ Data import completed successfully")
        else:
            logging.error("❌ Data import failed")
            return False
    
    # Web application setup
    print("\n🌐 WEB APPLICATION SETUP:")
    print("="*40)
    print("1. Run the Flask application:")
    print("   python app_original.py")
    print("2. Open browser to: http://localhost:5000")
    print("3. Access dashboard: http://localhost:5000/dashboard")
    print("4. Access data story: http://localhost:5000/story")
    
    # Ask user if they want to start the web app
    start_app = input("\n🚀 Do you want to start the web application now? (y/n): ").lower().strip()
    
    if start_app == 'y':
        logging.info("🌐 Starting Flask application...")
        try:
            subprocess.run([sys.executable, "app_original.py"])
        except KeyboardInterrupt:
            logging.info("👋 Application stopped by user")
        except Exception as e:
            logging.error(f"❌ Error starting application: {e}")
    
    print("\n✅ SETUP COMPLETE!")
    print("="*40)
    print("📊 Project Features:")
    print("• 16,599 electricity consumption records")
    print("• 36 Indian States/UTs across 5 regions")
    print("• Date range: Jan 2019 to Sep 2020")
    print("• COVID-19 lockdown impact analysis")
    print("• Interactive web dashboard")
    print("• Data story presentation")
    print("• REST API endpoints")
    print("• Tableau-ready views")
    
    print("\n📁 Important Files:")
    print("• Consumption.csv - Original dataset")
    print("• database_schema_original.sql - Database structure")
    print("• data_import_original.py - Data import script")
    print("• app_original.py - Flask web application")
    print("• sql_queries_original.sql - Analysis queries")
    
    print("\n🔗 Access URLs:")
    print("• Main Site: http://localhost:5000/")
    print("• Dashboard: http://localhost:5000/dashboard")
    print("• Data Story: http://localhost:5000/story")
    print("• API Health: http://localhost:5000/api/health")
    
    return True

if __name__ == "__main__":
    main()
