import os
import sqlite3
import tempfile
import importlib
import unittest

# Ensure the app uses a temporary database path
class MarketplaceTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmpdir.name, 'test.db')
        os.environ['DB_PATH'] = self.db_path
        # reload app module so DB_PATH is read from environment
        global app
        import app as app_module
        importlib.reload(app_module)
        app = app_module
        self.client = app.app.test_client()

    def tearDown(self):
        self.tmpdir.cleanup()
        os.environ.pop('DB_PATH', None)

    def test_get_marketplaces(self):
        res = self.client.get('/marketplaces')
        self.assertEqual(res.status_code, 200)

    def test_post_marketplaces_add(self):
        res = self.client.post('/marketplaces/add', json={'name': 'Mercado'})
        self.assertEqual(res.status_code, 201)
        # verify it's stored in db
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('SELECT name FROM marketplaces')
        rows = cur.fetchall()
        conn.close()
        self.assertEqual(rows, [('Mercado',)])

    def test_local_barcodes_returns_pdf(self):
        res = self.client.get('/local/barcodes?sku=123&name=prod')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, 'application/pdf')


if __name__ == '__main__':
    unittest.main()
