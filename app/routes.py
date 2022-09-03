import json
from statistics import median

import requests
from flask import Blueprint, request

from app.database import db
from app.models import SKUModel
from app.core import get, get_all, update_dataset, get_5_highest, update_21, create, delete, get_lowest
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
    sku = get(id)
    return sku.to_json() if sku else ("Not found", 404)


# Get all SKUs
@routes_blueprint.route("/sku")
def get_all_sku():
    return json.dumps([sku.to_json() for sku in get_all()])


@routes_blueprint.route("/sku/update", methods=["GET"])
def update_from_dataset():
    return update_dataset()


# Get the 5 best prices for a SKU
@routes_blueprint.route("/sku/best", methods=["GET"])
def get_best_sku():
    return json.dumps([sku.to_json() for sku in get_5_highest()])


# Update a SKU from an ID by increasing it's price by 21%
@routes_blueprint.route("/sku/<int:id>", methods=["PUT"])
def update_sku(id):
    return update_21(id)

# Create SKU from form data
@routes_blueprint.route("/sku", methods=["POST"])
def create_sku():
    sku = request.form.get("sku")
    quantity = request.form.get("quantity")
    price = request.form.get("price")
    return create(sku, quantity, price).to_json()


# Delete SKU from ID
@routes_blueprint.route("/sku/<int:id>", methods=["DELETE"])
def delete_sku(id):
    return delete(id)


# Return the lowest price for a SKU
@routes_blueprint.route("/sku/lowest")
def get_lowest_sku():
    return get_lowest().to_json()


# return median price of all SKU.
@routes_blueprint.route("/sku/median")
def get_median_sku():
    return {"median": median([sku.price for sku in get_all()])}
