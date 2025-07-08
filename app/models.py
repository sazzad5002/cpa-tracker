from app import db, login_manager
from flask_login import UserMixin
import time, uuid

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    url = db.Column(db.String(500))

class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    click_id = db.Column(db.String(100), unique=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    country = db.Column(db.String(5))
    timestamp = db.Column(db.Integer)

class Conversion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    click_id = db.Column(db.String(100))
    revenue = db.Column(db.Float)
    country = db.Column(db.String(5))
    timestamp = db.Column(db.Integer)
