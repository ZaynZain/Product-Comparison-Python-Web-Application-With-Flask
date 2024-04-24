from connection import get_database_connection
import mysql.connector

def search_item(search_term):
    try:
        # Get database connection
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        # Get a list of tables in your database
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        results = []

        for table in tables:
            table_name = list(table.values())[0]

            # Check if the table has a 'productname' column
            cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'productname'")
            productname_column = cursor.fetchone()

            if productname_column:
                query = f"SELECT * FROM {table_name} WHERE productname LIKE %s"
                search_value = f"%{search_term}%"
                cursor.execute(query, (search_value,))
                table_results = cursor.fetchall()
                results.extend(table_results)

        return results

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []

    finally:
        cursor.close()
        connection.close()
