import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class SKUModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String)
    product_tile = db.Column(db.String)
    quantity = db.Column(db.Integer)
    paper_size = db.Column(db.String)
    finished_size = db.Column(db.String)
    paper_type = db.Column(db.String)
    print_type = db.Column(db.String)
    turnaround = db.Column(db.String)
    print_page_number = db.Column(db.String)
    lamination = db.Column(db.String)
    cover = db.Column(db.String)
    fold_type = db.Column(db.String)
    print_orientation = db.Column(db.String)
    product_finishing = db.Column(db.String)
    cut_type = db.Column(db.String)
    sets = db.Column(db.String)
    vat_rate = db.Column(db.Float)
    price = db.Column(db.Float)
    spotUV = db.Column(db.String)

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
