from flask import Flask, escape, request
import email_validator
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


# Get one SKU
@app.route("/sku/<int:id>")
def get_sku(id):
    sku = SKUModel.query.get(id)
    if not sku:
        return "Not found", 404
    return sku.to_json()


# Get all SKU from dataset.json
@app.route("/sku")
def get_skus():
    f = open("data/dataset.json", "r")
    data = json.load(f)
    return json.dumps(data[0])


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
