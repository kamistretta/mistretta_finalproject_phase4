from flask import render_template
import yfinance as yf
import pandas as pd
import plotly.express as px

from . import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reports')
def reports():
    # Sample data (replace with your actual sales data)
    data = {
        'Date': ['2024-01-01', '2024-01-02', '2024-01-10', '2024-02-01', '2024-02-15', '2024-02-20'],
        'Region': ['North', 'South', 'East', 'North', 'East', 'South'],
        'Sales': [2000, 1500, 1800, 2200, 1700, 2500]
    }

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Convert Date to datetime format for analysis
    df['Date'] = pd.to_datetime(df['Date'])

    # 1. Total Sales by Region
    total_sales_by_region = df.groupby('Region')['Sales'].sum().reset_index()

    # 2. Monthly Sales Trend
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_sales = df.groupby('Month')['Sales'].sum().reset_index()

    # 3. Top-Performing Region
    top_region = df.groupby('Region')['Sales'].sum().idxmax()

    # Convert the DataFrames to HTML for rendering in the template
    total_sales_by_region_html = total_sales_by_region.to_html(classes='table table-bordered table-striped',
                                                               index=False)
    monthly_sales_html = monthly_sales.to_html(classes='table table-bordered table-striped', index=False)

    return render_template('reports.html',
                           total_sales_by_region=total_sales_by_region_html,
                           monthly_sales=monthly_sales_html,
                           top_region=top_region)


# Example Flask route to render the visualization page
@app.route('/visualization')
def visualization():
    # Sample sales data (replace with your actual data)
    data = {
        'Region': ['North', 'South', 'East', 'West'],
        'Sales': [2500, 3000, 1500, 2200]
    }

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Create a bar chart using Plotly
    fig = px.bar(df, x='Region', y='Sales', title='Sales by Region')

    # Convert the Plotly figure to HTML
    graph_html = fig.to_html(full_html=False)

    return render_template('visualization.html', graph_html=graph_html)