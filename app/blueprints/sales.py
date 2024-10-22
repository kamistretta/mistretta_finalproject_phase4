# In sales.py

from flask import Blueprint, render_template
from app.db_connect import get_db
import pandas as pd

sales = Blueprint('sales', __name__)

@sales.route('/show_sales')
def show_sales():
    # Step 1: Establish connection to the database
    connection = get_db()

    # Step 2: Execute the SQL query to fetch all rows from 'sales_data'
    query = "SELECT * FROM sales_data"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    # Step 3: Convert the result to a Pandas DataFrame
    df = pd.DataFrame(result)

    # Step 4: Extract only the rows (<tr>) from the DataFrame HTML output
    table_html = df.to_html(classes='dataframe table table-striped table-bordered', index=False, header=False)
    rows_only = table_html.split('<tbody>')[1].split('</tbody>')[0]

    # Step 5: Render the 'sales_data.html' template with the extracted rows
    return render_template("sales_data.html", table=rows_only)
