import os

from flask import Flask
from flask_crontab import Crontab

from app.database import db
from app.routes import routes_blueprint


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "any secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/ssku.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(routes_blueprint)
    return app


def setup_database(app):
    with app.app_context():
        db.create_all()
        app.logger.info("DB init!")


if __name__ == "__main__":
    app = create_app()
    # Because this is just a demonstration we set up the database like this.
    if not os.path.isfile("/tmp/ssku.db"):
        setup_database(app)
    app.run()
""" 

app = Flask(__name__)




app.logger.info("Starting!")
crontab = Crontab(app)


def initialize_db(app):
    try:
        db.create_all()
        app.logger.info("DB init!")
    except Exception as e:
        app.logger.error("DB init failed: %s", e)


initialize_db(app)

# add crontab job to run */3 8-10 * * *
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
"""
