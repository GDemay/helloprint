import json
import logging
from asyncio.log import logger
from statistics import median

from app.config import BasicConfig
from app.models import SKUModel, db

LOGGER = logging.getLogger(__name__)


def get(id):
    try:
        return db.session.query(SKUModel).get(id)
    except Exception as e:
        LOGGER.error("Error while getting SKU", e)
        return None
    return None


def get_all():
    try:
        return db.session.query(SKUModel).all()
    except Exception as e:
        LOGGER.error("Error while getting all SKU", e)
        return None


def update_dataset():
    # Open the dataset file
    with open(BasicConfig.DATASET_PATH, encoding="utf-8") as f:
        try:
            # Set all SKU to the database
            for sku in json.load(f):
                sku = SKUModel(
                    sku=sku["SKU"],
                    product_title=sku["Product Title"],
                    quantity=sku["Quantity"],
                    price=sku["Price £"],
                )
                db.session.add(sku)
            db.session.commit()
            return "OK", 200
        except Exception as e:
            # LOGGER.error("Error while updating dataset", e)
            return {"message": "Error while updating dataset", "error": str(e)}, 500


def get_5_highest():
    try:
        return db.session.query(SKUModel).order_by(SKUModel.price.asc()).limit(5).all()
    except Exception as e:
        LOGGER.error("Error while getting 5 highest SKU", e)
        return None
    return None


def update_21(id):
    try:
        sku = db.session.query(SKUModel).get(id)
        if not sku:
            return None
        sku.price = sku.price * 1.21
        db.session.commit()
    except Exception as e:
        LOGGER.error(e)
        return None
    return sku


def create(sku: SKUModel):
    if not sku:
        return None
    try:
        db.session.add(sku)
        db.session.commit()
    except Exception as e:
        LOGGER.error(e)
        return None
    return sku


def delete(id):
    try:
        sku = db.session.query(SKUModel).get(id)
        if not sku:
            return None
        db.session.delete(sku)
        db.session.commit()
        return None
    except Exception as e:
        LOGGER.error(e)
        return None


def get_lowest():
    try:
        return db.session.query(SKUModel).order_by(SKUModel.price.asc()).first()
    except Exception as e:
        LOGGER.error("Error while getting lowest SKU", e)
        return None


def get_highest():
    try:
        return db.session.query(SKUModel).order_by(SKUModel.price.desc()).first()
    except Exception as e:
        LOGGER.error("Error while getting highest SKU", e)
        return None


def get_median():
    try:
        skus = db.session.query(SKUModel).order_by(SKUModel.price.asc()).all()
        prices = [sku.price for sku in skus]
        return median(prices)

    except Exception as e:
        LOGGER.error("Error while getting median SKU", e)
        return None
