#!/usr/bin/env python3
"""
Tableau Electricity Analysis - Complete Setup Script
Automated setup for the entire project
"""

import os
import sys
import subprocess
import json
from datetime import datetime

class TableauProjectSetup:
    def __init__(self):
        self.project_dir = os.getcwd()
        self.setup_log = []
        
    def log(self, message):
        """Log setup progress"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.setup_log.append(log_entry)
        print(log_entry)
        
    def check_requirements(self):
        """Check if required software is available"""
        self.log("🔍 Checking system requirements...")
        
        requirements = {
            'Python': sys.version_info >= (3, 7),
            'MySQL': False,
            'SQL Server': False,
            'Tableau': False
        }
        
        # Check Python
        if requirements['Python']:
            self.log("✅ Python 3.7+ detected")
        else:
            self.log("❌ Python 3.7+ required")
            
        # Check MySQL
        try:
            import mysql.connector
            requirements['MySQL'] = True
            self.log("✅ MySQL connector available")
        except ImportError:
            self.log("⚠️ MySQL connector not available. Install with: pip install mysql-connector-python")
            
        # Check SQL Server
        try:
            import pyodbc
            requirements['SQL Server'] = True
            self.log("✅ SQL Server connector available")
        except ImportError:
            self.log("⚠️ SQL Server connector not available. Install with: pip install pyodbc")
            
        # Check for Tableau (basic check)
        tableau_paths = [
            'C:\\Program Files\\Tableau\\Tableau 2024.1\\bin\\tableau.exe',
            'C:\\Program Files\\Tableau\\Tableau 2023.3\\bin\\tableau.exe',
            'C:\\Program Files (x86)\\Tableau\\Tableau 2024.1\\bin\\tableau.exe'
        ]
        
        for path in tableau_paths:
            if os.path.exists(path):
                requirements['Tableau'] = True
                self.log("✅ Tableau Desktop detected")
                break
        else:
            self.log("⚠️ Tableau Desktop not detected. Install Tableau Desktop for visualization creation")
            
        return requirements
    
    def create_directories(self):
        """Create necessary directories"""
        self.log("📁 Creating project directories...")
        
        directories = [
            'tableau_files',
            'tableau_files/dashboards',
            'tableau_files/stories',
            'tableau_files/visualizations',
            'tableau_files/data_sources',
            'tableau_files/exports',
            'documentation',
            'documentation/images',
            'documentation/videos'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            self.log(f"✅ Created directory: {directory}")
            
    def setup_database(self):
        """Setup database schema"""
        self.log("🗄️ Setting up database schema...")
        
        # Check if schema file exists
        schema_file = 'tableau_electricity_schema.sql'
        if not os.path.exists(schema_file):
            self.log(f"❌ Schema file not found: {schema_file}")
            return False
            
        self.log(f"✅ Schema file found: {schema_file}")
        self.log("📋 Database schema ready for execution")
        self.log("🔧 To setup database:")
        self.log("   For MySQL: mysql -u root -p < tableau_electricity_schema.sql")
        self.log("   For SQL Server: Execute in SQL Server Management Studio")
        
        return True
    
    def check_dataset(self):
        """Check if dataset is available"""
        self.log("📊 Checking dataset availability...")
        
        dataset_file = 'datasets/Consumption.csv'
        if os.path.exists(dataset_file):
            self.log(f"✅ Dataset found: {dataset_file}")
            
            # Get dataset info
            import pandas as pd
            try:
                df = pd.read_csv(dataset_file)
                self.log(f"📈 Dataset info: {len(df)} records, {len(df.columns)} columns")
                self.log(f"🗓️ Date range: {df['Dates'].min()} to {df['Dates'].max()}")
                self.log(f"🏛️ States: {df['States'].nunique()}")
                self.log(f"🌍 Regions: {df['Regions'].nunique()}")
                return True
            except Exception as e:
                self.log(f"❌ Error reading dataset: {e}")
                return False
        else:
            self.log(f"❌ Dataset not found: {dataset_file}")
            return False
    
    def setup_flask_app(self):
        """Setup Flask application"""
        self.log("🌐 Setting up Flask application...")
        
        flask_file = 'tableau_flask_app.py'
        if os.path.exists(flask_file):
            self.log(f"✅ Flask application found: {flask_file}")
            self.log("🚀 To run Flask app:")
            self.log("   python tableau_flask_app.py")
            self.log("   Access at: http://localhost:5000")
            return True
        else:
            self.log(f"❌ Flask application not found: {flask_file}")
            return False
    
    def create_tableau_instructions(self):
        """Create Tableau development instructions"""
        self.log("📋 Creating Tableau development instructions...")
        
        instructions = """
# Tableau Development Instructions

## 1. Connect to Data Source
### MySQL Connection:
- Server: localhost
- Port: 3306
- Database: electricity_tableau_analysis
- Username: root
- Password: [your_password]

### SQL Server Connection:
- Server: localhost\\SQLEXPRESS
- Database: electricity_tableau_analysis
- Authentication: Windows Authentication

