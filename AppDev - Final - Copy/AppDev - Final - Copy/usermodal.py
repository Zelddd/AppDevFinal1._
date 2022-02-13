from app import db

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postalcode = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    paymentmethod = db.Column(db.String(100), nullable=False)
    cardholder = db.Column(db.String(100), nullable=False)
    cardnumber = db.Column(db.Integer, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    cvc = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'id: {self.id}, email: {self.email}'
