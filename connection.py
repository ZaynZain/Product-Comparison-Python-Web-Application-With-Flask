import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'csvdatastore'
}

# Function to establish a database connection
def get_database_connection():
    return mysql.connector.connect(**db_config)
