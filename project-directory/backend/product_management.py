from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Set SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create a Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    sales = db.Column(db.Integer, nullable=False, default=0)

# Create the database
with app.app_context():
    db.create_all()

# Dummy data for products
products_data ={
    'product_id':{
        'sales':0,
        'stock':100, # initial stock
        'name':'Sample Product',
        'price':100,
        'description':'This is a sample product'
    }
}

# # API
# API_URL = " "
# API_KEY = "API_KEY"

# Get product info
@app.route('/product/<product_id>', methods=['GET']) 
def get_product_info(product_id):
    product = products_data.get(product_id)
    if product is None:
        return jsonify({'error':'Product not found'}), 404
    return jsonify(product) 

# Update sales
@app.route('/product/<string:product_id>/sell', methods=['POST'])
def update_sales(product_id):
    product = products_data.get(product_id)
    # Check if product exists
    if product is None:
        return jsonify({'error':'Product not found'}), 404
    
    # Get sold quantity
    data =request.get_json()
    sold_quantity = data.get('sold_quantity',0)

    # Check stock
    if product['stock'] < sold_quantity:
        return jsonify({'error':'Not enough stock available'}), 400
    
    # Update sales and stock
    product['stock'] -= sold_quantity
    product['sales'] += sold_quantity
    return jsonify({"message":"Sales updated successfully","product":product})

# Update stock
@app.route('/product/<string:product_id>/restock', methods=['POST'])
def update_stock(product_id):
    product = products_data.get(product_id)
    # Check if product exists
    if product is None:
        return jsonify({'error':'Product not found'}), 404
    
    # Get restock quantity
    data =request.get_json()
    restock_quantity = data.get('restock_quantity',0)

    # Update stock
    product['stock'] += restock_quantity
    return jsonify({"message":"Stock updated successfully","product":product})

# Get product summary (total sales and total stock) 
@app.route('/product/summary', methods=['GET'])
def get_product_summary():
    total_sales = 0
    total_stock = 0
    
    # Calculate total sales and total stock
    for product in products_data.values():
        total_sales += product.get('sales',0)
        total_stock += product.get('stock',0)
    
    return jsonify({'total_sales':total_sales, 'total_stock':total_stock}), 200

# # Delete product 
# @app.route('/product/<string:product_id>/delete', methods=['DELETE'])
# def delete_product(product_id):
#     if product_id in products_data:
#         del products_data[product_id]
#         return jsonify({'message':'Product deleted successfully'}), 200
#     else:
#         return jsonify({'error':'Product not found'}), 404

# Update product info
@app.route('/product/<string:product_id>/update', methods=['PUT'])
def update_product(product_id):
    global products_data
    product = products_data.get(product_id)
    if product is None:
        return jsonify({'error':'Product not found'}), 404
    
    data = request.get_json()
    data = request.get_json()
    product['name'] = data.get('name', product['name'])
    product['price'] = data.get('price', product['price'])
    product['description'] = data.get('description', product['description'])

    return jsonify({'message':'Product updated successfully','product':product})

# Get product info (from API)
def get_apps():
    query_params = {
        'applicationId': API_KEY,
        'format':'json',
        'keyword':'???'
    }
    response = requests.get(API_URL, params=query_params)

    if response.status_code == 200:
        return jspnify(response.json())
    else:
        return jsonify({'error':'Failed to fetch data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
