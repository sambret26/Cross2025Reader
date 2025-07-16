from database import db

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(63), nullable=False)
    category = db.Column(db.String(63), nullable=False)
    sex = db.Column(db.String(7), nullable=False)
    order = db.Column(db.Integer)

    def __init__(self, label, category, sex, order):
        self.label = label
        self.category = category
        self.sex = sex
        self.order = order

    def to_json(self):
        return {
            "label": self.label,
            "category": self.category,
            "sex": self.sex,
        }