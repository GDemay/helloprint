import logging

import pytest
from base import BaseTestCase
from flask import Flask
from flask import Response

from app.core import (create, delete, get, get_5_highest, get_all, get_highest,
                      get_lowest, get_median, update_21, update_dataset)
from app.models import SKUModel
from tests.context import MyTest

LOGGER = logging.getLogger(__name__)


class FlaskTestCase(BaseTestCase):
    def __init__(self, *args, **kwargs):
        self.id = 0
        super(FlaskTestCase, self).__init__(*args, **kwargs)

    def test_create(self):
        """Test create"""
        sku = SKUModel(sku="This is a sku",
                       product_title="test", quantity=1, price=1.0)
        sku = create(sku)

        assert sku is not None
        # Get in db and check
        sku_db = get(sku.id)
        # assert sku_db none
        assert sku_db is not None

        # check if the id is the same
        assert sku_db.id == sku.id
        LOGGER.critical("sku_db.id: %s", sku_db.id)

    def test_get(self):
        sku = get(1)

        # check if sku = "Test" and quanity = 42
        assert sku is not None
        assert sku.sku == "SKU0"
        assert sku.quantity == 10

    def test_bad_get(self):
        sku = get(9999999)
        assert sku is None

    def test_get_all(self):
        sku = get_all()
        assert sku is not None

    def test_get_best(self):
        sku = get_5_highest()

        assert sku is not None
        assert len(sku) == 5
        assert sku[0].price == 10.0
        assert sku[0].sku == "SKU0"
        assert sku[0].quantity == 10
        assert sku[2] == sku[2]
        assert sku[4].price == 14.0
        assert sku[4].sku == "SKU4"
        assert sku[4].quantity == 14

    def test_update(self):
        # Get the lowest sku
        sku = get_lowest()
        assert sku.price == 10.0

        sku = update_21(1)
        assert sku is not None
        assert sku.price == 12.1

    def test_update_bad(self):
        sku = update_21(9999999)
        assert sku is None

    def test_delete(self):
        # Trying to get sku with id 1
        sku = get(1)
        assert sku is not None

        # Deleting it
        response_delete = delete(1)
        # Get http response
        assert response_delete.status_code == 200

    def test_get_lowest(self):
        sku = get_lowest()

        assert sku is not None
        LOGGER.error("sku price: %s", sku.price)
        assert sku.price == 10.0

    def test_get_highest(self):
        sku = get_highest()
        assert sku is not None
        assert sku.price == 19.0

    def test_get_median(self):
        median = get_median()

        assert median is not None
        assert 14.5 == median

    def test_update_dataset(self):
        check_update = update_dataset()
        assert check_update == ("OK", 200)
