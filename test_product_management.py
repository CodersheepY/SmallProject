import  unittest  
import  json
from product_management import app, products_data

class TestProductManagement(unittest.TestCase):
    # Set up the test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
   
    global products_data
    products_data.clear()
    products_data['product_id'] ={
        'sales':0,
        'stock':100, # initial stock
        'name':'Sample Product',
        'price':100,
        'description':'This is a sample product'
    }
    # print("Initialized products_data:", products_data)

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
        #print("Response data (initial):",response.get_data(as_text=True))
        data = json.loads(response.get_data(as_text=True))
        initial_stock = data['stock']
        self.assertIsNotNone(initial_stock, "Stock should not be None")

        # Sell 10 products then Update sales
        response = self.app.post('/product/product_id/sell', 
                                 data=json.dumps({'sold_quantity': 10}),
                                 content_type='application/json')
        #print("Response data (after update):", response.get_data(as_text=True))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['product']['sales'], 10)
        self.assertEqual(data['product']['stock'], initial_stock - 10)
   
    # Test update_stock
    def test_update_stock(self):
        # Get initial stock
        response = self.app.get('/product/product_id')
        #print("Response data (initial):", response.get_data(as_text=True))
        data = json.loads(response.get_data(as_text=True))
        initial_stock = data['stock']
        self.assertIsNotNone(initial_stock, "Stock should not be None")

        # Restock 50 products then Update stock
        response = self.app.post('/product/product_id/restock',
                                 data=json.dumps({'restock_quantity': 50}),
                                 content_type='application/json')
        print("Response data (after update):", response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['product']['stock'], initial_stock + 50)
    
    # Test sell more than stock
    def test_sell_more_than_stock(self):
        # Sell more than available stock 
        response = self.app.post('/product/product_id/sell',
                                 data=json.dumps({'sold_quantity': 200}),
                                 content_type='application/json')
        #print("Response data for test_sell_more_than_stock:", response.get_data(as_text=True))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Not enough stock available')
    
    # Test nonexistent product
    def test_nonexitent_product(self):
        # Test nonexistent product
        response = self.app.get('/product/nonexistent_product')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Product not found')
    
    # Test get_product_summary
    def test_get_products_summary(self):
        # Get initial summary
        response = self.app.get('/product/summary')
        data = json.loads(response.get_data(as_text=True))
        # Calculate expected total sales and stock 
        expected_total_sales = sum([product['sales'] for product in products_data.values()])
        expected_total_stock = sum([product['stock'] for product in products_data.values()])
        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_sales'], expected_total_sales)
        self.assertEqual(data['total_stock'], expected_total_stock)

    # # Test delete product
    # def test_delete_product(self):
    #     # Examine the products_data before deleting a product
    #     response = self.app.get('/product/product_id')
    #     self.assertEqual(response.status_code, 200)
    #     # Delete the product
    #     response = self.app.delete('/product/product_id/delete')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("Product deleted successfully", response.get_data(as_text=True))
    #     # Check if the product is deleted
    #     response = self.app.get('/product/product_id')
    #     self.assertEqual(response.status_code, 404)

    def test_update_product_info(self):
        # global products_data
        # products_data['update_test_product_id'] = {
        # 'sales': 0,
        # 'stock': 100,
        # 'name': 'Old Name',
        # 'price': 100,
        # 'description': 'Old Description'
    # }
        
        products_data['product_id']['name'] = "Old Name"
        products_data['product_id']['price'] = 100
        products_data['product_id']['description'] = "Old Description"

        response = self.app.put('/product/product_id/update',
                                data=json.dumps({
                                    'name': 'New Name',
                                    'price': 200,
                                    'description': 'New Description'
                                }),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['product']['name'], 'New Name')
        self.assertEqual(data['product']['price'], 200)
        self.assertEqual(data['product']['description'], 'New Description')
                               
if __name__ == '__main__':
    unittest.main()