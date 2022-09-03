import json
from statistics import median

import requests
from flask import Blueprint, request

from app.database import db
from app.models import SKUModel

routes_blueprint = Blueprint("route_blueprint", __name__)

@routes_blueprint.route("/")
def hello():
    return "Hello World!"


# Retrieve the current timezone using the WorldTimeAPI (http://worldtimeapi.org) for any country available in the service
@routes_blueprint.route("/timezone/<string:area>/<string:region>")
def timezone(area, region):
    url = f"http://worldtimeapi.org/api/timezone/{area}/{region}"
    response = requests.get(url)
    return (
        {"UTF:": response.json()["utc_offset"]}
        if response.ok
        else {"response error": response.text, "http code": response.status_code}
    )


# Get one SKU
@routes_blueprint.route("/sku/<int:id>")
def get_sku(id):
    sku = db.session.query(SKUModel).get(id)
    return sku.to_json() if sku else ("Not found", 404)


# Get all SKUs
@routes_blueprint.route("/sku")
def get_all_sku():
    skus = db.session.query(SKUModel).all()
    return json.dumps([sku.to_json() for sku in skus])


@routes_blueprint.route("/sku/update", methods=["GET"])
def get_skus():
    try:
        f = open("data/dataset.json", "r")

        # Set all SKU to the database

        for sku in json.load(f):
            sku = SKUModel(
                sku=sku["SKU"], quantity=sku["Quantity"], price=sku["Price £"]
            )
            db.session.add(sku)
        db.session.commit()
        return "OK", 200
    except Exception as e:
        return {"error": str(e)}, 500


# Get the 5 best prices for a SKU
@routes_blueprint.route("/sku/best", methods=["GET"])
def get_best_sku():
    skus = db.session.query(SKUModel).order_by(SKUModel.price.asc()).limit(5).all()
    return [sku.to_json() for sku in skus]


# Update a SKU from an ID by increasing it's price by 21%
@routes_blueprint.route("/sku/<int:id>", methods=["PUT"])
def update_sku(id):
    sku = db.session.query(SKUModel).get(id)
    if not sku:
        return {"message": "SKU not found"}, 404
    sku.price = sku.price * 1.21
    db.session.commit()
    return sku.to_json()


# Create SKU from form data
@routes_blueprint.route("/sku", methods=["POST"])
def create_sku():
    # data = request.form["sku"]
    # Create SKU from request form
    sku = SKUModel(
        sku=request.form["sku"],
        quantity=request.form["quantity"],
        price=request.form["price"],
    )
    db.session.add(sku)
    db.session.commit()
    return sku.to_json()


# Delete SKU from ID
@routes_blueprint.route("/sku/<int:id>", methods=["DELETE"])
def delete_sku(id):
    try:
        sku = db.session.query(SKUModel).get(id)
        if not sku:
            return {"message": "SKU not found"}, 404
        db.session.delete(sku)
        db.session.commit()
        return {"message:": "SKU deleted"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


# Return the lowest price for a SKU
@routes_blueprint.route("/sku/lowest")
def get_lowest_sku():
    try:
        if sku := db.session.query(SKUModel).order_by(SKUModel.price.asc()).first():
            return sku.to_json()
        routes_blueprint.logger.error("No SKU found!")
        return [], 404
    except Exception:
        return [], 500


# return median price of all SKU.
@routes_blueprint.route("/sku/median")
def get_median_sku():

    skus = db.session.query(SKUModel).all()
    prices = [sku.price for sku in skus]
    return {"median": median(prices)}
