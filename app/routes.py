from flask import Blueprint, render_template, redirect, request, url_for, session
from .models import db, Offer, Click, Conversion
from datetime import datetime
import requests
import os

routes = Blueprint('routes', __name__)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['admin'] = True
            return redirect(url_for('routes.dashboard'))
    return render_template('login.html')

@routes.before_app_request
def require_login():
    if not session.get('admin') and request.endpoint not in ['routes.login', 'static']:
        return redirect(url_for('routes.login'))

@routes.route('/')
def dashboard():
    clicks = Click.query.all()
    conversions = Conversion.query.all()
    revenue = sum([c.revenue for c in conversions])
    return render_template('dashboard.html', clicks=clicks, conversions=conversions, revenue=revenue)

@routes.route('/offerwall', methods=['GET', 'POST'])
def offerwall():
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        offer = Offer(name=name, url=url)
        db.session.add(offer)
        db.session.commit()
    offers = Offer.query.all()
    return render_template('offerwall.html', offers=offers)

@routes.route('/click/<int:offer_id>')
def track_click(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return "Offer not found", 404

    click = Click(offer_id=offer_id, country='BD', datetime=datetime.utcnow())
    db.session.add(click)
    db.session.commit()

    return redirect(offer.url)

@routes.route('/postback', methods=['GET'])
def postback():
    offer_id = request.args.get('offer_id')
    revenue = float(request.args.get('revenue', 0))
    country = request.args.get('country', 'BD')
    conversion = Conversion(offer_id=offer_id, revenue=revenue, country=country, datetime=datetime.utcnow())
    db.session.add(conversion)
    db.session.commit()
    return "OK"
