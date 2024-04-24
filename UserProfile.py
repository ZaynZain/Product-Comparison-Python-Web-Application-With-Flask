import mysql.connector
from connection import get_database_connection

def fetch_user_info_from_database(email):
    try:
        # Establish a connection to the database

        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        # Define the SQL query to fetch user information based on email
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user_info = cursor.fetchone()
        print("user info is : " , user_info)

        return user_info

    except Exception as e:
        # Handle any exceptions that occur during the database operation
        print(f"An error occurred while fetching user information: {str(e)}")
        return None

    finally:
        # Close the cursor and database connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()