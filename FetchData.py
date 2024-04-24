from connection import get_database_connection
import mysql.connector


def fetch_data_from_table(table_name, page=1, per_page=5):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Calculate the offset based on the page number and items per page
        offset = (page - 1) * per_page

        # Fetch total count of records
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_count = cursor.fetchone()[0]

        # Construct the SQL query with pagination
        select_query = f"SELECT * FROM {table_name} LIMIT %s OFFSET %s"

        # Execute the query with parameters
        cursor.execute(select_query, (per_page, offset))

        data = cursor.fetchall()
        print("Fetched data:", data)

    except Exception as e:
        print(f"An error occurred while fetching data: {str(e)}")
        data = []  # Set data to an empty list in case of an exception
        total_count = 0  # Reset total_count to 0 in case of an exception
    finally:
        cursor.close()
        connection.close()

    return data, total_count

