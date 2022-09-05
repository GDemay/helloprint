import json
from itertools import product
from statistics import median

import requests
from flask import Blueprint, request

from app.core import (create, delete, get, get_5_highest, get_all, get_lowest,
                      update_21, update_dataset)
from app.models import SKUModel, db

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
    return get(id)

# Get all SKUs


@routes_blueprint.route("/sku")
def get_all_sku():
    return get_all()


@routes_blueprint.route("/sku/update", methods=["GET"])
def update_from_dataset():
    return update_dataset()


# Get the 5 best prices for a SKU
@routes_blueprint.route("/sku/highest", methods=["GET"])
def get_best_sku():
    return get_5_highest()


# Update a SKU from an ID by increasing it's price by 21%
@routes_blueprint.route("/sku/<int:id>", methods=["PUT"])
def update_sku(id):
    return update_21(id)


# Create SKU from form data
@routes_blueprint.route("/sku", methods=["POST"])
def create_sku():
    sku = SKUModel(
        sku=request.form["sku"],
        product_title=request.form["product_title"],
        quantity=request.form["quantity"],
        price=request.form["price"],
    )
    return create(sku).to_json()


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
