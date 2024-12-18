from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import bcrypt  # Import bcrypt for password hashing

user_info = Blueprint('user_info', __name__)

# Route to display and filter users
@user_info.route('/users', methods=['GET', 'POST'])
def users():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new user
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']  # Capture the password input

        # Hash the password before storing it
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert the new user into the database
        cursor.execute('INSERT INTO user_info (username, email, password_hash) VALUES (%s, %s, %s)',
                       (username, email, password_hash))
        db.commit()

        flash('New user added successfully!', 'success')
        return redirect(url_for('user_info.users'))

    # Handle GET request for filtering
    username_filter = request.args.get('username')
    email_filter = request.args.get('email')

    # Construct SQL query for filtering
    query = 'SELECT * FROM user_info WHERE TRUE'
    params = []

    if username_filter:
        query += ' AND username LIKE %s'
        params.append(f'%{username_filter}%')

    if email_filter:
        query += ' AND email LIKE %s'
        params.append(f'%{email_filter}%')

    cursor.execute(query, params)
    all_users = cursor.fetchall()

    return render_template('users.html', all_users=all_users)

# Route to update a user's details
@user_info.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form.get('password')  # Get the new password (optional)

        if password:  # If a new password is provided, hash it
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute('UPDATE user_info SET username = %s, email = %s, password_hash = %s WHERE user_id = %s',
                           (username, email, password_hash, user_id))
        else:  # If no new password, update only other fields
            cursor.execute('UPDATE user_info SET username = %s, email = %s WHERE user_id = %s',
                           (username, email, user_id))
        db.commit()

        flash('User updated successfully!', 'success')
        return redirect(url_for('user_info.users'))

    # GET method: fetch the user's current data for pre-populating the form
    cursor.execute('SELECT * FROM user_info WHERE user_id = %s', (user_id,))
    current_user_data = cursor.fetchone()
    return render_template('users_update.html', current_user_data=current_user_data)

# Route to delete a user
@user_info.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the user
    cursor.execute('DELETE FROM user_info WHERE user_id = %s', (user_id,))
    db.commit()

    flash('User deleted successfully!', 'danger')
    return redirect(url_for('user_info.users'))
