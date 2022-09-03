from flask_testing import TestCase

from app.models import SKUModel
from app.database import db
from app.app import create_app
from app.config import BasicConfig

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app = create_app()
        #app.config.from_object('app.config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        #sku = SKUModel(sku="Test", quantity=42, price=3)
        #db.session.add(sku)
        #db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
