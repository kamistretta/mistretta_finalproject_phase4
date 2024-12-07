from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db_connect import get_db

# Create the events blueprint
event_info = Blueprint('event_info', __name__)

# Route for displaying all events (used in 'events.html')
@event_info.route('/events', methods=['GET', 'POST'])
def events():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new event
    if request.method == 'POST':
        event_name = request.form['event_name']
        category = request.form['category']
        description = request.form['description']
        event_date = request.form['event_date']
        event_time = request.form['event_time']
        location = request.form['location']
        max_attendees = request.form['max_attendees']
        current_attendees = 0  # Initialize current_attendees as 0

        # Insert event into the event_info table
        cursor.execute(
            'INSERT INTO event_info (event_name, category, description, date, time, location, max_attendees, current_attendees) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (event_name, category, description, event_date, event_time, location, max_attendees, current_attendees)
        )
        db.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('event_info.events'))

    # Filtering logic
    location_filter = request.args.get('location', '').strip()
    if location_filter:
        query = '''
            SELECT e.event_id, e.event_name, e.category, e.description, e.date, e.time, e.location, 
                   e.max_attendees, e.current_attendees, 
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
                   e.max_attendees, e.current_attendees, 
                   COUNT(a.attendee_id) AS attendee_count
            FROM event_info e
            LEFT JOIN attendee_info a ON e.event_id = a.event_id
            GROUP BY e.event_id
        '''
        cursor.execute(query)

    # Fetch all events with attendee count
    all_events = cursor.fetchall()
    return render_template('events.html', all_events=all_events)

# Route for updating an event (used in 'events_update.html')
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

        # Update event details
        cursor.execute(
            'UPDATE event_info SET event_name = %s, category = %s, description = %s, date = %s, time = %s, location = %s, max_attendees = %s WHERE event_id = %s',
            (event_name, category, description, event_date, event_time, location, max_attendees, event_id)
        )
        db.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('event_info.events'))

    # Fetch the event's current data for pre-populating the update form
    cursor.execute('SELECT * FROM event_info WHERE event_id = %s', (event_id,))
    current_event_info = cursor.fetchone()
    return render_template('events_update.html', current_event_info=current_event_info)

# Route for deleting an event
@event_info.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the event
    cursor.execute('DELETE FROM event_info WHERE event_id = %s', (event_id,))
    db.commit()
    flash('Event deleted successfully!', 'danger')
    return redirect(url_for('event_info.events'))