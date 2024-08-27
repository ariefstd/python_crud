from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder='views')  # Specify the template folder

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )

# READ: Display all users
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    connection.close()
    return render_template('index.html', users=users)

# CREATE: Add a new user
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        connection.commit()
        connection.close()
        
        return redirect(url_for('index'))
    
    return render_template('add.html')

# UPDATE: Edit a user
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, id))
        connection.commit()
        connection.close()
        
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    connection.close()
    
    return render_template('edit.html', user=user)

# DELETE: Delete a user
@app.route('/delete/<int:id>')
def delete_user(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    connection.commit()
    connection.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
