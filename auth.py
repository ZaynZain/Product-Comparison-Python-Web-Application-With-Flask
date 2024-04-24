from connection import get_database_connection
from flask import session

def insert_user_to_database(name, email, password):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, email, password))
        connection.commit()

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"An error occurred while inserting data: {str(e)}")

def validate_login(email, password):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            # Create a session for the user
            session['email'] = email

        return user

    except Exception as e:
        print(f"An error occurred while validating login: {str(e)}")
        return None