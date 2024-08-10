from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Dummy data for products
products_data ={
    'product_id':{
        'sales':0,
        'stock':100 # initial stock
    }
}

# # Rakuten API
# RAKUTEN_API_URL = "https://app.rakuten.co.jp/services/api/???"
# RAKUTEN_API_KEY = "RAKUTEN_API_KEY"

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

# Get product info (from Rakuten API)
def get_apps():
    query_params = {
        'applicationId': RAKUTEN_API_KEY,
        'format':'json',
        'keyword':'???'
    }
    response = requests.get(RAKUTEN_API_URL, params=query_params)

    if response.status_code == 200:
        return jspnify(response.json())
    else:
        return jsonify({'error':'Failed to fetch data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
