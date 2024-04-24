from connection import get_database_connection
import csv
import mysql.connector


file_path="uploads/daraz_laptops.csv"

table_name="/daraz_laptops.csv"
def read_csv_file_and_insert_to_database(connection, file_path, table_name):
    data = read_csv_file(file_path)
    insert_data_to_database(connection, data, table_name)

def read_csv_file(file_path):
    data = []

    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def insert_data_to_database(connection, data, table_name):
    try:
        cursor = connection.cursor()
        for row in data:
            columns = ', '.join([f'`{key}`' for key in row.keys()])
            values = ', '.join(['%s'] * len(row))
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            cursor.execute(insert_query, tuple(row.values()))

        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"An error occurred while inserting data: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()
