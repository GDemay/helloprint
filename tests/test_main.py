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
        sku_response = create(sku)

        assert sku_response.status_code == 200
        # Get in db and check
        response_get = get(sku.id)
        # assert sku_db none
        assert response_get.status_code == 200

        # check if the id is the same
        assert response_get.json["id"] == sku.id

    def test_get(self):
        response_get = get(1)

        # check if sku = "Test" and quanity = 42
        assert response_get.status_code == 200
        assert response_get.json["sku"] == "SKU0"
        assert response_get.json["quantity"] == 10

    def test_bad_get(self):
        response_get = get(9999999)
        assert response_get.status_code == 404

    def test_get_all(self):
        sku = get_all()
        assert sku is not None

    def test_get_best(self):
        sku = get_5_highest()

        assert sku.status_code == 200
        assert len(sku.json) == 5
        assert sku.json[0]["price"] == 10.0
        assert sku.json[0]["sku"] == "SKU0"
        assert sku.json[1]["price"] == 11.0
        assert sku.json[1]["sku"] == "SKU1"
        assert sku.json[2]["price"] == 12.0
        assert sku.json[2]["sku"] == "SKU2"
        assert sku.json[3]["price"] == 13.0
        assert sku.json[3]["sku"] == "SKU3"
        assert sku.json[4]["price"] == 14.0
        assert sku.json[4]["sku"] == "SKU4"

    def test_update(self):

        response_update = update_21(1)

        assert response_update.status_code == 200
        assert response_update.json["price"] == 12.1

    def test_update_bad(self):
        response_update = update_21(9999999)
        assert response_update.status_code == 404

    def test_delete(self):
        # Trying to get sku with id 1
        response_get = get(1)
        assert response_get.status_code == 200

        # Deleting it
        response_delete = delete(1)
        # Get http response
        assert response_delete.status_code == 200

    def test_get_lowest(self):
        response_get_lowest = get_lowest()

        assert response_get_lowest.status_code == 200
        assert response_get_lowest.json["price"] == 10.0

    def test_get_highest(self):
        response_get_highest = get_highest()
        assert response_get_highest.status_code == 200
        assert response_get_highest.json["price"] == 19.0

    def test_update_dataset(self):
        check_update = update_dataset()
        assert check_update.status_code == 200
