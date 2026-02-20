#!/usr/bin/env python3
"""
Simple Electricity Dashboard - No Extra Packages Required
Uses only pandas and basic web server
"""

import pandas as pd
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import threading
import time
from urllib.parse import urlparse, parse_qs

class SimpleElectricityDashboard:
    def __init__(self):
        self.df = None
        self.port = 8050
        self.load_data()
        
    def load_data(self):
        """Load enhanced data"""
        try:
            self.df = pd.read_csv('datasets/Tableau_Ready_Data.csv')
            self.df['dates'] = pd.to_datetime(self.df['dates'])
            print("✅ Data loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def generate_html_dashboard(self):
        """Generate HTML dashboard"""
        # Calculate key statistics
        total_usage = self.df['Usage'].sum()
        avg_usage = self.df['Usage'].mean()
        max_usage = self.df['Usage'].max()
        total_records = len(self.df)
        unique_states = self.df['States'].nunique()
        unique_regions = self.df['Regions'].nunique()
        
        # Generate HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Electricity Consumption Analysis Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            font-size: 0.9rem;
            opacity: 0.9;
        }}
        .chart-container {{
            margin-bottom: 30px;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}
        .chart-title {{
            font-size: 1.3rem;
            color: #2c3e50;
            margin-bottom: 15px;
            text-align: center;
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        .data-table th, .data-table td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        .data-table th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .data-table tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ Electricity Consumption Analysis Dashboard</h1>
            <p>Professional Data Analytics - 2019-2020</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_records:,}</div>
                <div class="stat-label">Total Records</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_usage:,.2f}</div>
                <div class="stat-label">Total Usage (MWh)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{avg_usage:,.2f}</div>
                <div class="stat-label">Average Usage (MWh)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{max_usage:,.2f}</div>
                <div class="stat-label">Peak Usage (MWh)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{unique_states}</div>
                <div class="stat-label">Unique States</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{unique_regions}</div>
                <div class="stat-label">Unique Regions</div>
            </div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">📊 Top 10 States by Consumption</div>
            {self.generate_state_chart()}
        </div>
        
        <div class="chart-container">
            <div class="chart-title">📈 Monthly Consumption Trends</div>
            {self.generate_monthly_chart()}
        </div>
        
        <div class="chart-container">
            <div class="chart-title">🌍 Regional Consumption Distribution</div>
            {self.generate_regional_chart()}
        </div>
        
        <div class="chart-container">
            <div class="chart-title">🔒 COVID-19 Lockdown Impact</div>
            {self.generate_lockdown_chart()}
        </div>
        
        <div class="chart-container">
            <div class="chart-title">🌸 Seasonal Consumption Patterns</div>
            {self.generate_seasonal_chart()}
        </div>
        
        <div class="chart-container">
            <div class="chart-title">📋 Data Summary Table</div>
            {self.generate_data_table()}
        </div>
        
        <div class="footer">
            <p>🎊 Professional Electricity Consumption Analysis Dashboard</p>
            <p>Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Data Source: Tableau_Ready_Data.csv ({total_records:,} records)</p>
        </div>
    </div>
    
    <script>
        // Simple chart interactions
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('Dashboard loaded successfully');
        }});
    </script>
