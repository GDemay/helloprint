import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class SKUModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String)
    product_title = db.Column(db.String)
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

    # JSON serializer
    def to_json(self):
        return { 
            "id": self.id,
            "sku": self.sku,
            "product_title": self.product_title,
            "quantity": self.quantity,
            "paper_size": self.paper_size,
            "finished_size": self.finished_size,
            "paper_type": self.paper_type,
            "print_type": self.print_type,
            "turnaround": self.turnaround,
            "print_page_number": self.print_page_number,
            "lamination": self.lamination,
            "cover": self.cover,
            "fold_type": self.fold_type,
            "print_orientation": self.print_orientation,
            "product_finishing": self.product_finishing,
            "cut_type": self.cut_type,
            "sets": self.sets,
            "vat_rate": self.vat_rate,
            "price": self.price,
            "spotUV": self.spotUV
        }
