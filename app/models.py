from app import db
from datetime import datetime

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(500), nullable=False)

class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    country = db.Column(db.String(10))

class Conversion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
    revenue = db.Column(db.Float, default=0.0)
    country = db.Column(db.String(10))
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
