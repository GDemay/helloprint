from flask_testing import TestCase

from app.app import create_app_test
from app.models import db


class MyTest(TestCase):

    # I removed some config passing here
    def create_app(self):
        return create_app_test()

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()
