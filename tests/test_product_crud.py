import unittest
from unittest.mock import patch
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

from app import app


class TestProductCRUD(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        self.client = app.test_client()
        self.db = TinyDB(storage=MemoryStorage)

        self.patcher = patch("app.products.views.products_table", self.db)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.db.close()

    def add_product(self):
        self.db.insert({
            "id": 1,
            "name": "Laptop",
            "content": "Тестовий ноутбук",
            "price": 1000.0,
            "category": "electronics",
            "quantity": 5,
            "image": "",
            "created_at": "2026-01-01"
        })

    def test_create(self):
        response = self.client.post("/products/add", data={
            "name": "Monitor",
            "content": "Тестовий монітор",
            "price": "250.50",
            "category": "electronics",
            "quantity": "5"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.db.all()), 1)
        self.assertEqual(self.db.all()[0]["name"], "Monitor")

    def test_read(self):
        self.add_product()

        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)

        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        self.add_product()

        response = self.client.post("/products/1/edit", data={
            "name": "Updated Laptop",
            "content": "Оновлений опис ноутбука",
            "price": "1200.00",
            "category": "electronics",
            "quantity": "10"
        })

        self.assertEqual(response.status_code, 302)

        product = self.db.get(Query().id == 1)
        self.assertEqual(product["name"], "Updated Laptop")
        self.assertEqual(product["quantity"], 10)

    def test_delete(self):
        self.add_product()

        response = self.client.post("/products/1/delete")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.db.all()), 0)

    def test_not_found(self):
        response = self.client.get("/products/99999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
