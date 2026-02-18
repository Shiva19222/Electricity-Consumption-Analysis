#!/usr/bin/env python3
"""
Tableau Electricity Consumption Flask Application
Web integration for Tableau visualizations
"""

from flask import Flask, render_template, jsonify, request
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'tableau_electricity_analysis_2024'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Tableau Public URLs (replace with your actual Tableau Public URLs)
TABLEAU_VIEWS = {
    'dashboard': 'PASTE_YOUR_DASHBOARD_URL_HERE',
    'story': 'PASTE_YOUR_STORY_URL_HERE',
    'yearly_comparison': 'PASTE_YOUR_DASHBOARD_URL_HERE',
    'regional_analysis': 'PASTE_YOUR_DASHBOARD_URL_HERE',
    'lockdown_impact': 'PASTE_YOUR_DASHBOARD_URL_HERE',
    'seasonal_patterns': 'PASTE_YOUR_DASHBOARD_URL_HERE',
    'state_rankings': 'PASTE_YOUR_DASHBOARD_URL_HERE',
    'consumption_trends': 'PASTE_YOUR_DASHBOARD_URL_HERE',
    'metro_analysis': 'PASTE_YOUR_DASHBOARD_URL_HERE',
    'quarterly_analysis': 'PASTE_YOUR_DASHBOARD_URL_HERE',
    'regional_distribution': 'PASTE_YOUR_DASHBOARD_URL_HERE',
    'usage_categories': 'PASTE_YOUR_DASHBOARD_URL_HERE'
}
@app.route('/')
def index():
    """Main portfolio page"""
    return render_template('tableau_index.html', 
                        tableau_views=TABLEAU_VIEWS,
                        current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/dashboard')
def dashboard():
    """Tableau dashboard page"""
    return render_template('tableau_dashboard.html',
                        tableau_url=TABLEAU_VIEWS['dashboard'],
                        title='Electricity Consumption Dashboard')

@app.route('/story')
def story():
    """Tableau story page"""
    return render_template('tableau_story.html',
                        tableau_url=TABLEAU_VIEWS['story'],
                        title='Electricity Consumption Story')

@app.route('/visualizations')
def visualizations():
    """Individual visualizations page"""
    return render_template('tableau_visualizations.html',
                        tableau_views=TABLEAU_VIEWS,
                        title='Electricity Consumption Visualizations')

@app.route('/analysis')
def analysis():
    """Analysis insights page"""
    return render_template('tableau_analysis.html',
                        title='Analysis Insights')

@app.route('/api/project-info')
def project_info():
    """API endpoint for project information"""
    project_info = {
        'project_name': 'Plugging into the Future: Electricity Consumption Analysis',
        'project_description': 'Comprehensive analysis of electricity consumption patterns using Tableau',
        'dataset': 'Consumption.csv (16,599 records)',
        'time_period': '2019-01-02 to 2020-12-05',
        'total_states': 36,
        'total_regions': 6,
        'visualizations_count': 12,
        'dashboard_count': 1,
        'story_scenes': 5,
        'technologies': ['Tableau', 'MySQL', 'Flask', 'HTML/CSS', 'JavaScript'],
        'features': [
            'Time-of-day usage patterns',
            'Seasonal variations analysis',
            'COVID-19 lockdown impact',
            'Regional consumption insights',
            'State-wise comparisons',
            'Quarterly trends analysis'
        ],
        'scenarios': [
            {
                'title': 'Time-of-Day Usage Patterns',
                'description': 'Analyze electricity consumption trends throughout the day across different regions and sectors',
                'insights': ['Peak usage identification', 'Off-peak opportunities', 'Grid optimization']
            },
            {
                'title': 'Seasonal Variations and Forecasting',
                'description': 'Examine seasonal fluctuations in electricity consumption patterns',
                'insights': ['Seasonal peaks', 'Renewable integration', 'Supply planning']
            },
            {
                'title': 'Sector-Specific Consumption Insights',
                'description': 'Explore electricity consumption by different sectors',
                'insights': ['Sector comparisons', 'Conservation programs', 'Efficiency initiatives']
            }
        ]
    }
    return jsonify(project_info)

@app.route('/api/visualization-stats')
def visualization_stats():
    """API endpoint for visualization statistics"""
    stats = {
        'total_visualizations': 12,
        'categories': {
            'time_series': 4,
            'geographical': 3,
            'comparative': 3,
            'statistical': 2
        },
        'visualizations': [
            {
                'id': 1,
                'name': '2019 State Consumption',
                'type': 'Bar Chart',
                'category': 'Comparative',
                'description': 'Electricity consumption by states for 2019'
            },
            {
                'id': 2,
                'name': '2020 State Consumption',
                'type': 'Bar Chart',
                'category': 'Comparative',
                'description': 'Electricity consumption by states for 2020'
            },
            {
                'id': 3,
                'name': 'Total Consumption',
                'type': 'Summary',
                'category': 'Statistical',
                'description': 'Overall consumption summary and statistics'
            },
            {
                'id': 4,
                'name': 'Usage by Region',
                'type': 'Pie Chart',
                'category': 'Comparative',
                'description': 'Regional breakdown of electricity consumption'
            },
            {
                'id': 5,
                'name': 'Top N and Bottom N States',
                'type': 'Ranking',
                'category': 'Comparative',
                'description': 'Highest and lowest consuming states'
            },
            {
                'id': 6,
                'name': '2019 and 2020 Month-wise Consumption',
                'type': 'Line Chart',
                'category': 'Time Series',
                'description': 'Monthly consumption trends for both years'
            },
            {
                'id': 7,
                'name': 'Total Consumption by Region',
                'type': 'Heat Map',
                'category': 'Geographical',
                'description': 'Geographic distribution of consumption'
            },
            {
                'id': 8,
                'name': 'Usage Before and After Lockdown',
                'type': 'Comparison',
                'category': 'Time Series',
                'description': 'COVID-19 lockdown impact analysis'
            },
            {
                'id': 9,
                'name': 'Region-wise State Usage',
                'type': 'Map',
                'category': 'Geographical',
                'description': 'State consumption within regions'
            },
            {
                'id': 10,
                'name': 'Quarter Usage',
                'type': 'Bar Chart',
                'category': 'Time Series',
                'description': 'Quarterly consumption patterns'
            },
            {
                'id': 11,
                'name': 'Metro City State Usage',
                'type': 'Scatter Plot',
                'category': 'Statistical',
                'description': 'Metro cities consumption analysis'
            },
            {
                'id': 12,
                'name': 'Usage by Year',
                'type': 'Comparison',
                'category': 'Time Series',
                'description': 'Year-over-year consumption comparison'
            }
        ]
    }
    return jsonify(stats)

@app.route('/documentation')
def documentation():
    """Project documentation page"""
    return render_template('tableau_documentation.html',
                        title='Project Documentation')

@app.route('/setup-guide')
def setup_guide():
    """Setup guide page"""
    return render_template('tableau_setup.html',
                        title='Setup Guide')

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🎊 Tableau Electricity Consumption Flask Application")
    print("="*60)
    print("🌐 Starting Flask server...")
    print("📊 Tableau Visualizations Integration")
    print("🔗 Available endpoints:")
    print("   / - Main portfolio page")
    print("   /dashboard - Tableau dashboard")
    print("   /story - Tableau story")
    print("   /visualizations - Individual visualizations")
    print("   /analysis - Analysis insights")
    print("   /documentation - Project documentation")
    print("   /setup-guide - Setup instructions")
    print("="*60)
    print("🚀 Server running on http://localhost:5000")
    print("📱 Mobile responsive design enabled")
    print("🔗 Tableau Public integration ready")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
