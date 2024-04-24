import pandas as pd
from connection import get_database_connection
import logging
import mysql.connector

def create_table(cursor, table_name, headers):
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(headers)});"
    cursor.execute(create_table_query)

def upload_file_to_database(file):
    try:
        # Extract table name from the filename without extension
        table_name = file.filename.split('.')[0]

        # Read CSV and drop rows with missing values
        df_clean = pd.read_csv(file,encoding='iso-8859-1')
        df_clean.fillna('none', inplace=True)
        # df_clean = df.dropna()


        # Connect to MySQL using the function from db_connection
        connection = get_database_connection()
        cursor = connection.cursor()

        # Extract headers and create a table in MySQL
        headers = list(df_clean.columns)
        create_table(cursor, table_name, [f"{header} VARCHAR(250)" for header in headers])

        # Convert the remaining data to a list of tuples
        data_to_insert = [tuple(row) for row in df_clean.itertuples(index=False, name=None)]

        insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(['%s'] * len(headers))})"
        cursor.executemany(insert_query, data_to_insert)

        # Commit changes and close connection
        connection.commit()
        cursor.close()
        connection.close()

        logging.info(f"File '{file.filename}' uploaded to table '{table_name}' successfully.")
        return "File uploaded successfully to the database"

    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
        return f"File upload failed. MySQL Error: {err}"

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return f"File upload failed. Error: {e}"

def get_table_names():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Retrieve table names
        cursor.execute("SHOW TABLES")
        table_names = [row[0] for row in cursor.fetchall()]

        return table_names

    finally:
        cursor.close()
        connection.close()

def delete_table(table_name):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Drop the selected table
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print("deleted")

        connection.commit()

    finally:
        cursor.close()
        connection.close()
