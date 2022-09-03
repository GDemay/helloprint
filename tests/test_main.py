import pytest
import unittest
from flask import Flask

from app.app import create_app_test
from tests.context import MyTest
from app.models import SKUModel
from app.core import get, create
from base import BaseTestCase


import logging

LOGGER = logging.getLogger(__name__)
class FlaskTestCase(BaseTestCase):

    def test_create(self):
        sku = create("CECI EST MON TEST", 42, 3)
        assert sku.sku == "CECI EST MON TEST"
        assert sku.quantity == 42
        # Get in db and check
        sku_db = get(sku.id)
        # assert sku_db none 
        assert sku_db is not None

        assert sku_db.id == sku.id
         

    """ 
      def test_get_bad_id(self):
          sku = get(99999)
          self.assertEqual(sku, None)

      def test_get_good_id(self):
          sku = get(1)
          self.assertEqual(sku.sku, "WWWWWWWWWWW IS FOR TEST")
    """
