from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

sales_data = Blueprint('sales_data', __name__)

@sales_data.route('/sales', methods=['GET', 'POST'])
def sales():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new movie
    if request.method == 'POST':
        monthly_amount = request.form['monthly_amount']
        date = request.form['date']
        region = request.form['region']

        # Insert the new movie info into the database
        cursor.execute('INSERT INTO sales_data (monthly_amount, date, region) VALUES (%s, %s, %s)',
                       (monthly_amount, date, region))
        db.commit()

        flash('New sales data added successfully!', 'success')
        return redirect(url_for('sales_data.sales'))

    # Handle GET request for filtering
    monthly_amount_filter = request.args.get('monthly_amount')
    date_filter = request.args.get('date')
    region_filter = request.args.get('region')

    # Construct SQL query for filtering
    query = 'SELECT * FROM sales_data WHERE TRUE'
    params = []

    if monthly_amount_filter:
        query += ' AND monthly_amount LIKE %s'
        params.append(f'%{monthly_amount_filter}%')

    if date_filter:
        query += ' AND date LIKE %s'
        params.append(f'%{date_filter}%')

    if region_filter:
        query += ' AND region = %s'
        params.append(region_filter)

    cursor.execute(query, params)
    all_sales = cursor.fetchall()

    return render_template('sales_data.html', all_sales=all_sales)

@sales_data.route('/update_sales/<int:sales_data_id>', methods=['GET', 'POST'])
def update_sales(sales_data_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the sale's's details
        monthly_amount = request.form['monthly_amount']
        date = request.form['date']
        region = request.form['region']

        cursor.execute('UPDATE sales_data SET monthly_amount = %s, date = %s, region = %s WHERE sales_data_id = %s',
                       (monthly_amount, date, region, sales_data_id))
        db.commit()

        flash('Sales data updated successfully!', 'success')
        return redirect(url_for('sales_data.sales'))

    # GET method: fetch sale's current data for pre-populating the form
    cursor.execute('SELECT * FROM sales_data WHERE sales_data_id = %s', (sales_data_id,))
    current_sales_data = cursor.fetchone()
    return render_template('sales_data_update.html', current_sales_data=current_sales_data)

@sales_data.route('/delete_sales/<int:sales_data_id>', methods=['POST'])
def delete_sales(sales_data_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the sale
    cursor.execute('DELETE FROM sales_data WHERE sales_data_id = %s', (sales_data_id,))
    db.commit()

    flash('Sale deleted successfully!', 'danger')
    return redirect(url_for('sales_data.sales'))
