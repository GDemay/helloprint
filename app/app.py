import requests
from flask import Flask
from flask_crontab import Crontab
from app.routes import routes_blueprint
from app.database import db
from app.config import BaseConfig, BasicConfig, TestConfig
import os
from statistics import median

from app.models import SKUModel


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "any secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = BaseConfig.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(routes_blueprint)
    crontab.init_app(app)
    return app


def create_app_test():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "any secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = TestConfig.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(routes_blueprint)
    return app


def setup_database(app):
    with app.app_context():
        db.create_all()
        app.logger.info("DB init!")

crontab = Crontab()

if __name__ == "__main__":
    app = create_app()
    if not os.path.isfile(BaseConfig.SQLALCHEMY_DATABASE_URI):
        setup_database(app)
    app.run()



@crontab.job(minute="*/1", day_of_week="1-5")
def scheduled_highest_price():
  try:
      if sku:= SKUModel.query.order_by(SKUModel.price.desc()).first():
        print(sku.to_json())
      else:
        print("No SKU found!")
  except Exception as e:
      print("Error while getting SKU", e)


# add crontab job to run */3 8-10 * * *
@crontab.job(minute="*/3", hour="8-10")
def scheduled_lowest_price():
  try:
      if sku:= SKUModel.query.order_by(SKUModel.price.asc()).first():
        print(sku.to_json())
      else:
        print("No SKU found!")
  except Exception as e:
      print("Error while getting SKU", e)
  
# add crontab job to run */5 11-12 * * 1,3,5
@crontab.job( minute="*/5", hour="11-12", day_of_week="1,3,5")
def scheduled_median_price():
  try:
      skus = SKUModel.query.all()
      prices = [sku.price for sku in skus]
      print({"median": median(prices)})
  except Exception as e:
      print("Error while getting SKU", e)