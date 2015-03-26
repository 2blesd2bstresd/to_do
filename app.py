#!flask/bin/python
import os
import psycopg2
# from functools import wraps
from psycopg2.extras import RealDictCursor
import urlparse
from flask import Flask, jsonify, abort, request, session, Response
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import json

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse('//yymrdbzqoowsqh:1bmpBpFOiKPLzweXcuX04FASwB@ec2-23-21-183-70.compute-1.amazonaws.com:5432/d7p0rp7lvl3e7b')

app = Flask(__name__)
app.config.from_object('config')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yymrdbzqoowsqh:1bmpBpFOiKPLzweXcuX04FASwB@ec2-23-21-183-70.compute-1.amazonaws.com:5432/d7p0rp7lvl3e7b'
db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    profile_url = db.Column(db.String)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String)

    def __init__(self, username, password, first_name=None, last_name=None, email=None, profile_url=None):

        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.profile_url = profile_url

    def __repr__(self):
        return '<User %r>' & self.username


class Spotkey(db.Model):

    __tablename__ = "spotkeys"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    location_type = db.Column(db.String)
    primary_spot_id = db.Column(db.Integer)
    name = db.Column(db.String)
    create_date = db.Column(db.String, nullable=False)
    share_with_all = db.Column(db.Boolean)

    def __init__(self, owner_id, name, create_date, location_type=None, share_with_all=False, primary_spot_id=None):

        self.owner_id = owner_id
        self.name = name
        self.create_date = create_date
        self.primary_spot_id = primary_spot_id
        self.location_type = location_type
        self.share_with_all = share_with_all

    def __repr__(self):
        return '<Spotkey %r>' % self.name

class Spot(db.Model):

    __tablename__ = "spots"

    id = db.Column(db.Integer, primary_key=True)
    spotkey_id = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.Integer, nullable=False) 
    location_type = db.Column(db.String)
    street_address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zipcode = db.Column(db.String)
    transport_type = db.Column(db.String)
    buzzer_code = db.Column(db.String)
    requires_navigation = db.Column(db.Boolean)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    door_number = db.Column(db.Integer)
    details = db.Column(db.String)
    cross_street = db.Column(db.String)

    def __init__(self, spotkey_id, priority, transport_type='Any', requires_navigation=False, 
                 latitude=None, longitude=None, location_type=None, street_address=None, 
                 city=None, state=None, zipcode=None, buzzer_code=None, door_number=None, 
                 details=None, cross_street=None):

        self.spotkey_id = spotkey_id
        self.priority = priority
        self.transport_type = transport_type
        self.requires_navigation = requires_navigation
        self.latitude = latitude
        self.longitude = longitude
        self.location_type = location_type
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.buzzer_code = buzzer_code
        self.door_number = door_number
        self.details = details
        self.cross_street = cross_street

    def __repr__(self):
        return '<Spot %r>' % self.priority


def get_conn_cursor():

    conn = psycopg2.connect(
        database=url.path[1:],
        user='yymrdbzqoowsqh',  
        password='1bmpBpFOiKPLzweXcuX04FASwB',
        host=url.hostname,
        port=url.port
    )
    conn.autocommit=True
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return c


def get_spotkeys(user_id, c):

    c.execute("SELECT id, name, owner_id, primary_spot_id FROM spotkeys WHERE owner_id=%s" % user_id)
    spotkeys = []
    for sk in c.fetchall():
        spotkey = {'name' : sk.get('name', None),
                   'id' : sk.get('id', None),
                   'owner_id' : sk.get('owner_id', None),
                   'primary_spot_id': sk.get('primary_spot_id', None)}
        spotkeys.append(spotkey)
    for sk in spotkeys:
        c.execute("SELECT id, longitude, latitude, picture_url, details, requires_navigation, priority FROM spots WHERE id=%s" % sk.get('primary_spot_id', None))
        spot = c.fetchone()
        sk['spot'] = {'id': spot.get('id', None),
                      'longitude': spot.get('longitude', None),
                      'latitude': spot.get('latitude', None),
                      'picture_url': spot.get('picture_url', None),
                      'requires_navigation': spot.get('requires_navigation', None),
                      'details': spot.get('details', None)
                    }
    return spotkeys


@app.route('/')
def hi():
    return 'vielkom and bienvenue.'

@app.route('/login', methods=['POST'])
def login():

    c = get_conn_cursor()

    auth = request.authorization
    username = auth.get('username', None)
    password = auth.get('password', None)
    u = User.query.filter_by(username=username).filter_by(password=password).first()
    if u:
        user = {}
        user['id'] = u.id
        user['first_name'] = u.first_name
        user['last_name'] = u.last_name
        user['profile_url'] = u.profile_url
        user['username'] = u.username

        # Get users spotkeys
        spotkeys = []
        for sk in get_spotkeys(user['id'], c):
            spotkeys.append(sk)
        user['spotkeys'] = spotkeys

        # get the users contacts
        contacts = []
        c.execute("SELECT contact_username , contact_id, profile_url FROM Contacts WHERE primary_id=%s" % user['id'])
        for con in c.fetchall():
            contact = {'username': con.get('contact_username', None),
                       'id': con.get('contact_id', None),
                       'profile_url': con.get('profile_url', None)}
            contacts.append(contact)
        user['contacts'] = contacts
        
        return jsonify(user)
    else:
        return abort(401)


