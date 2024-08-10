import  unittest  
import  json
from product_management import app, products_data

class TestProductManagement(unittest.TestCase):
    # Set up the test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    # Test get_product_info
    def test_get_product_info(self):
        response = self.app.get('/product/product_id')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIn('sales', data)
        self.assertIn('stock', data)
        self.assertEqual(data['sales'], 0)
        self.assertEqual(data['stock'], 100)

    # Test update_sales
    def test_update_sales(self):
        # Get initial sales
        response = self.app.get('/product/product_id')
        data = json.loads(response.get_data(as_text=True))
        initial_stock = data['stock']

        # Sell 10 products then Update sales
        response = self.app.post('/product/product_id/sell', 
                                 data=json.dumps({'sold_quantity': 10}),
                                 content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['product']['sales'], 10)
        self.assertEqual(data['product']['stock'], initial_stock - 10)

    def test_update_stock(self):
        # Get initial stock
        response = self.app.get('/product/product_id')
        data = json.loads(response.get_data(as_text=True))
        initial_stock = data['stock']

        # Restock 50 products then Update stock
        response = self.app.post('/product/product_id/restock',
                                 data=json.dumps({'restock_quantity': 50}),
                                 content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['product']['stock'], initial_stock + 50)

    def test_sell_more_than_stock(self):
        # Sell more than available stock 
        response = self.app.post('/product/product_id/sell',
                                 data=json.dumps({'sold_quantity': 200}),
                                 content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Not enough stock available')

    def test_nonexitent_product(self):
        # Test nonexistent product
        response = self.app.get('/product/nonexistent_product')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Product not found')

if __name__ == '__main__':
    unittest.main()