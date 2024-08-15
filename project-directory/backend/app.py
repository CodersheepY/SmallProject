from flask import Flask, request, jsonify
from product_management import db, initialize_db, get_product, get_all_products, update_sales, update_stock, delete_product, update_product_info, get_product_summary

app = Flask(__name__)

# Set SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
initialize_db(app)

@app.route('/')
def index():
    return "Welcome to the Product Management API"

# Get product info
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product_info(product_id):
    product = get_product(product_id)
    if product:
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'sales': product.sales
        }
        return jsonify(product_data)
    else:
        return jsonify({'error': 'Product not found'}), 404

# Get all products
@app.route('/products', methods=['GET'])
def get_all_products_route():
    products = get_all_products()
    product_list = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'sales': product.sales
        } for product in products
    ]
    return jsonify(product_list)

# Update sales
@app.route('/product/<int:product_id>/sell', methods=['POST'])
def update_sales_route(product_id):
    data = request.get_json()
    sold_quantity = data.get('sold_quantity', 0)
    product = update_sales(product_id, sold_quantity)
    
    if product:
        return jsonify({"message": "Sales updated successfully", "product": {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'sales': product.sales
        }})
    else:
        return jsonify({'error': 'Product not found or insufficient stock'}), 404

# Update stock
@app.route('/product/<int:product_id>/restock', methods=['POST'])
def update_stock_route(product_id):
    data = request.get_json()
    restock_quantity = data.get('restock_quantity', 0)
    product = update_stock(product_id, restock_quantity)
    
    if product:
        return jsonify({"message": "Stock updated successfully", "product": {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'sales': product.sales
        }})
    else:
        return jsonify({'error': 'Product not found'}), 404

# Get product summary (total sales and total stock)
@app.route('/product/summary', methods=['GET'])
def get_product_summary_route():
    summary = get_product_summary()
    return jsonify(summary)

# Delete product
@app.route('/product/<int:product_id>/delete', methods=['DELETE'])
def delete_product_route(product_id):
    if delete_product(product_id):
        return jsonify({'message': 'Product deleted successfully'})
    else:
        return jsonify({'error': 'Product not found'}), 404

# Update product info
@app.route('/product/<int:product_id>/update', methods=['PUT'])
def update_product_route(product_id):
    data = request.get_json()
    product = update_product_info(product_id, data)
    
    if product:
        return jsonify({'message': 'Product updated successfully', 'product': {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'sales': product.sales
        }})
    else:
        return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
