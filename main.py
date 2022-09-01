from flask import Flask, escape, request
import email_validator
import requests

from statistics import median

import json

app = Flask(__name__)

app.config["SECRET_KEY"] = "any secret key"


@app.route("/")
def hello():
    return "Hello World!"


from flask_wtf import FlaskForm

from wtforms import SubmitField, HiddenField, StringField, IntegerField, DecimalField
from wtforms.validators import Email


class SKUClass(FlaskForm):
    id = HiddenField()
    sku = StringField("sky")
    quantity = IntegerField("quantity")
    price = DecimalField("price")


from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/sku.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class SKUModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    def __repr__(self):
        return f"<SKUModel {self.sku} {self.quantity} {self.price}>"

    # JSON serializer
    def to_json(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "quantity": self.quantity,
            "price": self.price,
        }


# Retrieve the current timezone using the WorldTimeAPI (http://worldtimeapi.org) for any country available in the service
@app.route("/timezone/<string:area>/<string:region>")
def timezone( area, region ):
     
    url = "http://worldtimeapi.org/api/timezone/{}/{}".format(area, region)
    response = requests.get(url)
    if not response.ok:
        return  {"response error": response.text, "http code":response.status_code }
    return {"UTF:": response.json()["utc_offset"]}
  
# Get one SKU
@app.route("/sku/<int:id>")
def get_sku(id):
    sku = SKUModel.query.get(id)
    return sku.to_json() if sku else ("Not found", 404)

# Get all SKUs
@app.route("/sku")
def get_all_sku():
    skus = SKUModel.query.all()
    return json.dumps([sku.to_json() for sku in skus])
  
@app.route("/sku/update", methods=["GET"])
def get_skus():
    f = open("data/dataset.json", "r")
    # Set all SKU to the database

    for sku in json.load(f):
      sku = SKUModel( sku=sku["SKU"], quantity=sku["Quantity"], price=sku["Price £"])
      db.session.add(sku)
    db.session.commit()
    return "OK", 200

# Get the 5 best prices for a SKU
@app.route("/sku/best", methods=["GET"])
def get_best_sku():
    skus = SKUModel.query.order_by(SKUModel.price.desc()).limit(5).all()
    return {"skus": [sku.to_json() for sku in skus]}


# Update a SKU from an ID by increasing it's price by 21%
@app.route("/sku/<int:id>", methods=["PUT"])
def update_sku(id):
    sku = SKUModel.query.get(id)
    if not sku:
        return {"message": "SKU not found"}, 404
    sku.price = sku.price * 1.21
    db.session.commit()
    return {"sku": sku.to_json()}


# Create SKU from form data
@app.route("/sku", methods=["POST"])
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
    return {"sku": sku.to_json()}


# Delete SKU from ID
@app.route("/sku/<int:id>", methods=["DELETE"])
def delete_sku(id):
    sku = SKUModel.query.get(id)
    db.session.delete(sku)
    db.session.commit()
    return {"sku": sku.to_json()}

# Print the SKU with the highest price
@app.route("/sku/highest")
def get_highest_sku():
    sku = SKUModel.query.order_by(SKUModel.price.desc()).first()
    return {"sku": sku.to_json()}

# Return the lowest price for a SKU
@app.route("/sku/lowest")
def get_lowest_sku():
    sku = SKUModel.query.order_by(SKUModel.price.asc()).first()
    return {"sku": sku.to_json()}
  
# return median price of all SKU. 
@app.route("/sku/median")
def get_median_sku():
    skus = SKUModel.query.all()
    prices = [sku.price for sku in skus]
    return {"median": median(prices)}

@app.route("/test")
def test():
    scheduled()
    return {"ok": "ok"}
  
@app.cli.command()
def scheduled():
    print(get_highest_sku()["sku"])
    print(get_lowest_sku()["sku"])
    print(get_median_sku()["median"])
