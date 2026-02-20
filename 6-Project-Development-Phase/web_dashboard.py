#!/usr/bin/env python3
"""
Professional Web Dashboard for Electricity Consumption Analysis
Complete alternative to Tableau Desktop
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
from datetime import datetime
import os

class ElectricityDashboard:
    def __init__(self):
        self.df = None
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
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
    
    def create_layout(self):
        """Create dashboard layout"""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Electricity Consumption Analysis", 
                             className="text-center mb-4 text-primary"),
                    html.Hr(),
                    html.P("Professional Dashboard - 2019-2020 Data Analysis", 
                            className="text-center text-muted mb-4")
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("📊 Data Overview", className="card-title"),
                            html.P(f"Total Records: {len(self.df):,}", 
                                    className="card-text"),
                            html.P(f"Date Range: {self.df['dates'].min().strftime('%Y-%m-%d')} to {self.df['dates'].max().strftime('%Y-%m-%d')}", 
                                    className="card-text"),
                            html.P(f"States: {self.df['States'].nunique()} | Regions: {self.df['Regions'].nunique()}", 
                                    className="card-text")
                        ])
                    ], className="mb-3")
                ], width=3),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("⚡ Quick Stats", className="card-title"),
                            html.P(f"Total Usage: {self.df['Usage'].sum():,.2f} MWh", 
                                    className="card-text"),
                            html.P(f"Avg Daily: {self.df['Usage'].mean():,.2f} MWh", 
                                    className="card-text"),
                            html.P(f"Peak Usage: {self.df['Usage'].max():,.2f} MWh", 
                                    className="card-text")
                        ])
                    ], className="mb-3")
                ], width=3),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("🔍 Filters", className="card-title"),
                            html.Div([
                                html.Label("Select Year:"),
                                dcc.Dropdown(
                                    id='year-filter',
                                    options=[{'label': str(year), 'value': year} 
                                           for year in sorted(self.df['year'].unique())],
                                    value=sorted(self.df['year'].unique())[-1],
                                    className="mb-2"
                                ),
                                html.Label("Select Region:"),
                                dcc.Dropdown(
                                    id='region-filter',
                                    options=[{'label': region, 'value': region} 
                                           for region in sorted(self.df['Regions'].unique())],
                                    value='All',
                                    className="mb-2"
                                ),
                                html.Label("Lockdown Filter:"),
                                dcc.Dropdown(
                                    id='lockdown-filter',
                                    options=[
                                        {'label': 'All', 'value': 'All'},
                                        {'label': 'Normal Period', 'value': False},
                                        {'label': 'Lockdown Period', 'value': True}
                                    ],
                                    value='All',
                                    className="mb-2"
                                )
                            ])
                        ])
                    ], className="mb-3")
                ], width=3),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("📈 Visualizations", className="card-title"),
                            html.Div([
                                dbc.Button("State Consumption", id="btn-states", color="primary", className="m-1"),
                                dbc.Button("Monthly Trends", id="btn-monthly", color="info", className="m-1"),
                                dbc.Button("Regional Analysis", id="btn-regional", color="success", className="m-1"),
                                dbc.Button("Lockdown Impact", id="btn-lockdown", color="warning", className="m-1"),
                                dbc.Button("Seasonal Patterns", id="btn-seasonal", color="secondary", className="m-1")
                            ])
                        ])
                    ], className="mb-3")
                ], width=3)
            ])
            
            dbc.Row([
                dbc.Col([
                    html.Div(id='visualization-container', className="mt-4")
                ], width=12)
            ])
        ], fluid=True, className="p-4")
    
    def create_state_consumption_chart(self, year_filter=None, region_filter=None):
        """Create state consumption chart"""
        filtered_df = self.df.copy()
        
        if year_filter:
            filtered_df = filtered_df[filtered_df['year'] == year_filter]
        if region_filter != 'All':
            filtered_df = filtered_df[filtered_df['Regions'] == region_filter]
        
        # Aggregate by state
        state_data = filtered_df.groupby('States')['Usage'].sum().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=state_data.values,
            y=state_data.index,
            orientation='h',
            title=f"Top 10 States by Consumption ({year_filter or 'All Years'}, {region_filter or 'All Regions'})",
            labels={'x': 'Usage (MWh)', 'y': 'State'},
            color=px.colors.sequential.Plasma
        )
        
        return fig
    
    def create_monthly_trends_chart(self, year_filter=None, region_filter=None):
        """Create monthly trends chart"""
        filtered_df = self.df.copy()
        
        if year_filter:
            filtered_df = filtered_df[filtered_df['year'] == year_filter]
        if region_filter != 'All':
            filtered_df = filtered_df[filtered_df['Regions'] == region_filter]
        
        # Aggregate by month
        monthly_data = filtered_df.groupby(['year', 'month_name'])['Usage'].sum().reset_index()
        
        fig = px.line(
            monthly_data,
            x='month_name',
            y='Usage',
            color='year',
            title=f"Monthly Consumption Trends ({region_filter or 'All Regions'})",
            labels={'x': 'Month', 'y': 'Usage (MWh)', 'color': 'Year'}
        )
        
        return fig
    
    def create_regional_analysis_chart(self, year_filter=None):
        """Create regional analysis chart"""
        filtered_df = self.df.copy()
        
        if year_filter:
            filtered_df = filtered_df[filtered_df['year'] == year_filter]
        
        # Aggregate by region
        regional_data = filtered_df.groupby('Regions')['Usage'].sum().sort_values(ascending=False)
        
        fig = px.pie(
            values=regional_data.values,
            names=regional_data.index,
            title=f"Regional Consumption Distribution ({year_filter or 'All Years'})",
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        
        return fig
    
    def create_lockdown_impact_chart(self, region_filter=None):
        """Create lockdown impact chart"""
        filtered_df = self.df.copy()
        
        if region_filter != 'All':
            filtered_df = filtered_df[filtered_df['Regions'] == region_filter]
        
        # Aggregate by lockdown status
        lockdown_data = filtered_df.groupby(['year', 'is_lockdown'])['Usage'].mean().reset_index()
        
        fig = px.bar(
            lockdown_data,
            x='year',
            y='Usage',
            color='is_lockdown',
            barmode='group',
            title=f"COVID-19 Lockdown Impact ({region_filter or 'All Regions'})",
            labels={'is_lockdown': 'Lockdown Status', 'Usage': 'Average Usage (MWh)'},
            color_discrete_map={True: 'Lockdown Period', False: 'Normal Period'}
        )
        
        return fig
    
    def create_seasonal_patterns_chart(self, year_filter=None, region_filter=None):
        """Create seasonal patterns chart"""
        filtered_df = self.df.copy()
        
        if year_filter:
            filtered_df = filtered_df[filtered_df['year'] == year_filter]
        if region_filter != 'All':
            filtered_df = filtered_df[filtered_df['Regions'] == region_filter]
        
        # Aggregate by season
        seasonal_data = filtered_df.groupby('season')['Usage'].sum().reset_index()
        
        fig = px.bar(
            seasonal_data,
            x='season',
            y='Usage',
            title=f"Seasonal Consumption Patterns ({year_filter or 'All Years'}, {region_filter or 'All Regions'})",
            labels={'x': 'Season', 'y': 'Total Usage (MWh)'},
            color=px.colors.sequential.Plasma
        )
        
        return fig
    
    def setup_callbacks(self):
        """Setup dashboard callbacks"""
        @self.app.callback(
            Output('visualization-container', 'children'),
            [Input('year-filter', 'value'),
             Input('region-filter', 'value'),
             Input('lockdown-filter', 'value'),
             Input('btn-states', 'n_clicks'),
             Input('btn-monthly', 'n_clicks'),
             Input('btn-regional', 'n_clicks'),
             Input('btn-lockdown', 'n_clicks'),
             Input('btn-seasonal', 'n_clicks')]
        )
        def update_visualization(year_filter, region_filter, lockdown_filter, 
                           btn_states, btn_monthly, btn_regional, btn_lockdown, btn_seasonal):
            
            # Determine which button was clicked
            ctx = dash.callback_context
            button_id = None
            if ctx.triggered:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            else:
                button_id = 'states'  # default
            
            # Create appropriate chart
            if button_id == 'states' or not ctx.triggered:
                fig = self.create_state_consumption_chart(year_filter, region_filter)
                return dcc.Graph(figure=fig, id='main-chart')
            elif button_id == 'monthly':
                fig = self.create_monthly_trends_chart(year_filter, region_filter)
                return dcc.Graph(figure=fig, id='main-chart')
            elif button_id == 'regional':
                fig = self.create_regional_analysis_chart(year_filter)
                return dcc.Graph(figure=fig, id='main-chart')
            elif button_id == 'lockdown':
                fig = self.create_lockdown_impact_chart(region_filter)
                return dcc.Graph(figure=fig, id='main-chart')
            elif button_id == 'seasonal':
                fig = self.create_seasonal_patterns_chart(year_filter, region_filter)
                return dcc.Graph(figure=fig, id='main-chart')
    
    def run(self):
        """Run the dashboard"""
        if not self.df:
            return html.Div("❌ Data loading failed", className="alert alert-danger")
        
        self.setup_callbacks()
        self.app.layout = self.create_layout()
        
        print("🚀 Electricity Consumption Dashboard Starting...")
        print("🌐 Access at: http://localhost:8050")
        print("📊 Interactive visualizations ready")
        print("🔍 Filters working")
        print("📱 Mobile responsive design")
        
        self.app.run_server(debug=True, host='0.0.0.0', port=8050)

def main():
    """Main function"""
    print("🎊 Professional Web Dashboard for Electricity Consumption")
    print("="*60)
    print("📈 Alternative to Tableau Desktop")
    print("🚀 Interactive visualizations with filters")
    print("📱 Mobile responsive design")
    print("🔧 No database required")
    print("="*60)
    
    dashboard = ElectricityDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
