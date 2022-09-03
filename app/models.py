import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


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
