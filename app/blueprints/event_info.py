from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import plotly.express as px
import pandas as pd
from app.db_connect import get_db

event_info = Blueprint('event_info', __name__)

@event_info.route('/events', methods=['GET', 'POST'])
def events():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        event_name = request.form['event_name']
        category = request.form['category']
        description = request.form['description']
        event_date = request.form['event_date']
        event_time = request.form['event_time']
        location = request.form['location']
        max_attendees = request.form['max_attendees']

        # Insert event into event_info, no current_attendees column now
        cursor.execute(
            'INSERT INTO event_info (event_name, category, description, date, time, location, max_attendees) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (event_name, category, description, event_date, event_time, location, max_attendees)
        )
        db.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('event_info.events'))

    # Filtering logic
    location_filter = request.args.get('location', '').strip()
    if location_filter:
        query = '''
            SELECT e.event_id, e.event_name, e.category, e.description, e.date, e.time, e.location,
                   e.max_attendees,
                   COUNT(a.attendee_id) AS attendee_count
            FROM event_info e
            LEFT JOIN attendee_info a ON e.event_id = a.event_id
            WHERE e.location LIKE %s
            GROUP BY e.event_id
        '''
        cursor.execute(query, (f'%{location_filter}%',))
    else:
        query = '''
            SELECT e.event_id, e.event_name, e.category, e.description, e.date, e.time, e.location,
                   e.max_attendees,
                   COUNT(a.attendee_id) AS attendee_count
            FROM event_info e
            LEFT JOIN attendee_info a ON e.event_id = a.event_id
            GROUP BY e.event_id
        '''
        cursor.execute(query)

    all_events = cursor.fetchall()
    return render_template('events.html', all_events=all_events)

@event_info.route('/update_event/<int:event_id>', methods=['GET', 'POST'])
def update_event(event_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        event_name = request.form['event_name']
        category = request.form['category']
        description = request.form['description']
        event_date = request.form['event_date']
        event_time = request.form['event_time']
        location = request.form['location']
        max_attendees = request.form['max_attendees']

        cursor.execute(
            'UPDATE event_info SET event_name = %s, category = %s, description = %s, date = %s, time = %s, location = %s, max_attendees = %s '
            'WHERE event_id = %s',
            (event_name, category, description, event_date, event_time, location, max_attendees, event_id)
        )
        db.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('event_info.events'))

    # Fetch the event's current data
    cursor.execute('SELECT * FROM event_info WHERE event_id = %s', (event_id,))
    current_event_info = cursor.fetchone()
    return render_template('events_update.html', current_event_info=current_event_info)

@event_info.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM event_info WHERE event_id = %s', (event_id,))
    db.commit()
    flash('Event deleted successfully!', 'danger')
    return redirect(url_for('event_info.events'))

@event_info.route('/visualization')
def visualization():
    connection = get_db()
    with connection.cursor() as cursor:
        # We now count attendees via a join, rather than using a separate column.
        query = '''
            SELECT e.event_name, COUNT(a.attendee_id) AS attendee_count
            FROM event_info e
            LEFT JOIN attendee_info a ON e.event_id = a.event_id
            GROUP BY e.event_name
        '''
        cursor.execute(query)
        event_data = cursor.fetchall()

    # Convert to DataFrame
    df = pd.DataFrame(event_data, columns=['event_name', 'attendee_count'])

    # Create a chart using attendee_count
    # Let's say we stick with a pie chart, but you can switch to line or any other chart type:
    fig = px.pie(
        df,
        names='event_name',
        values='attendee_count',
        title="Attendees per Event"
    )

    graph_html = fig.to_html(full_html=False)
    return render_template('visualization.html', graph_html=graph_html)
