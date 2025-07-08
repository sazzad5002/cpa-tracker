from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Offer, Click, Conversion
from . import db
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['admin'] = True
            return redirect(url_for('routes.dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@routes.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('routes.login'))

    offers = Offer.query.all()
    clicks = Click.query.all()
    conversions = Conversion.query.all()
    return render_template('dashboard.html', offers=offers, clicks=clicks, conversions=conversions)

@routes.route('/offerwall')
def offerwall():
    offers = Offer.query.all()
    return render_template('offerwall.html', offers=offers)

@routes.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('routes.login'))
