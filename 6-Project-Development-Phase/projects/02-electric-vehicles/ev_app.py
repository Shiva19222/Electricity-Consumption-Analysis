#!/usr/bin/env python3
"""
Electric Vehicle Analysis Flask Web Application
Comprehensive EV Market Analysis Dashboard
"""

from flask import Flask, render_template, jsonify, request
import mysql.connector
from mysql.connector import Error
import pandas as pd
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ev_analysis_2024_secure'

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Update with your MySQL password
    'database': 'electric_vehicle_analysis',
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
    return render_template('ev_index.html')

@app.route('/dashboard')
def dashboard():
    """Main EV dashboard page"""
    return render_template('ev_dashboard.html')

@app.route('/story')
def story():
    """EV data story page"""
    return render_template('ev_story.html')

@app.route('/api/ev/overview')
def get_ev_overview():
    """Get overall EV market overview"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get overview statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_models,
                COUNT(DISTINCT brand) as unique_brands,
                ROUND(MIN(price), 2) as min_price,
                ROUND(MAX(price), 2) as max_price,
                ROUND(AVG(price), 2) as avg_price,
                ROUND(MIN(range_km), 2) as min_range,
                ROUND(MAX(range_km), 2) as max_range,
                ROUND(AVG(range_km), 2) as avg_range,
                ROUND(AVG(battery_capacity_kwh), 2) as avg_battery,
                COUNT(DISTINCT segment) as segments
            FROM ev_specifications
        """)
        overview = cursor.fetchone()
        
        # Get charging stations count
        cursor.execute("SELECT COUNT(*) as total_stations FROM charging_stations")
        charging = cursor.fetchone()
        
        # Get India market stats
        cursor.execute("SELECT COUNT(*) as india_models, SUM(sales_2024) as total_sales_2024 FROM ev_india_data WHERE sales_2024 > 0")
        india_stats = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        # Combine all data
        result = {
            **overview,
            'total_stations': charging['total_stations'],
            'india_models': india_stats['india_models'],
            'total_sales_2024': india_stats['total_sales_2024'] or 0
        }
        
        return jsonify(result)
        
    except Error as e:
        logging.error(f"Error fetching overview: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ev/brands')
def get_ev_brands():
    """Get brand-wise EV analysis"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get brand comparison data
        cursor.execute("""
            SELECT 
                brand,
                COUNT(*) as total_models,
                ROUND(AVG(price), 2) as avg_price,
                ROUND(MIN(price), 2) as min_price,
                ROUND(MAX(price), 2) as max_price,
                ROUND(AVG(range_km), 2) as avg_range,
                ROUND(MIN(range_km), 2) as min_range,
                ROUND(MAX(range_km), 2) as max_range,
                ROUND(AVG(battery_capacity_kwh), 2) as avg_battery,
                ROUND(AVG(efficiency_km_kwh), 2) as avg_efficiency,
                COUNT(DISTINCT segment) as segments_covered,
                MIN(year) as first_model_year,
                MAX(year) as latest_model_year
            FROM ev_specifications
            GROUP BY brand
            ORDER BY total_models DESC
        """)
        brands = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(brands)
        
    except Error as e:
        logging.error(f"Error fetching brands: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ev/price-range-analysis')
def get_price_range_analysis():
    """Get price vs range analysis"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        price_category = request.args.get('category', 'all')
        brand_filter = request.args.get('brand', 'all')
        
        query = """
            SELECT 
                brand,
                model,
                year,
                price,
                range_km,
                battery_capacity_kwh,
                efficiency_km_kwh,
                fast_charging_kw,
                ROUND(price / range_km, 2) as price_per_km_range,
                ROUND(range_km / battery_capacity_kwh, 2) as range_per_kwh,
                CASE 
                    WHEN price < 30000 THEN 'Budget'
                    WHEN price BETWEEN 30000 AND 60000 THEN 'Mid-Range'
                    WHEN price BETWEEN 60000 AND 100000 THEN 'Premium'
                    ELSE 'Luxury'
                END as price_category,
                CASE 
                    WHEN range_km < 200 THEN 'Short Range'
                    WHEN range_km BETWEEN 200 AND 400 THEN 'Medium Range'
                    WHEN range_km BETWEEN 400 AND 600 THEN 'Long Range'
                    ELSE 'Ultra Long Range'
                END as range_category
            FROM ev_specifications
        """
        
        conditions = []
        params = []
        
        if price_category != 'all':
            conditions.append("price < %s" if price_category == 'Budget' else 
                           "price BETWEEN %s AND %s" if price_category in ['Mid-Range', 'Premium'] else 
                           "price >= %s")
            if price_category == 'Budget':
                params.append(30000)
            elif price_category == 'Mid-Range':
                params.extend([30000, 60000])
            elif price_category == 'Premium':
                params.extend([60000, 100000])
            elif price_category == 'Luxury':
                params.append(100000)
        
        if brand_filter != 'all':
            conditions.append("brand = %s")
            params.append(brand_filter)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY price"
        
        cursor.execute(query, params)
        data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(data)
        
    except Error as e:
        logging.error(f"Error fetching price range analysis: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ev/technology-trends')
def get_technology_trends():
    """Get technology evolution trends"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                year,
                COUNT(*) as total_models,
                ROUND(AVG(battery_capacity_kwh), 2) as avg_battery_capacity,
                ROUND(AVG(range_km), 2) as avg_range,
                ROUND(AVG(price), 2) as avg_price,
                ROUND(AVG(efficiency_km_kwh), 2) as avg_efficiency,
                ROUND(AVG(fast_charging_kw), 2) as avg_charging_speed,
                COUNT(DISTINCT brand) as unique_brands,
                MIN(price) as min_price_year,
                MAX(price) as max_price_year,
                MIN(range_km) as min_range_year,
                MAX(range_km) as max_range_year
            FROM ev_specifications
            GROUP BY year
            ORDER BY year
        """)
        trends = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(trends)
        
    except Error as e:
        logging.error(f"Error fetching technology trends: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ev/charging-infrastructure')
def get_charging_infrastructure():
    """Get charging infrastructure analysis"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        state_filter = request.args.get('state', 'all')
        
        query = """
            SELECT 
                city,
                state,
                country,
                COUNT(*) as total_stations,
                COALESCE(SUM(number_of_ports), 0) as total_ports,
                ROUND(AVG(power_kw), 2) as avg_power_kw,
                MAX(power_kw) as max_power_kw,
                COUNT(DISTINCT operator) as unique_operators,
                GROUP_CONCAT(DISTINCT connector_types) as available_connectors
            FROM charging_stations
        """
        
        params = []
        if state_filter != 'all':
            query += " WHERE state = %s"
            params.append(state_filter)
        
        query += """
            GROUP BY city, state, country
            ORDER BY total_stations DESC
        """
        
        cursor.execute(query, params)
        infrastructure = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(infrastructure)
        
    except Error as e:
        logging.error(f"Error fetching charging infrastructure: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ev/india-market')
def get_india_market():
    """Get India-specific EV market analysis"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                brand,
                model,
                price_inr,
                price_usd,
                range_km,
                battery_capacity_kwh,
                sales_2023,
                sales_2024,
                ROUND(((sales_2024 - sales_2023) / sales_2023) * 100, 2) as sales_growth_percentage,
                market_share_percentage,
                CASE 
                    WHEN price_inr < 1000000 THEN 'Budget'
                    WHEN price_inr BETWEEN 1000000 AND 2000000 THEN 'Mid-Range'
                    WHEN price_inr BETWEEN 2000000 AND 4000000 THEN 'Premium'
                    ELSE 'Luxury'
                END as price_category_inr
            FROM ev_india_data
            WHERE sales_2024 > 0
            ORDER BY sales_2024 DESC
        """)
        india_data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(india_data)
        
    except Error as e:
        logging.error(f"Error fetching India market data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ev/top-models')
def get_top_models():
    """Get top EV models by various metrics"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        metric = request.args.get('metric', 'range')
        limit = request.args.get('limit', 10, type=int)
        
        if metric == 'range':
            query = """
                SELECT brand, model, range_km, price, battery_capacity_kwh, efficiency_km_kwh
                FROM ev_specifications
                ORDER BY range_km DESC
                LIMIT %s
            """
        elif metric == 'price':
            query = """
                SELECT brand, model, price, range_km, battery_capacity_kwh, efficiency_km_kwh
                FROM ev_specifications
                ORDER BY price ASC
                LIMIT %s
            """
        elif metric == 'efficiency':
            query = """
                SELECT brand, model, efficiency_km_kwh, range_km, price, battery_capacity_kwh
                FROM ev_specifications
                WHERE efficiency_km_kwh > 0
                ORDER BY efficiency_km_kwh DESC
                LIMIT %s
            """
        elif metric == 'battery':
            query = """
                SELECT brand, model, battery_capacity_kwh, range_km, price, efficiency_km_kwh
                FROM ev_specifications
                ORDER BY battery_capacity_kwh DESC
                LIMIT %s
            """
        else:
            query = """
                SELECT brand, model, range_km, price, battery_capacity_kwh, efficiency_km_kwh
                FROM ev_specifications
                ORDER BY range_km DESC
                LIMIT %s
            """
        
        cursor.execute(query, (limit,))
        top_models = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(top_models)
        
    except Error as e:
        logging.error(f"Error fetching top models: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ev/segment-analysis')
def get_segment_analysis():
    """Get segment-wise analysis"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                segment,
                COUNT(*) as total_models,
                COUNT(DISTINCT brand) as unique_brands,
                ROUND(AVG(price), 2) as avg_price,
                ROUND(MIN(price), 2) as min_price,
                ROUND(MAX(price), 2) as max_price,
                ROUND(AVG(range_km), 2) as avg_range,
                ROUND(MIN(range_km), 2) as min_range,
                ROUND(MAX(range_km), 2) as max_range,
                ROUND(AVG(battery_capacity_kwh), 2) as avg_battery
            FROM ev_specifications
            WHERE segment IS NOT NULL AND segment != ''
            GROUP BY segment
            ORDER BY total_models DESC
        """)
        segments = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(segments)
        
    except Error as e:
        logging.error(f"Error fetching segment analysis: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ev/kpi-metrics')
def get_kpi_metrics():
    """Get KPI metrics for dashboard"""
    connection = create_database_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        year_filter = request.args.get('year', 'all')
        brand_filter = request.args.get('brand', 'all')
        
        # Base query
        query = """
            SELECT 
                COUNT(*) as total_models,
                COUNT(DISTINCT brand) as active_brands,
                ROUND(AVG(price), 0) as average_price,
                ROUND(MAX(range_km), 0) as max_range,
                ROUND(AVG(range_km), 0) as average_range,
                ROUND(AVG(battery_capacity_kwh), 0) as average_battery
            FROM ev_specifications
        """
        
        params = []
        conditions = []
        
        if year_filter != 'all':
            conditions.append("year = %s")
            params.append(year_filter)
        
        if brand_filter != 'all':
            conditions.append("brand = %s")
            params.append(brand_filter)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        cursor.execute(query, params)
        kpi_data = cursor.fetchone()
        
        # Get year-over-year change
        yoy_query = """
            SELECT 
                ROUND(AVG(CASE WHEN year = 2024 THEN price END), 0) as avg_2024,
                ROUND(AVG(CASE WHEN year = 2023 THEN price END), 0) as avg_2023,
                ROUND(AVG(CASE WHEN year = 2024 THEN range_km END), 0) as range_2024,
                ROUND(AVG(CASE WHEN year = 2023 THEN range_km END), 0) as range_2023
            FROM ev_specifications
            WHERE year IN (2023, 2024)
        """
        
        cursor.execute(yoy_query)
        yoy_data = cursor.fetchone()
        
        # Calculate YoY changes
        price_change = 0
        range_change = 0
        
        if yoy_data['avg_2023'] and yoy_data['avg_2023'] > 0:
            price_change = round(((yoy_data['avg_2024'] - yoy_data['avg_2023']) / yoy_data['avg_2023']) * 100, 1)
        
        if yoy_data['range_2023'] and yoy_data['range_2023'] > 0:
            range_change = round(((yoy_data['range_2024'] - yoy_data['range_2023']) / yoy_data['range_2023']) * 100, 1)
        
        kpi_data['price_yoy_change'] = price_change
        kpi_data['range_yoy_change'] = range_change
        
        cursor.close()
        connection.close()
        
        return jsonify(kpi_data)
        
    except Error as e:
        logging.error(f"Error fetching KPI metrics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ev/health')
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
        'mode': 'ev_analysis'
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
    print("🚗 Electric Vehicle Analysis Dashboard")
    print("="*50)
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("📖 Data Story: http://localhost:5000/story")
    print("🔌 API Health: http://localhost:5000/api/ev/health")
    print("🚀 Starting EV Analysis Application...")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
