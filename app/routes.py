from flask import render_template, redirect, url_for, request, flash, send_file
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from app.models import User, Offer, Click, Conversion
import uuid, time, requests

@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        user = User(username='admin', password='admin123')
        db.session.add(user)
        db.session.commit()

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        u = User.query.filter_by(username=request.form['username']).first()
        if u and u.password == request.form['password']:
            login_user(u); return redirect(url_for('dashboard'))
        flash('Invalid', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    offers = Offer.query.all()
    clicks = Click.query.all()
    convs = Conversion.query.all()
    return render_template('dashboard.html',
            offers=offers, clicks=clicks, convs=convs)

@app.route('/offerwall', methods=['GET','POST'])
@login_required
def offerwall():
    if request.method=='POST':
        n = request.form['name']; u = request.form['url']
        db.session.add(Offer(name=n,url=u)); db.session.commit()
    off = Offer.query.all()
    return render_template('offerwall.html', offers=off)

@app.route('/delete_offer/<int:id>')
@login_required
def delete_offer(id):
    Offer.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('offerwall'))

@app.route('/click')
def click():
    offer_id = int(request.args.get('offer_id'))
    off = Offer.query.get(offer_id)
    cid = str(uuid.uuid4())
    country = request.args.get('country', None)
    if not country:
        try:
            ip = request.remote_addr
            res = requests.get(f'http://ip-api.com/json/{ip}').json()
            country = res.get('countryCode','UN')
        except:
            country='UN'
    click = Click(click_id=cid, offer_id=offer_id,
                  country=country, timestamp=int(time.time()))
    db.session.add(click); db.session.commit()
    sep = '&' if '?' in off.url else '?'
    return redirect(off.url + sep + 'sub_id=' + cid)

@app.route('/postback')
def postback():
    click_id = request.args.get('click_id')
    revenue = float(request.args.get('revenue',0))
    country = request.args.get('country','UN')
    conv = Conversion(click_id=click_id, revenue=revenue,
                      country=country, timestamp=int(time.time()))
    db.session.add(conv); db.session.commit()
    return 'OK'

