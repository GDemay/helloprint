import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class SKUModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String)
    product_title = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    # JSON serializer
    def to_json(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "product_title": self.product_title,
            "quantity": self.quantity,
            "price": self.price,
        }
