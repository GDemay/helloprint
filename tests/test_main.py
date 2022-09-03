import pytest
import unittest
from flask import Flask

from app.app import create_app_test
from tests.context import MyTest
from app.models import SKUModel
from app.core import get, get_all, update_dataset, get_5_highest, update_21, create, delete, get_lowest, get_highest, get_median
from base import BaseTestCase


import logging

LOGGER = logging.getLogger(__name__)
class FlaskTestCase(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self.id = 0
        super(FlaskTestCase, self).__init__(*args, **kwargs)

    def test_create(self):
        sku = create("This is a test", 42, 3)
        assert sku is not None
        # Get in db and check
        sku_db = get(sku.id)
        # assert sku_db none 
        assert sku_db is not None

        # check if the id is the same
        assert sku_db.id == sku.id

    
    def test_get(self):
        sku = get(1)
        assert sku is not None

    def test_bad_get(self):
          sku = get(9999999)
          assert sku is None
    
    def test_get_all(self):
        sku = get_all()
        assert sku is not None

    def test_get_best(self):
        sku = get_5_highest()
        assert sku is not None

    def test_update(self):
        sku = update_21(1)
        assert sku is not None

    def test_update_bad(self):
        sku = update_21(9999999)
        assert sku is None

    def test_delete(self):
        pass
        #sku = delete(1)
        #assert sku is not None

    def test_get_lowest(self):
        sku = get_lowest()
        assert sku is not None

    def get_highest(self):
        sku = get_highest()
        assert sku is not None
    
    def get_median(self):
        sku = get_median()
        assert sku is not None
  