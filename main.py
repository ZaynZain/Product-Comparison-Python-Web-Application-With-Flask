from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from FetchData import fetch_data_from_table
from CategoryHandler import get_categories
from csv_operations import read_csv_file_and_insert_to_database
from SearchProduct import search_item
from connection import get_database_connection
from comparison_fatch_data import get_product_comparison, get_compare_product_data
from auth import insert_user_to_database, validate_login
from UserProfile import fetch_user_info_from_database
from admin_functions import upload_file_to_database, get_table_names, delete_table
from flask_paginate import Pagination
import pandas as pd
import csv
import mysql.connector

app = Flask(__name__)
app.secret_key = "hello_zain"


# This route is commented because we want to run multiple functions on same route.
# @app.route('/admin')
# def admin_panel():
#     return render_template('admin.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Check if the user is authenticated
    if 'email' in session:
        if request.method == 'POST':
            # Check if it's an upload request
            if 'file' in request.files:
                file = request.files['file']

                if file.filename == '':
                    return "No selected file"

                # Use the function from admin_functions
                result = upload_file_to_database(file)
                return result

            # Check if it's a delete request
            selected_table = request.form.get('deleteFile')
            if selected_table:
                delete_table(selected_table)
                return redirect(url_for('admin'))

        # On GET request, render the admin panel with table names
        table_names = get_table_names()
        return render_template('admin.html', table_names=table_names)

    # If the user is not authenticated, redirect to the login page
    return redirect(url_for('login'))


# Add your login route and other routes as needed

@app.route('/')
def index():
    categories = get_categories()
    return render_template('index.html', categories=categories)


# Create a route to search the data
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_term = request.form.get("search_term")
        results = search_item(search_term)

        return render_template("searchresults.html", results=results, search_term=search_term)


@app.route('/instant_search', methods=['GET'])
def instant_search():
    query = request.args.get('query')
    if not query:
        return jsonify([])  # Return an empty response if query is None or empty

    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM laptops WHERE productname LIKE %s", ('%' + query + '%',))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("instant_search.html", results=results)


# Create a route for product comparison
@app.route('/product_comparison/<int:product_id>/<string:product_name>', methods=['GET', 'POST'])
def product_comparison(product_id, product_name):
    # Fetch the main product data
    product = get_product_comparison(product_id, product_name)
    print('the selected product data is ', product)

    compare_product_data = None  # Initialize additional_product_info variable

    if request.method == 'POST':
        # Get additional data from the form
        compare_product = request.form.get('compare_product')

        # Fetch more data from the database based on the additional data
        compare_product_data = get_compare_product_data(compare_product)
        print('the comparison data', compare_product_data)

    # Render the template with both products if additional product info is available
    # or with only the main product if additional product info is not available or no POST request
    return render_template('productcomparison.html', product=product, compare_product_data=compare_product_data)


@app.route('/registration', methods=['GET', 'POST'])
# Create a route for user registration
def registration():
    if request.method == 'POST':
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['pass']
            confirm_password = request.form['re_pass']

            # Perform password match validation
            if password != confirm_password:
                return "Passwords do not match. Please try again."

            # Insert user data into the database

            # Insert user data into the database using the imported function
            insert_user_to_database(name, email, password)

            # Redirect to a success page or any other page after registration
            return redirect(url_for('index'))

    # Render the registration form template for GET requests
    return render_template('Registration.html')


# Create a route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['your_pass']

        # Check if the login is for the admin
        if email == 'admin@zain.com' and password == 'adminzain':
            session['email'] = email
            return redirect(url_for('admin'))

        # Validate user login
        user = validate_login(email, password)

        if user:
            # Create a session for the user
            session['email'] = email
            # Redirect to a logged-in page or perform further actions
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')


# Create a route for logout
@app.route('/logout')
def logout():
    # Clear the session and redirect to the index page
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/laptops')
def display_data():
    try:
        daraz_table = 'darazlaptops'
        amazon_table = 'laptops'
        aliexpress_table = 'aliexpresslaptops'

        page = request.args.get('page', 1, type=int)
        per_page = 5  # Number of items per page

        daraz_laptops, total_count = fetch_data_from_table(daraz_table, page, per_page)
        # print( 'the data of the daraz_table_data:',  daraz_table_result)
        amazon_laptops, _ = fetch_data_from_table(amazon_table, page, per_page)
        aliexpress_laptops, _ = fetch_data_from_table(aliexpress_table, page, per_page)
        # print(' the data of the laptop table',result3)
        total_pages = total_count // per_page

        return render_template('laptops.html', daraz_laptops=daraz_laptops, amazon_laptops=amazon_laptops,
                               aliexpress_laptops=aliexpress_laptops, total_pages=total_pages, total_count=total_count,
                               page=page, per_page=per_page)
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route('/filter')
def filter():
    f = request.args.get('f')
    if f:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM laptops WHERE productname LIKE %s LIMIT 10", ('%' + f + '%',))
        filters = cursor.fetchall()
        print(filters)
        return render_template('filter.html', filters=filters)
    else:
        return jsonify(message="No filter provided")


@app.route('/chairs')
def chairs():
    table_name = 'chair'
    try:
        result = fetch_data_from_table(table_name)
        return render_template('chairs.html', data=result)
    except Exception as e:
        return f"An error occurred:{str(e)}"


@app.route('/mobiles')
def mobiles():
    try:
        mobiles_table = 'newAmazon'
        page = request.args.get('page', 1, type=int)
        per_page = 5  # Number of items per page

        daraz_table_result, total_count = fetch_data_from_table(mobiles_table, page, per_page)
        # result2, _ = fetch_data_from_table(mobiles_table, page, per_page)
        total_pages = total_count // per_page

        return render_template('mobiles.html', data=daraz_table_result, total_pages=total_pages,
                               total_count=total_count, page=page, per_page=per_page)
    except Exception as e:
        return "An error occurred: {str(e)}"


@app.route('/item_show')
def item_show():
    product_id = request.args.get('product_id')
    product_name = request.args.get('product_name')
    product_show = request.args.get('product_show')
    product_price = request.args.get('product_price')
    product_photo = request.args.get('product_photo')

    # You can use these variables to render the second page
    return render_template('item_show.html', product_id=product_id, product_name=product_name,
                           product_show=product_show, product_price=product_price, product_photo=product_photo)


# Route for the profile page
@app.route('/profile')
def profile():
    # Check if the user is logged in and their basic information is available
    if 'email' in session:
        email = session['email']
        print(" the email is : ", email)
        # Fetch the user's basic information from the database using their email
        # Replace this with your own function to fetch user information
        user_info = fetch_user_info_from_database(email)
        print(user_info)
        # Render the profile page template with the user's basic information
        return render_template('profile.html', user_info=user_info)
    else:
        # If the user is not logged in, redirect them to the login page
        return redirect(url_for('login'))


# After successful login or registration, redirect the user to the profile page
def successful_login_or_registration():
    # Redirect the user to the profile page route
    return redirect(url_for('profile'))


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


if __name__ == '__main__':
    app.run(debug=True)
