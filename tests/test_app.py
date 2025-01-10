import unittest
import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_add_url(self):
        response = self.app.post('/add_url', json={"url": "https://example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"URL added successfully!", response.data)

if __name__ == '__main__':
    unittest.main()