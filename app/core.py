import json
import logging
from statistics import median
from flask import abort
from flask import json

from app.config import BasicConfig
from app.models import SKUModel, db
from flask import Response
LOGGER = logging.getLogger(__name__)


def get(id):
    try:
        # return db.session.query(SKUModel).get(id)
        sku = db.session.query(SKUModel).get(id)
        if sku is None:
            return Response("No sku found", status=404, mimetype="application/json")
        return Response(json.dumps(sku.to_json()), status=200, mimetype="application/json")
    except Exception as e:
        LOGGER.error("Error while getting SKU", e)
        return Response(f"Error while getting SKU {e}",  status=500, mimetype="application/json")


def get_all():
    try:
        skus = db.session.query(SKUModel).all()
        if skus is None:
            return Response("No sku found", status=404, mimetype="application/json")
        skus = [sku.to_json() for sku in skus]
        return Response(json.dumps(skus), status=200, mimetype="application/json")
    except Exception as e:
        return Response(f"Error while getting all SKUS {e}",  status=500, mimetype="application/json")


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
            return Response("OK",  status=200, mimetype="application/json")

        except Exception as e:
            # LOGGER.error("Error while updating dataset", e)
            return Response(f"Error while updating SKUS {e}",  status=500, mimetype="application/json")


def get_5_highest():
    try:
        skus = db.session.query(SKUModel).order_by(
            SKUModel.price.asc()).limit(5).all()
        skus = [sku.to_json() for sku in skus]
        return Response(json.dumps(skus), status=200, mimetype="application/json")

    except Exception as e:
        return Response(f"Error while getting 5 SKUS {e}",  status=500, mimetype="application/json")


def update_21(id):
    try:
        sku = db.session.query(SKUModel).get(id)
        if not sku:
            return Response("No sku found", status=404, mimetype="application/json")
        sku.price = sku.price * 1.21
        db.session.commit()
        return Response(json.dumps(sku.to_json()), status=200, mimetype="application/json")
    except Exception as e:
        return Response(f"Error while update SKUS {e}",  status=500, mimetype="application/json")


def create(sku: SKUModel):
    # TODO Check if this SKU already exists
    if not sku:
        return Response("No sku found", status=404, mimetype="application/json")
    try:
        db.session.add(sku)
        db.session.commit()
        return Response(json.dumps(sku.to_json()), status=200, mimetype="application/json")
    except Exception as e:
        LOGGER.error(e)
        return Response(f"Error while create SKUS {e}",  status=500, mimetype="application/json")


def delete(id):
    try:
        sku = db.session.query(SKUModel).get(id)
        if not sku:
            return Response("No sku found", status=404)
        db.session.delete(sku)
        db.session.commit()
        return Response("OK", status=200)
    except Exception as e:
        return Response(f"Error while deleting SKU {e}",  status=500, mimetype="application/json")


def get_lowest():
    try:
        sku = db.session.query(SKUModel).order_by(SKUModel.price.asc()).first()
        if not sku:
            return Response("No sku found", status=404)
        return Response(json.dumps(sku.to_json()), status=200, mimetype="application/json")
    except Exception as e:
        return Response("Error while deleting", status=500)


def get_highest():
    try:
        sku = db.session.query(SKUModel).order_by(
            SKUModel.price.desc()).first()
        if not sku:
            return Response("No sku found", status=404)
        return Response(json.dumps(sku.to_json()), status=200, mimetype="application/json")

    except Exception as e:
        return Response(f"Error while getting SKU {e}",  status=500, mimetype="application/json")


def get_median():
    try:
        skus = db.session.query(SKUModel).order_by(SKUModel.price.asc()).all()
        if not skus:
            return Response("No sku found", status=404)
        prices = [sku.price for sku in skus]
        return Response(median(prices), status=200, mimetype="application/json")

    except Exception as e:
        return Response(f"Error while getting SKU {e}",  status=500, mimetype="application/json")
