from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

region_info = Blueprint('region_info', __name__)

@region_info.route('/regions', methods=['GET', 'POST'])
def regions():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new genre
    if request.method == 'POST':
        region = request.form['region']

        # Insert the new genre into the database
        cursor.execute('INSERT INTO region_info (region) VALUES (%s)', (region,))
        db.commit()

        flash('New region added successfully!', 'success')
        return redirect(url_for('region_info.regions'))

    # Handle GET request to display all regions
    cursor.execute('SELECT * FROM region_info')
    all_regions = cursor.fetchall()
    return render_template('regions.html', all_regions=all_regions)  # Ensure this matches your file name

@region_info.route('/update_region/<int:region_id>', methods=['GET', 'POST'])
def update_region(region_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the region's details
        region = request.form['region']

        cursor.execute('UPDATE region_info SET region = %s WHERE region_id = %s', (region, region_id))
        db.commit()

        flash('Region updated successfully!', 'success')
        return redirect(url_for('region_info.regions'))

    # GET method: fetch region's current data for pre-populating the form
    cursor.execute('SELECT * FROM region_info WHERE region_id = %s', (region_id,))
    current_region_info = cursor.fetchone()
    return render_template('region_update.html', current_region_info=current_region_info)

@region_info.route('/delete_region/<int:region_id>', methods=['POST'])
def delete_region(region_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the genre
    cursor.execute('DELETE FROM region_info WHERE region_id = %s', (region_id,))
    db.commit()

    flash('Region deleted successfully!', 'danger')
    return redirect(url_for('region_info.regions'))
