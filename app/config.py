import os




class BaseConfig(object):
    DEBUG = False
    # shortened for readability
    SECRET_KEY = "\xbf\xb0\x11\xb1\xcd\xf9\xba\x8bp\x0c..."
    SQLALCHEMY_PATH = "/tmp/thisisatest.db"
    # SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/sku.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLALCHEMY_PATH}"



class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class BasicConfig(BaseConfig):
    DATASET_PATH = "app/data/dataset.json"
