from connection import get_database_connection
import mysql.connector
# import Levenshtein
import difflib
import re
from mysql.connector import Error  # Import the Error class explicitly


def get_product_comparison(product_id, product_name):
    # Function logic here...

    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch product by ID from the determined table
    sql_query = """
        SELECT * FROM (
            SELECT id,laptops_href, productname, price,discount ,photo_url FROM laptops
            UNION ALL
            SELECT id,laptop_href, productname, price,photo_url,rating FROM darazlaptops

        ) AS all_tables
        WHERE id = %s AND productname = %s;
        """
    cursor.execute(sql_query, (product_id, product_name))
    product = cursor.fetchone()

    cursor.close()

    return product


def get_compare_product_data(compare_product):
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
                    SELECT * FROM laptops,darazlaptops
                    WHERE laptops.productname LIKE %s
                       OR darazlaptops.productname LIKE %s
                """
        cursor.execute(query, ('%' + compare_product + '%',) * 2)

        compare_product_data = cursor.fetchall()  # Fetch all matching rows


        cursor.close()
        connection.close()

        if compare_product_data:
            return compare_product_data[0]  # Return the first matching product
        else:
            return None
    except Error as e:
        print("Error while connecting to MySQL:", e)
        return None

# THE  BELOW METHOD IS USE IT THE PRODUCT NAME IS TITTLE BIT SPILL MISTAKE  
# def levenshtein_distance(s1, s2):
#     if len(s1) < len(s2):
#         return levenshtein_distance(s2, s1)
#
#     if len(s2) == 0:
#         return len(s1)
#
#     previous_row = range(len(s2) + 1)
#
#     for i, c1 in enumerate(s1):
#         current_row = [i + 1]
#
#         for j, c2 in enumerate(s2):
#             insertions = previous_row[j + 1] + 1
#             deletions = current_row[j] + 1
#             substitutions = previous_row[j] + (c1 != c2)
#
#             current_row.append(min(insertions, deletions, substitutions))
#
#         previous_row = current_row
#
#     return previous_row[-1]
#
# def get_closest_match(query, options, cutoff=0.1):
#     closest_match = None
#     min_distance = float('inf')
#
#     for option in options:
#         distance = levenshtein_distance(query, option)
#         if distance < min_distance:
#             min_distance = distance
#             closest_match = option
#
#     if min_distance / max(len(query), len(closest_match)) <= cutoff:
#         return closest_match
#     else:
#         return None
#
# def tokenize(text):
#     return re.findall(r'\w+', text.lower())
#
# def get_compare_product_data(compare_product):
#     try:
#         connection = get_database_connection()
#         cursor = connection.cursor(dictionary=True)
#
#         query = "SELECT * FROM laptops, daraz_laptops"
#         cursor.execute(query)
#
#         products = cursor.fetchall()
#
#         closest_match = get_closest_match(tokenize(compare_product), [tokenize(product['productname']) for product in products], cutoff=0.1)
#
#         cursor.close()
#         connection.close()
#
#         if closest_match:
#             for product in products:
#                 if tokenize(product['productname']) == closest_match:
#                     return product
#         else:
#             return None
#     except Error as e:
#         print("Error while connecting to MySQL:", e)
#         return None