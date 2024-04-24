from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import bcrypt
from flask import Blueprint

registration1 = Blueprint('registration', __name__, static_folder='static', template_folder='templates')

@registration1.route('/register')
def register():
    # Your registration-related code here
    return render_template('Registration.html')

# Additional routes, functions, or logic related to registration


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Establishing connection to the MySQL database
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='register'
    )

    if connection.is_connected():
        print('Connected to MySQL database')

except mysql.connector.Error as e:
    print(f"Error connecting to MySQL database: {e}")

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass'].encode('utf-8')

        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
            connection.commit()
            cursor.close()

            return redirect(url_for('login'))
        except mysql.connector.Error as e:
            print(f"Error inserting data into MySQL table: {e}")

    return render_template('Registration.html')

# Your other routes, configurations, and app logic will go here

if __name__ == '__main__':
    app.run(debug=True)
