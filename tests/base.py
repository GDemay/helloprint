from flask_testing import TestCase

from app.models import SKUModel, db
from app.app import create_app
from app.config import BasicConfig


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        return create_app()

    def setUp(self):
        db.create_all()
        for i in range(10):
            sku = SKUModel(sku=f"SKU{str(i)}", price=(
                10 + i), quantity=10 + i, product_title="Test")

            db.session.add(sku)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