@app.route('/add_user', methods=['POST'])
def register_user():

    form = request.form

    first_name = form.get('first_name', None)
    last_name = form.get('last_name', None)
    email = form.get('email', None)
    username = form.get('username', None)
    password = form.get('password', None)

    u = User(username, password, first_name, last_name, email)
    db.session.add(u)
    db.session.commit()

    return jsonify ({'status_code': 200, 'date': datetime.now(), 'data': form.to_dict()})


@app.route('/create_spotkey', methods=['POST'])
def create_spotkey():
    
    form = request.form

    name = form.get('name', None)
    share_with_all = form.get('share_with_all', False)
    location_type = form.get('location_type', None)
    street_address = form.get('street_address', None)
    city = form.get('city', None)
    state = form.get('state', None)
    zipcode = form.get('zipcode', None)
    transport_type = form.get('transport_type', None)
    buzzer_code = form.get('buzzer_code')
    requires_navigation = form.get('requires_navigation', None)
    latitude = form.get('latitude', None)
    longitude = form.get('longitude', None)
    door_number = form.get('door_number', None)
    details = form.get('details', None)
    cross_street = form.get('cross_street', None)

    sk = Spotkey(2, name, datetime.now(), location_type, share_with_all)


    s = Spot(50, 1, transport_type, requires_navigation, 
                 latitude, longitude, location_type, street_address, 
                 city, state, zipcode, buzzer_code, door_number, 
                 details, cross_street)

    db.session.add(sk)
    db.session.add(s)

    # sk.primary_spot_id = s.id
    # db.session.add(sk)
    # db.session.commit()



    return jsonify({'status_code':200, 'date':datetime.now()})



@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):

    # get the query cursor
    c = get_conn_cursor()

    # get the user info
    c.execute("SELECT id, username, first_name, last_name, profile_url FROM users WHERE id=%s" % user_id)
    u = c.fetchone()

    if not u:
        abort(404)

    user = {}
    user['id'] = u.get('id', None)
    user['first_name'] = u.get('first_name', None)
    user['last_name'] = u.get('last_name', None)
    user['profile_url'] = u.get('profile_url', None)
    user['username'] = u.get('username', None)
    spotkeys = []
    for sk in get_spotkeys(user_id, c):
        spotkeys.append(sk)
    user['spotkeys'] = spotkeys

    # get the users spotkeys
    # user['spotkeys'] = get_spotkeys(user_id)

    # get the users contacts
    try:
        contacts = []
        c.execute("SELECT contact_username , contact_id, profile_url FROM Contacts WHERE primary_id=%s" % user_id)
        for con in c.fetchall():
            contact = {'username': con.get('contact_username', None),
                       'id': con.get('contact_id', None),
                       'profile_url': con.get('profile_url', None)}
            contacts.append(contact)
        user['contacts'] = contacts
    except:
        return 'adding contacts'
    
    return jsonify(user)


@app.route('/all_spotkeys/<int:user_id>', methods=['GET'])
def all_spotkeys(user_id):
    c = get_conn_cursor()

    spotkeys = []

    c.execute("SELECT contact_id FROM Contacts WHERE primary_id=%s" % user_id)
    contacts = [con.get('contact_id', None) for con in c.fetchall()]
    contacts.append(user_id)

    spotkeys = []
    for con_id in contacts:
        for sk in (get_spotkeys(con_id, c)):
            spotkeys.append(sk)
    return jsonify({'spotkeys': spotkeys})


@app.route('/spotkey/<int:spotkey_id>', methods=['GET'])
def get_spotkey(spotkey_id):
    c = get_conn_cursor()

    c.execute("SELECT * FROM spotkeys WHERE id=%s" % spotkey_id)

    spotkey=c.fetchone()
    c.execute("SELECT * FROM spots WHERE id=%s" % spotkey.get('primary_spot_id', None))

    spot = c.fetchone()
    spotkey['spot'] = spot

    if not spotkey:
            abort(404)
    return jsonify({'spotkey': spotkey})


@app.route('/spotkey/<int:spotkey_id>/spots/<string:transport_type>', methods=['GET'])
def get_spot(spotkey_id, transport_type):
    c = get_conn_cursor()
    c.execute("SELECT * FROM spots WHERE spotkey_id={0} AND transport_type=\'{1}\' ORDER BY priority DESC".format(spotkey_id, transport_type))        
    spots=c.fetchall()

    if not spots:
        return jsonify({'error': 'No Spots.',
                 'error_code': 1})
    return jsonify({'spots': spots})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port = port)

