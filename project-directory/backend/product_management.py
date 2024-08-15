from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Create a Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    sales = db.Column(db.Integer, nullable=False, default=0)

def initialize_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def get_product(product_id):
    return Product.query.get(product_id)

def get_all_products():
    return Product.query.all()

def update_sales(product_id, sold_quantity):
    product = get_product(product_id)
    if product and product.stock >= sold_quantity:
        product.stock -= sold_quantity
        product.sales += sold_quantity
        db.session.commit()
        return product
    return None

def update_stock(product_id, restock_quantity):
    product = get_product(product_id)
    if product:
        product.stock += restock_quantity
        db.session.commit()
        return product
    return None

def delete_product(product_id):
    product = get_product(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return True
    return False

def update_product_info(product_id, data):
    product = get_product(product_id)
    if product:
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        db.session.commit()
        return product
    return None

def get_product_summary():
    total_sales = db.session.query(db.func.sum(Product.sales)).scalar() or 0
    total_stock = db.session.query(db.func.sum(Product.stock)).scalar() or 0
    return {'total_sales': total_sales, 'total_stock': total_stock}
