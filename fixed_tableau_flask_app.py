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

# Tableau Public URLs with individual sheet parameters
TABLEAU_VIEWS = {
    'dashboard': 'https://public.tableau.com/app/profile/shva.sai/viz/ElectricityConsumptionAnalysis_17713957778860/Dashboard1?publish=yes',
    'story': 'https://public.tableau.com/app/profile/shva.sai/viz/ElectricityConsumptionAnalysis_17713957778860/Dashboard1?publish=yes',
    'viz_2019_states': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis_17713957778860/Sheet1?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link',
    'viz_2020_states': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis_17713957778860/Sheet12?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link',
    'viz_total_consumption': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis_17713957778860/Sheet3?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link',
    'viz_usage_by_region': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis_17713957778860/Sheet4?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link',
    'viz_top_bottom_states': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis_17713957778860/Sheet5?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link',
    'viz_monthly_trends': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis_17713957778860/Sheet6?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link',
    'viz_region_heatmap': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis_17713957778860/Sheet7?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link',
    'viz_lockdown_impact': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis_17713957778860/Sheet8?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link',
    'viz_state_map': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis_17713957778860/Sheet9?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link',
    'viz_quarter_usage': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis_17713957778860/Sheet10?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link',
    'viz_metro_analysis': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis_17713957778860/Sheet11?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link',
    'viz_yearly_comparison': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis_17713957778860/Sheet12_1?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link'
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
    """Visualizations page"""
    return render_template('tableau_visualizations_fixed.html',
                        tableau_views=TABLEAU_VIEWS,
                        title='Electricity Consumption Visualizations')

@app.route('/analysis/time-patterns')
def analysis_time_patterns():
    """Time-of-Day Usage Patterns analysis"""
    return render_template('analysis_time_patterns.html',
                        tableau_views=TABLEAU_VIEWS,
                        title='Time-of-Day Usage Patterns Analysis')

@app.route('/analysis/seasonal-variations')
def analysis_seasonal_variations():
    """Seasonal Variations and Forecasting analysis"""
    return render_template('analysis_seasonal_variations.html',
                        tableau_views=TABLEAU_VIEWS,
                        title='Seasonal Variations and Forecasting Analysis')

@app.route('/analysis/sector-specific')
def analysis_sector_specific():
    """Sector-Specific Consumption analysis"""
    return render_template('analysis_sector_specific.html',
                        tableau_views=TABLEAU_VIEWS,
                        title='Sector-Specific Consumption Analysis')

@app.route('/analysis')
def analysis():
    """Analysis page - overview of all scenarios"""
    return render_template('tableau_analysis.html',
                        tableau_views=TABLEAU_VIEWS,
                        title='Electricity Consumption Analysis')

@app.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('tableau_documentation.html',
                        title='Project Documentation')

# Individual visualization routes
@app.route('/visualization/2019-states')
def viz_2019_states():
    """2019 State Consumption visualization"""
    return render_template('individual_viz.html',
                        tableau_url=TABLEAU_VIEWS['viz_2019_states'],
                        title='2019 State Consumption',
                        description='Bar chart showing electricity consumption by Indian states for 2019',
                        activity='Activity 1.1',
                        viz_type='Bar Chart')

@app.route('/visualization/2020-states')
def viz_2020_states():
    """2020 State Consumption visualization"""
    return render_template('individual_viz.html',
                        tableau_url=TABLEAU_VIEWS['viz_2020_states'],
                        title='2020 State Consumption',
                        description='Bar chart showing electricity consumption by Indian states for 2020',
                        activity='Activity 1.1',
                        viz_type='Bar Chart')

@app.route('/visualization/total-consumption')
def viz_total_consumption():
    """Total Consumption visualization"""
    return render_template('individual_viz.html',
                        tableau_url=TABLEAU_VIEWS['viz_total_consumption'],
                        title='Total Consumption',
                        description='Summary card showing overall electricity consumption statistics',
                        activity='Activity 1.1',
                        viz_type='Summary Card')

@app.route('/visualization/usage-by-region')
def viz_usage_by_region():
    """Usage by Region visualization"""
    return render_template('individual_viz.html',
                        tableau_url=TABLEAU_VIEWS['viz_usage_by_region'],
                        title='Usage by Region',
                        description='Pie chart showing regional breakdown of electricity consumption',
                        activity='Activity 1.1',
                        viz_type='Pie Chart')

@app.route('/visualization/top-bottom-states')
def viz_top_bottom_states():
    """Top N and Bottom N States visualization"""
    return render_template('individual_viz.html',
                        tableau_url=TABLEAU_VIEWS['viz_top_bottom_states'],
                        title='Top N and Bottom N States',
                        description='Ranking chart showing highest and lowest consuming states',
                        activity='Activity 1.1',
                        viz_type='Ranking Chart')

@app.route('/visualization/monthly-trends')
def viz_monthly_trends():
    """Monthly Trends visualization"""
    return render_template('individual_viz.html',
                        tableau_url=TABLEAU_VIEWS['viz_monthly_trends'],
                        title='2019 and 2020 Month-wise Consumption',
                        description='Line chart showing monthly consumption trends for both years',
                        activity='Activity 1.2',
                        viz_type='Line Chart')

@app.route('/visualization/region-heatmap')
def viz_region_heatmap():
    """Region Heatmap visualization"""
    return render_template('individual_viz.html',
                        tableau_url=TABLEAU_VIEWS['viz_region_heatmap'],
                        title='Total Consumption Region Wise',
                        description='Heat map showing total consumption by regions',
                        activity='Activity 1.2',
                        viz_type='Heat Map')

@app.route('/visualization/lockdown-impact')
def viz_lockdown_impact():
    """Lockdown Impact visualization"""
    return render_template('individual_viz.html',
                        tableau_url=TABLEAU_VIEWS['viz_lockdown_impact'],
                        title='Usage Before and After Lockdown',
                        description='Bar chart comparing consumption before and after COVID-19 lockdowns',
                        activity='Activity 1.2',
                        viz_type='Bar Chart')

@app.route('/visualization/state-map')
def viz_state_map():
    """State Map visualization"""
    return render_template('individual_viz.html',
                        tableau_url=TABLEAU_VIEWS['viz_state_map'],
                        title='Region wise State Usage',
                        description='Filled map showing electricity consumption by states',
                        activity='Activity 1.3',
                        viz_type='Filled Map')

@app.route('/visualization/quarter-usage')
def viz_quarter_usage():
    """Quarter Usage visualization"""
    return render_template('individual_viz.html',
                        tableau_url=TABLEAU_VIEWS['viz_quarter_usage'],
                        title='Quarter Usage',
                        description='Bar chart showing electricity consumption by quarters',
                        activity='Activity 1.3',
                        viz_type='Bar Chart')

@app.route('/visualization/metro-analysis')
def viz_metro_analysis():
    """Metro Analysis visualization"""
    return render_template('individual_viz.html',
                        tableau_url=TABLEAU_VIEWS['viz_metro_analysis'],
                        title='Metro City State Usage',
                        description='Scatter plot showing consumption patterns in metropolitan cities',
                        activity='Activity 1.3',
                        viz_type='Scatter Plot')

@app.route('/visualization/yearly-comparison')
def viz_yearly_comparison():
    """Yearly Comparison visualization"""
    return render_template('individual_viz.html',
                        tableau_url=TABLEAU_VIEWS['viz_yearly_comparison'],
                        title='Usage by Year',
                        description='Bar chart showing year-over-year electricity consumption comparison',
                        activity='Activity 1.3',
                        viz_type='Bar Chart')

@app.route('/api/project-info')
def api_project_info():
    """API endpoint for project information"""
    project_info = {
        'title': 'Plugging into the Future: An Exploration of Electricity Consumption Patterns Using Tableau',
        'description': 'Professional data visualization project analyzing electricity consumption patterns across India',
        'dataset': '16,599 records from 2019-2020',
        'visualizations': 12,
        'dashboard': 'Interactive dashboard with filters',
        'story': '5-scene narrative analysis',
        'technologies': ['Tableau Desktop', 'Tableau Public', 'Flask', 'Python', 'MySQL'],
        'completion': '100%',
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(project_info)

@app.route('/api/visualizations')
def api_visualizations():
    """API endpoint for visualizations list"""
    visualizations = [
        {'id': 1, 'name': '2019 State Consumption', 'type': 'Bar Chart', 'activity': '1.1'},
        {'id': 2, 'name': '2020 State Consumption', 'type': 'Bar Chart', 'activity': '1.1'},
        {'id': 3, 'name': 'Total Consumption', 'type': 'Summary Card', 'activity': '1.1'},
        {'id': 4, 'name': 'Usage by Region', 'type': 'Pie Chart', 'activity': '1.1'},
        {'id': 5, 'name': 'Top N and Bottom N States', 'type': 'Ranking Chart', 'activity': '1.1'},
        {'id': 6, 'name': '2019 and 2020 Month-wise Consumption', 'type': 'Line Chart', 'activity': '1.2'},
        {'id': 7, 'name': 'Total Consumption Region Wise', 'type': 'Heat Map', 'activity': '1.2'},
        {'id': 8, 'name': 'Usage Before and After Lockdown', 'type': 'Bar Chart', 'activity': '1.2'},
        {'id': 9, 'name': 'Region wise State Usage', 'type': 'Filled Map', 'activity': '1.3'},
        {'id': 10, 'name': 'Quarter Usage', 'type': 'Bar Chart', 'activity': '1.3'},
        {'id': 11, 'name': 'Metro City State Usage', 'type': 'Scatter Plot', 'activity': '1.3'},
        {'id': 12, 'name': 'Usage by Year', 'type': 'Bar Chart', 'activity': '1.3'}
    ]
    return jsonify(visualizations)

@app.route('/api/dataset-info')
def api_dataset_info():
    """API endpoint for dataset information"""
    dataset_info = {
        'filename': 'Tableau_Ready_Data.csv',
        'records': 16599,
        'columns': 20,
        'date_range': '2019-01-02 to 2020-12-05',
        'states': 35,
        'regions': 5,
        'years': [2019, 2020],
        'enhanced_fields': [
            'year', 'month', 'month_name', 'quarter', 'quarter_name',
            'day_of_week', 'day_name', 'week_of_year',
            'is_lockdown', 'lockdown_phase', 'season',
            'is_summer', 'is_winter', 'is_monsoon',
            'is_metro', 'usage_category', 'usage_level'
        ]
    }
    return jsonify(dataset_info)

if __name__ == '__main__':
    print("Tableau Electricity Consumption Flask Application")
    print("=" * 50)
    print("Starting web server...")
    print("Access at: http://localhost:5000")
    print("Dashboard: http://localhost:5000/dashboard")
    print("Story: http://localhost:5000/story")
    print("Visualizations: http://localhost:5000/visualizations")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
