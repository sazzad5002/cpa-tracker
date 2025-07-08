from . import db

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    payout = db.Column(db.Float, nullable=False)

class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

class Conversion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
