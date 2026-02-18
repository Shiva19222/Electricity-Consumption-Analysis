#!/usr/bin/env python3
"""
Flask Web Application for Electricity Consumption Analysis
Updated for Original Dataset Structure
"""

from flask import Flask, render_template, jsonify, request
import mysql.connector
from mysql.connector import Error
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'electricity_consumption_original_2024'

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Update with your MySQL password
    'database': 'electricity_consumption',
    'raise_on_warnings': True
}

def create_database_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        logging.error(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/story')
def story():
    """Data story page"""
    return render_template('story.html')

@app.route('/api/consumption/summary')
def get_consumption_summary():
    """Get overall consumption summary"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get summary statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT c.state_id) as states_covered,
                COUNT(DISTINCT s.region) as regions_covered,
                ROUND(SUM(c.usage_value), 2) as total_consumption,
                ROUND(AVG(c.usage_value), 2) as average_consumption,
                ROUND(MAX(c.usage_value), 2) as peak_consumption,
                ROUND(MIN(c.usage_value), 2) as minimum_consumption,
                ROUND(STDDEV(c.usage_value), 2) as consumption_std_dev
            FROM consumption c
            JOIN states s ON c.state_id = s.state_id
        """)
        summary = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return jsonify(summary)
        
    except Error as e:
        logging.error(f"Error fetching summary: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/consumption/yearly')
def get_yearly_consumption():
    """Get year-wise consumption data"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        year_filter = request.args.get('year', 'all')
        region_filter = request.args.get('region', 'all')
        
        query = """
            SELECT 
                s.state_name,
                s.region,
                YEAR(c.consumption_date) as analysis_year,
                ROUND(SUM(c.usage_value), 2) as total_consumption,
                ROUND(AVG(c.usage_value), 2) as average_consumption,
                ROUND(MAX(c.usage_value), 2) as peak_consumption,
                ROUND(MIN(c.usage_value), 2) as minimum_consumption,
                COUNT(*) as data_points
            FROM consumption c
            JOIN states s ON c.state_id = s.state_id
        """
        
        conditions = []
        params = []
        
        if year_filter != 'all':
            conditions.append("YEAR(c.consumption_date) = %s")
            params.append(year_filter)
        
        if region_filter != 'all':
            conditions.append("s.region = %s")
            params.append(region_filter)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += """
            GROUP BY s.state_name, s.region, YEAR(c.consumption_date)
            ORDER BY total_consumption DESC
        """
        
        cursor.execute(query, params)
        data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(data)
        
    except Error as e:
        logging.error(f"Error fetching yearly data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/consumption/regional')
def get_regional_consumption():
    """Get regional consumption data"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT 
                s.region,
                YEAR(c.consumption_date) as analysis_year,
                MONTH(c.consumption_date) as analysis_month,
                ROUND(SUM(c.usage_value), 2) as regional_total,
                ROUND(AVG(c.usage_value), 2) as regional_average,
                ROUND(MAX(c.usage_value), 2) as regional_peak,
                ROUND(MIN(c.usage_value), 2) as regional_minimum,
                COUNT(DISTINCT s.state_id) as state_count
            FROM consumption c
            JOIN states s ON c.state_id = s.state_id
            GROUP BY s.region, YEAR(c.consumption_date), MONTH(c.consumption_date)
            ORDER BY s.region, analysis_year, analysis_month
        """
        
        cursor.execute(query)
        data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(data)
        
    except Error as e:
        logging.error(f"Error fetching regional data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/consumption/monthly')
def get_monthly_consumption():
    """Get monthly consumption trends"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT 
                YEAR(c.consumption_date) as analysis_year,
                MONTH(c.consumption_date) as analysis_month,
                MONTHNAME(c.consumption_date) as month_name,
                ROUND(SUM(c.usage_value), 2) as monthly_total,
                ROUND(AVG(c.usage_value), 2) as daily_average,
                ROUND(MAX(c.usage_value), 2) as monthly_peak,
                ROUND(MIN(c.usage_value), 2) as monthly_minimum,
                COUNT(DISTINCT c.consumption_date) as days_in_month
            FROM consumption c
            GROUP BY YEAR(c.consumption_date), MONTH(c.consumption_date)
            ORDER BY analysis_year, analysis_month
        """
        
        cursor.execute(query)
        data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(data)
        
    except Error as e:
        logging.error(f"Error fetching monthly data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/consumption/top-states')
def get_top_states():
    """Get top states by consumption"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        limit = request.args.get('limit', 10, type=int)
        year_filter = request.args.get('year', 'all')
        
        query = """
            SELECT 
                s.state_name,
                s.region,
                ROUND(SUM(c.usage_value), 2) as total_consumption,
                ROUND(AVG(c.usage_value), 2) as average_consumption,
                ROUND(MAX(c.usage_value), 2) as peak_consumption,
                ROUND(MIN(c.usage_value), 2) as minimum_consumption,
                COUNT(*) as data_points,
                ROUND((SUM(c.usage_value) / (SELECT SUM(usage_value) FROM consumption)) * 100, 2) as market_share_percentage
            FROM consumption c
            JOIN states s ON c.state_id = s.state_id
        """
        
        params = []
        if year_filter != 'all':
            query += " WHERE YEAR(c.consumption_date) = %s"
            params.append(year_filter)
        
        query += """
            GROUP BY s.state_name, s.region
            ORDER BY total_consumption DESC
            LIMIT %s
        """
        params.append(limit)
        
        cursor.execute(query, params)
        data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(data)
        
    except Error as e:
        logging.error(f"Error fetching top states: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/consumption/lockdown-impact')
def get_lockdown_impact():
    """Get lockdown impact analysis"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT 
                s.state_name,
                s.region,
                ROUND(AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END), 2) as pre_lockdown_avg,
                ROUND(AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END), 2) as during_lockdown_avg,
                ROUND(AVG(CASE WHEN c.consumption_date > '2020-05-31' THEN c.usage_value END), 2) as post_lockdown_avg,
                ROUND(
                    ((AVG(CASE WHEN c.consumption_date BETWEEN '2020-03-25' AND '2020-05-31' THEN c.usage_value END) - 
                      AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END)) / 
                     AVG(CASE WHEN c.consumption_date BETWEEN '2020-01-01' AND '2020-03-24' THEN c.usage_value END)) * 100, 2
                ) as lockdown_impact_percentage
            FROM consumption c
            JOIN states s ON c.state_id = s.state_id
            WHERE YEAR(c.consumption_date) = 2020
            GROUP BY s.state_name, s.region
            HAVING pre_lockdown_avg IS NOT NULL AND during_lockdown_avg IS NOT NULL
            ORDER BY lockdown_impact_percentage ASC
        """
        
        cursor.execute(query)
        data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(data)
        
    except Error as e:
        logging.error(f"Error fetching lockdown impact: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/consumption/seasonal')
def get_seasonal_consumption():
    """Get seasonal consumption patterns"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT 
                CASE 
                    WHEN MONTH(c.consumption_date) IN (12, 1, 2) THEN 'Winter'
                    WHEN MONTH(c.consumption_date) IN (3, 4, 5) THEN 'Summer'
                    WHEN MONTH(c.consumption_date) IN (6, 7, 8, 9) THEN 'Monsoon'
                    ELSE 'Post-Monsoon'
                END as season,
                YEAR(c.consumption_date) as analysis_year,
                ROUND(SUM(c.usage_value), 2) as seasonal_total,
                ROUND(AVG(c.usage_value), 2) as daily_average,
                ROUND(MAX(c.usage_value), 2) as seasonal_peak,
                ROUND(MIN(c.usage_value), 2) as seasonal_minimum,
                COUNT(DISTINCT c.consumption_date) as days_in_season
            FROM consumption c
            GROUP BY season, YEAR(c.consumption_date)
            ORDER BY analysis_year, 
                CASE season 
                    WHEN 'Winter' THEN 1
                    WHEN 'Summer' THEN 2
                    WHEN 'Monsoon' THEN 3
                    WHEN 'Post-Monsoon' THEN 4
                END
        """
        
        cursor.execute(query)
        data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(data)
        
    except Error as e:
        logging.error(f"Error fetching seasonal data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/kpi/metrics')
def get_kpi_metrics():
    """Get KPI metrics for dashboard"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        year_filter = request.args.get('year', 'all')
        region_filter = request.args.get('region', 'all')
        
        # Base query
        query = """
            SELECT 
                ROUND(SUM(c.usage_value), 0) as total_consumption,
                ROUND(AVG(c.usage_value), 0) as average_consumption,
                ROUND(MAX(c.usage_value), 0) as peak_consumption,
                COUNT(DISTINCT c.state_id) as active_states
            FROM consumption c
            JOIN states s ON c.state_id = s.state_id
        """
        
        params = []
        conditions = []
        
        if year_filter != 'all':
            conditions.append("YEAR(c.consumption_date) = %s")
            params.append(year_filter)
        
        if region_filter != 'all':
            conditions.append("s.region = %s")
            params.append(region_filter)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        cursor.execute(query, params)
        kpi_data = cursor.fetchone()
        
        # Calculate year-over-year change
        yoy_query = """
            SELECT 
                ROUND(SUM(CASE WHEN YEAR(consumption_date) = 2020 THEN usage_value END), 0) as y2020,
                ROUND(SUM(CASE WHEN YEAR(consumption_date) = 2019 THEN usage_value END), 0) as y2019
            FROM consumption
        """
        
        cursor.execute(yoy_query)
        yoy_data = cursor.fetchone()
        
        # Calculate YoY change percentage
        yoy_change = 0
        if yoy_data['y2019'] and yoy_data['y2019'] > 0:
            yoy_change = round(((yoy_data['y2020'] - yoy_data['y2019']) / yoy_data['y2019']) * 100, 1)
        
        kpi_data['yoy_change'] = yoy_change
        
        cursor.close()
        connection.close()
        
        return jsonify(kpi_data)
        
    except Error as e:
        logging.error(f"Error fetching KPI metrics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tableau/embed')
def get_tableau_embed():
    """Get Tableau embed configuration"""
    tableau_config = {
        'url': 'https://public.tableau.com/views/ElectricityConsumptionAnalysis/Dashboard',
        'width': '100%',
        'height': '800px',
        'hideTabs': True,
        'hideToolbar': True
    }
    return jsonify(tableau_config)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    connection = create_database_connection()
    db_connected = connection is not None
    
    if connection:
        connection.close()
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database_connected': db_connected,
        'mode': 'production'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Electricity Consumption Analysis - Production Mode")
    print("Dashboard: http://localhost:5000/dashboard")
    print("Data Story: http://localhost:5000/story")
    print("API Health: http://localhost:5000/api/health")
    print("Running with original dataset and database")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
