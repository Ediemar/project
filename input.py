from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Render the form to add a new product
    return render_template('input.html')

@app.route('/submit-product', methods=['POST'])
def add_product():
    # Get form data
    name = request.form['name']
    selection_type = request.form['selectionType']
    quantity = request.form['quantity']
    price = request.form['price']
    description = request.form['description']
    image = request.files['image'].read()  # Read the image file as binary data

    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='erro',  # Replace with your MySQL password
            database='group2'
        )
        cursor = conn.cursor()

        # Insert product into the database
        sql_insert = """
        INSERT INTO product (name, type, quantity, price, description, image) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_insert, (name, selection_type, quantity, price, description, image))
        conn.commit()

        return redirect(url_for('display_products'))  # Redirect to display products page after submission

    except mysql.connector.Error as e:
        return f"Error: {e}"

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/products')
def display_products():
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='erro',  # Replace with your MySQL password
            database='group2'
        )
        cursor = conn.cursor(dictionary=True)

        # Retrieve all products from the database
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

        # Convert image data to base64 for each product
        for product in products:
            if product['image']:
                product['image'] = base64.b64encode(product['image']).decode('utf-8')

        return render_template('display.html', products=products)

    except mysql.connector.Error as e:
        return f"Error: {e}"

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
