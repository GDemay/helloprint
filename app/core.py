
from asyncio.log import logger
from app.database import db
from app.models import SKUModel
from app.config import BasicConfig
import json
def get(id):
    return db.session.query(SKUModel).get(id)

def get_all():
    return db.session.query(SKUModel).all()

def update_dataset():
  try:
      # Open the dataset file
      # TODO Try exepct if the file is not found
      f = open(BasicConfig.DATASET_PATH, "r")

      # Set all SKU to the database
      for sku in json.load(f):
          sku = SKUModel(
              sku=sku["SKU"], quantity=sku["Quantity"], price=sku["Price £"]
          )
          # TODO try excepct
          db.session.add(sku)
      db.session.commit()
      # TODO Get the number of SKU added
      return "OK", 200
  except Exception as e:
      return {"error": str(e)}, 500

def get_5_highest():
    return db.session.query(SKUModel).order_by(SKUModel.price.asc()).limit(5).all()

def update_21(id):
    sku = db.session.query(SKUModel).get(id)
    if not sku:
        return {"message": "SKU not found"}, 404
    sku.price = sku.price * 1.21
    db.session.commit()
    return sku.to_json()

def create(sku, quantity, price):
    sku = SKUModel(sku=sku, quantity=quantity, price=price)
    if not sku:
        return None
    try:
        db.session.add(sku)
        db.session.commit()
    except Exception as e:
        # TODO LOG
        return None
    return sku

def delete(id):
    try:
        sku = db.session.query(SKUModel).get(id)
        if not sku:
            return {"message": "SKU not found"}, 404
        db.session.delete(sku)
        db.session.commit()
        return {"message:": "SKU deleted"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

def get_lowest():
    return db.session.query(SKUModel).order_by(SKUModel.price.asc()).first()

def get_highest():
    return db.session.query(SKUModel).order_by(SKUModel.price.desc()).first()

def get_median():
    return db.session.query(SKUModel).order_by(SKUModel.price.desc()).first()
  