## 2. Create Visualizations
### Activity 1.1 (5 Visualizations):
1. 2019 State Consumption - Bar Chart
2. 2020 State Consumption - Bar Chart
3. Total Consumption - Summary Card
4. Usage by Region - Pie Chart
5. Top N and Bottom N States - Ranking Bar Chart

### Activity 1.2 (3 Visualizations):
6. 2019 and 2020 Month-wise Consumption - Line Chart
7. Total Consumption by Region - Heat Map
8. Usage Before and After Lockdown - Comparison Chart

### Activity 1.3 (4 Visualizations):
9. Region-wise State Usage - Filled Map
10. Quarter Usage - Bar Chart
11. Metro City State Usage - Scatter Plot
12. Usage by Year - Side-by-Side Bar Chart

## 3. Build Dashboard
- Drag all visualizations to dashboard
- Arrange in logical layout
- Add filters for Year, Region, State
- Add title and descriptions
- Make it responsive

## 4. Create Story
- Create 5 scenes as specified
- Add narrative text
- Include key insights
- Add navigation buttons
- Publish to Tableau Public

## 5. Publish to Tableau Public
- Click Share -> Publish to Tableau Public
- Sign in with Tableau Public account
- Choose what to publish
- Get public URL
- Update Flask app with URL
"""
        
        with open('tableau_files/development_instructions.txt', 'w') as f:
            f.write(instructions)
        self.log("✅ Tableau development instructions created")
    
    def create_checklist(self):
        """Create project checklist"""
        self.log("📋 Creating project checklist...")
        
        checklist = """
# Tableau Electricity Analysis - Project Checklist

## Database Setup
- [ ] Database schema executed
- [ ] Data imported successfully
- [ ] Views and stored procedures created
- [ ] Performance optimization applied

## Tableau Development
- [ ] Data source connected
- [ ] 12 visualizations created
- [ ] Interactive dashboard built
- [ ] 5-scene story created
- [ ] Published to Tableau Public

## Web Integration
- [ ] Flask application running
- [ ] HTML templates created
- [ ] Tableau URLs updated
- [ ] Responsive design tested

## Documentation
- [ ] Project documentation completed
- [ ] User guide created
- [ ] Technical documentation prepared
- [ ] Demonstration video recorded

## Testing
- [ ] Dashboard loading time < 3 seconds
- [ ] Mobile responsiveness verified
- [ ] All filters working correctly
- [ ] Navigation functioning properly

## Deployment
- [ ] Local testing completed
- [ ] Production deployment ready
- [ ] SSL certificate configured
- [ ] Custom domain set up
"""
        
        with open('tableau_files/project_checklist.txt', 'w') as f:
            f.write(checklist)
        self.log("✅ Project checklist created")
    
    def generate_report(self):
        """Generate setup report"""
        self.log("📊 Generating setup report...")
        
        report = {
            'setup_time': datetime.now().isoformat(),
            'project_directory': self.project_dir,
            'setup_log': self.setup_log,
            'next_steps': [
                'Execute database schema',
                'Import data using tableau_data_import.py',
                'Create Tableau visualizations',
                'Build dashboard and story',
                'Publish to Tableau Public',
                'Update Flask app with Tableau URLs',
                'Test web application'
            ]
        }
        
        with open('tableau_files/setup_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        self.log("✅ Setup report generated")
    
    def run_setup(self):
        """Run complete setup process"""
        print("🎊 Tableau Electricity Analysis - Complete Setup")
        print("="*60)
        
        # Check requirements
        requirements = self.check_requirements()
        
        # Create directories
        self.create_directories()
        
        # Check dataset
        dataset_ok = self.check_dataset()
        
        # Setup database
        db_ok = self.setup_database()
        
        # Setup Flask app
        flask_ok = self.setup_flask_app()
        
        # Create instructions
        self.create_tableau_instructions()
        self.create_checklist()
        
        # Generate report
        self.generate_report()
        
        # Summary
        print("\n" + "="*60)
        print("🎯 SETUP SUMMARY:")
        print("="*60)
        
        if dataset_ok and db_ok and flask_ok:
            print("✅ All components ready for development!")
        else:
            print("⚠️ Some components need attention")
            
        print("\n📋 NEXT STEPS:")
        print("1. Execute database schema")
        print("2. Import data: python tableau_data_import.py")
        print("3. Open Tableau and connect to database")
        print("4. Create 12 visualizations as specified")
        print("5. Build dashboard and story")
        print("6. Publish to Tableau Public")
        print("7. Update Flask app with Tableau URLs")
        print("8. Run web application: python tableau_flask_app.py")
        
        print("\n📁 Files Created:")
        print("- tableau_electricity_schema.sql (Database schema)")
        print("- tableau_data_import.py (Data import script)")
        print("- tableau_flask_app.py (Flask web application)")
        print("- tableau_project_guide.md (Complete guide)")
        print("- templates/tableau_index.html (Main page)")
        print("- tableau_files/ (Tableau development files)")
        
        print("\n🎊 Setup completed successfully!")

def main():
    """Main function"""
    setup = TableauProjectSetup()
    setup.run_setup()

if __name__ == "__main__":
    main()
