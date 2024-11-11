import pandas as pd


# Function to calculate total sales by region
def calculate_total_sales_by_region(sales_data):
    """
    Calculate total sales by region from the provided sales data.

    Parameters:
        sales_data (DataFrame): Pandas DataFrame containing sales data with 'Region' and 'Sales' columns.

    Returns:
        DataFrame: A DataFrame with regions and their corresponding total sales.
    """
    total_sales_by_region = sales_data.groupby('Region')['Sales'].sum().reset_index()
    total_sales_by_region = total_sales_by_region.sort_values(by='Sales', ascending=False)
    return total_sales_by_region


# Function to analyze monthly sales trends
def analyze_monthly_sales_trends(sales_data):
    """
    Analyze monthly sales trends from the provided sales data.

    Parameters:
        sales_data (DataFrame): Pandas DataFrame containing sales data with 'Date' and 'Sales' columns.

    Returns:
        DataFrame: A DataFrame with months and their corresponding total sales.
    """
    # Ensure the 'Date' column is in datetime format
    sales_data['Date'] = pd.to_datetime(sales_data['Date'])

    # Extract month and year from 'Date' column
    sales_data['Month'] = sales_data['Date'].dt.to_period('M')

    # Group by month and calculate total sales per month
    monthly_sales = sales_data.groupby('Month')['Sales'].sum().reset_index()
    monthly_sales = monthly_sales.sort_values(by='Month')
    return monthly_sales


# Function to identify the top-performing region based on total sales
def top_performing_region(sales_data):
    """
    Identify the top-performing region based on total sales.

    Parameters:
        sales_data (DataFrame): Pandas DataFrame containing sales data with 'Region' and 'Sales' columns.

    Returns:
        str: The region with the highest total sales.
    """
    total_sales_by_region = calculate_total_sales_by_region(sales_data)
    top_region = total_sales_by_region.iloc[0]['Region']
    return top_region
