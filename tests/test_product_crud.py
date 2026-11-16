import unittest
from unittest.mock import patch
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

from app import create_app


class TestProductCRUD(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.db = TinyDB(storage=MemoryStorage)

        self.patcher = patch("app.products.views.products_table", self.db)
        self.patcher.start()