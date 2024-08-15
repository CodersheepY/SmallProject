import unittest
import json
from app import app, db, Product

class TestProductManagement(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Setup database for testing
        with app.app_context():
            db.drop_all()
            db.create_all()
            product = Product(name="Test Product", description="A product for testing", price=10.0, stock=100)
            db.session.add(product)
            db.session.commit()

    def tearDown(self):
        # Clean up database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_product_info(self):
        response = self.app.get('/product/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], "Test Product")

    def test_update_sales(self):
        response = self.app.post('/product/1/sell', 
                                 data=json.dumps({'sold_quantity': 10}),
                                 content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['product']['sales'], 10)
        self.assertEqual(data['product']['stock'], 90)

    def test_update_stock(self):
        response = self.app.post('/product/1/restock',
                                 data=json.dumps({'restock_quantity': 50}),
                                 content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['product']['stock'], 150)

    def test_sell_more_than_stock(self):
        response = self.app.post('/product/1/sell',
                                 data=json.dumps({'sold_quantity': 200}),
                                 content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Not enough stock available')

    def test_nonexistent_product(self):
        response = self.app.get('/product/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Product not found')

    def test_delete_product(self):
        response = self.app.delete('/product/1/delete')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Product deleted successfully')

    def test_update_product_info(self):
        response = self.app.put('/product/1/update',
                                data=json.dumps({
                                    'name': 'Updated Product',
                                    'price': 200,
                                    'description': 'Updated Description'
                                }),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['product']['name'], 'Updated Product')
        self.assertEqual(data['product']['price'], 200)
        self.assertEqual(data['product']['description'], 'Updated Description')

if __name__ == '__main__':
    unittest.main()