</body>
</html>
        """
        return html_content
    
    def generate_state_chart(self):
        """Generate state consumption chart"""
        top_states = self.df.groupby('States')['Usage'].sum().sort_values(ascending=False).head(10)
        
        chart_html = """
        <div style="background: white; padding: 20px; border-radius: 10px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr><th style="background: #f2f2f2; padding: 10px; text-align: left;">Rank</th><th style="background: #f2f2f2; padding: 10px; text-align: left;">State</th><th style="background: #f2f2f2; padding: 10px; text-align: right;">Usage (MWh)</th></tr>
        """
        
        for i, (state, usage) in enumerate(top_states.items(), 1):
            chart_html += f"""
                <tr>
                    <td style="padding: 10px;">{i}</td>
                    <td style="padding: 10px;">{state}</td>
                    <td style="padding: 10px; text-align: right; font-weight: bold;">{usage:,.2f}</td>
                </tr>
            """
        
        chart_html += "</table></div>"
        return chart_html
    
    def generate_monthly_chart(self):
        """Generate monthly trends chart"""
        monthly_data = self.df.groupby(['year', 'month_name'])['Usage'].sum().reset_index()
        
        chart_html = """
        <div style="background: white; padding: 20px; border-radius: 10px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr><th style="background: #f2f2f2; padding: 10px; text-align: left;">Month</th>
        """
        
        # Add year columns
        years = sorted(self.df['year'].unique())
        for year in years:
            chart_html += f"<th style=\"background: #f2f2f2; padding: 10px; text-align: right;\">{year}</th>"
        
        chart_html += "</tr>"
        
        # Add data rows
        months = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
        
        for month in months:
            chart_html += f"<tr><td style=\"padding: 10px; font-weight: bold;\">{month}</td>"
            for year in years:
                month_data = monthly_data[(monthly_data['month_name'] == month) & (monthly_data['year'] == year)]
                if not month_data.empty:
                    usage = month_data['Usage'].iloc[0] if len(month_data) > 0 else 0
                else:
                    usage = 0
                chart_html += f"<td style=\"padding: 10px; text-align: right;\">{usage:,.2f}</td>"
            chart_html += "</tr>"
        
        chart_html += "</table></div>"
        return chart_html
    
    def generate_regional_chart(self):
        """Generate regional distribution chart"""
        regional_data = self.df.groupby('Regions')['Usage'].sum().sort_values(ascending=False)
        
        chart_html = """
        <div style="background: white; padding: 20px; border-radius: 10px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr><th style="background: #f2f2f2; padding: 10px; text-align: left;">Region</th><th style="background: #f2f2f2; padding: 10px; text-align: right;">Usage (MWh)</th><th style="background: #f2f2f2; padding: 10px; text-align: right;">Percentage</th></tr>
        """
        
        total_usage = regional_data.sum()
        for region, usage in regional_data.items():
            percentage = (usage / total_usage) * 100
            chart_html += f"""
                <tr>
                    <td style="padding: 10px;">{region}</td>
                    <td style="padding: 10px; text-align: right; font-weight: bold;">{usage:,.2f}</td>
                    <td style="padding: 10px; text-align: right;">{percentage:.1f}%</td>
                </tr>
            """
        
        chart_html += "</table></div>"
        return chart_html
    
    def generate_lockdown_chart(self):
        """Generate lockdown impact chart"""
        lockdown_data = self.df.groupby(['year', 'is_lockdown'])['Usage'].mean().reset_index()
        
        chart_html = """
        <div style="background: white; padding: 20px; border-radius: 10px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr><th style="background: #f2f2f2; padding: 10px; text-align: left;">Year</th><th style="background: #f2f2f2; padding: 10px; text-align: left;">Period</th><th style="background: #f2f2f2; padding: 10px; text-align: right;">Average Usage (MWh)</th><th style="background: #f2f2f2; padding: 10px; text-align: right;">Impact</th></tr>
        """
        
        years = sorted(self.df['year'].unique())
        for year in years:
            normal_usage = lockdown_data[(lockdown_data['year'] == year) & (lockdown_data['is_lockdown'] == False)]
            lockdown_usage = lockdown_data[(lockdown_data['year'] == year) & (lockdown_data['is_lockdown'] == True)]
            
            normal_avg = normal_usage['Usage'].iloc[0] if len(normal_usage) > 0 else 0
            lockdown_avg = lockdown_usage['Usage'].iloc[0] if len(lockdown_usage) > 0 else 0
            impact = ((lockdown_avg - normal_avg) / normal_avg * 100) if normal_avg > 0 else 0
            
            chart_html += f"""
                <tr>
                    <td style="padding: 10px;">{year}</td>
                    <td style="padding: 10px;">Normal Period</td>
                    <td style="padding: 10px; text-align: right;">{normal_avg:.2f}</td>
                    <td style="padding: 10px;">{impact:+.1f}%</td>
                </tr>
                <tr>
                    <td style="padding: 10px;"></td>
                    <td style="padding: 10px;">Lockdown Period</td>
                    <td style="padding: 10px; text-align: right;">{lockdown_avg:.2f}</td>
                    <td style="padding: 10px; text-align: right; color: red;">Impact</td>
                </tr>
                """
        
        chart_html += "</table></div>"
        return chart_html
    
    def generate_seasonal_chart(self):
        """Generate seasonal patterns chart"""
        seasonal_data = self.df.groupby('season')['Usage'].sum().sort_values(ascending=False)
        
        chart_html = """
        <div style="background: white; padding: 20px; border-radius: 10px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr><th style="background: #f2f2f2; padding: 10px; text-align: left;">Season</th><th style="background: #f2f2f2; padding: 10px; text-align: right;">Total Usage (MWh)</th><th style="background: #f2f2f2; padding: 10px; text-align: right;">Percentage</th></tr>
        """
        
        total_usage = seasonal_data.sum()
        for season, usage in seasonal_data.items():
            percentage = (usage / total_usage) * 100
            chart_html += f"""
                <tr>
                    <td style="padding: 10px;">{season}</td>
                    <td style="padding: 10px; text-align: right; font-weight: bold;">{usage:,.2f}</td>
                    <td style="padding: 10px; text-align: right;">{percentage:.1f}%</td>
                </tr>
            """
        
        chart_html += "</table></div>"
        return chart_html
    
    def generate_data_table(self):
        """Generate summary data table"""
        summary_data = self.df.groupby(['States', 'Regions', 'year']).agg({
            'Usage': ['sum', 'mean', 'min', 'max', 'count']
        }).round(2).reset_index()
        
        chart_html = """
        <div style="background: white; padding: 20px; border-radius: 10px; max-height: 400px; overflow-y: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
                <tr>
                    <th style="background: #f2f2f2; padding: 8px; text-align: left; position: sticky; top: 0;">State</th>
                    <th style="background: #f2f2f2; padding: 8px; text-align: left; position: sticky; top: 0;">Region</th>
                    <th style="background: #f2f2f2; padding: 8px; text-align: left; position: sticky; top: 0;">Year</th>
                    <th style="background: #f2f2f2; padding: 8px; text-align: right; position: sticky; top: 0;">Total</th>
                    <th style="background: #f2f2f2; padding: 8px; text-align: right; position: sticky; top: 0;">Average</th>
                    <th style="background: #f2f2f2; padding: 8px; text-align: right; position: sticky; top: 0;">Min</th>
                    <th style="background: #f2f2f2; padding: 8px; text-align: right; position: sticky; top: 0;">Max</th>
                    <th style="background: #f2f2f2; padding: 8px; text-align: right; position: sticky; top: 0;">Count</th>
                </tr>
        """
        
        for _, row in summary_data.head(20).iterrows():
            chart_html += f"""
                <tr>
                    <td style="padding: 8px;">{row['States']}</td>
                    <td style="padding: 8px;">{row['Regions']}</td>
                    <td style="padding: 8px; text-align: center;">{row['year']}</td>
                    <td style="padding: 8px; text-align: right;">{row['Usage']['sum']:,.2f}</td>
                    <td style="padding: 8px; text-align: right;">{row['Usage']['mean']:,.2f}</td>
                    <td style="padding: 8px; text-align: right;">{row['Usage']['min']:,.2f}</td>
                    <td style="padding: 8px; text-align: right;">{row['Usage']['max']:,.2f}</td>
                    <td style="padding: 8px; text-align: right;">{row['Usage']['count']}</td>
                </tr>
            """
        
        chart_html += "</table></div>"
        return chart_html
    
    def open_browser(self):
        """Open browser automatically"""
        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open(f'http://localhost:{self.port}')
                print(f"🌐 Opening dashboard at http://localhost:{self.port}")
            except:
                print(f"🌐 Please manually open: http://localhost:{self.port}")
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
    
    def run_server(self):
        """Run the HTTP server"""
        try:
            # Generate HTML dashboard
            html_content = self.generate_html_dashboard()
            
            # Write HTML to file
            with open('dashboard.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Start HTTP server
            handler = SimpleHTTPRequestHandler
            httpd = HTTPServer(('localhost', self.port), handler)
            
            print("🚀 Simple Electricity Dashboard Starting...")
            print(f"🌐 Access at: http://localhost:{self.port}")
            print("📊 Professional visualizations ready")
            print("📱 Mobile responsive design")
            print("🔧 No extra packages required")
            print("="*50)
            
            # Open browser
            self.open_browser()
            
            # Start server
            httpd.serve_forever()
            
        except KeyboardInterrupt:
            print("\n👋 Dashboard stopped by user")
        except Exception as e:
            print(f"❌ Server error: {e}")

def main():
    """Main function"""
    print("🎊 Simple Electricity Dashboard - No Extra Packages")
    print("="*60)
    print("📈 Alternative to Tableau Desktop")
    print("🚀 Professional visualizations")
    print("📱 Mobile responsive design")
    print("🔧 Uses only pandas and basic Python")
    print("="*60)
    
    dashboard = SimpleElectricityDashboard()
    dashboard.run_server()

if __name__ == "__main__":
    main()
