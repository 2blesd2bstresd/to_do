#!flask/bin/python
import os
import psycopg2
# from functools import wraps
from psycopg2.extras import RealDictCursor
import urlparse
from flask import Flask, jsonify, abort, request, session, Response, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from sqlalchemy import exc, desc
from datetime import datetime
import json
from database import db
from models import User, Spot, Spotkey, Contact
import config
from serialize import serialize

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(config.URL)
app = db.app
# login_manager = LoginManager()
# login_manager.init_app(app)

def get_spotkeys(user_id):


    spotkeys = Spotkey.query.filter_by(owner_id=user_id)

    sk_list = []
    for sk in spotkeys:
        spotkey = {
                    'name' : sk.name,
                    'id' : sk.id,
                    'owner_id' : sk.owner_id,
                    'primary_spot_id': sk.primary_spot_id
                   }
        sk_list.append(spotkey)


    for sk in sk_list:
        spot = Spot.query.filter_by(id=sk.get('primary_spot_id', None)).first()
        sk['spot'] = {
                       'id': spot.id,
                       'longitude': spot.longitude,
                       'latitude': spot.latitude,
                       'picture_url': spot.picture_url,
                       'requires_navigation': spot.requires_navigation,
                       'details': spot.details
                     }
    return sk_list

def load_user(userid):
    return User.get(userid)

@app.route('/')
def hi():
    try:
        from models import Spotkey
        sk = Spotkey(2, 'tester', datetime.now())
    except Exception, e:
        print 'trace: ', e
    print 'SKID: ', sk.id
    return 'vielkom and bienvenue.'

@app.route('/login', methods=['POST'])
def login():

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
        for sk in get_spotkeys(user['id']):
            spotkeys.append(sk)
        user['spotkeys'] = spotkeys

        # get the users contacts
        contact_list = []
        contacts = Contact.query.filter_by(primary_id=user['id'])
        for con in contacts:
            contact = {'username': con.contact_username,
                       'id': con.contact_id,
                       'profile_url': con.profile_url}
            contact_list.append(contact)
        user['contacts'] = contact_list
        
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

    print form

    name = form.get('name', None)
    share_with_all = form.get('share_with_all', False)
    location_type = form.get('location_type', None)
    street_address = form.get('street_address', None)
    street_address_2 = form.get('street_address_2', None)
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

    db.session.add(sk)
    db.session.commit()

    s = Spot(sk.id, 1, transport_type, requires_navigation, 
                 latitude, longitude, street_address, street_address_2,
                 city, state, zipcode, buzzer_code, door_number, 
                 details, cross_street)

    db.session.add(s)
    db.session.commit()

    sk.primary_spot_id = s.id
    db.session.add(sk)
    db.session.commit()

    return jsonify({'status_code':200, 'date':datetime.now(), 'spotkey_id': sk.id})



@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):

    # get the user info
    try:
        u = User.query.filter_by(id=user_id).first()
    except:
        abort(404)

    user = {
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'profile_url': u.profile_url,
            'username': u.username
            }

    spotkey_list = []
    for sk in get_spotkeys(user_id):
        spotkey_list.append(sk)
    user['spotkeys'] = spotkey_list

    # get the users contacts
    contact_list = []
    contacts = Contact.query.filter_by(primary_id=user['id'])
    for con in contacts:
        contact = {
                   'username': con.contact_username,
                   'id': con.contact_id,
                   'profile_url': con.profile_url
                  }
        contact_list.append(contact)
    user['contacts'] = contact_list
    
    return jsonify(user)


@app.route('/all_spotkeys/<int:user_id>', methods=['GET'])
def all_spotkeys(user_id):

    contacts = Contact.query.filter_by(primary_id=user_id)
    
    contacts = [con.contact_id for con in contacts]
    contacts.append(user_id)
    spotkeys = []
    for con_id in contacts:
        for sk in (get_spotkeys(con_id)):
            # print "SPOTKEYS: ", sk
            spotkeys.append(sk)
    return jsonify({'spotkeys': spotkeys})


# @app.route('/spotkey/<int:spotkey_id>', methods=['GET'])
# def get_spotkey(spotkey_id):

#     spotkey = Spotkey.query.filter_by(id=spotkey_id)

#     spot = Spot.query.filter_by(id=spotkey.primary_spot_id)

#     spotkey['spot'] = spot

#     if not spotkey:
#             abort(404)
#     return jsonify({'spotkey': spotkey})


@app.route('/spotkey/<int:spotkey_id>/spots/<string:transport_type>', methods=['GET'])
def get_spot(spotkey_id, transport_type):


    spots = Spot.query.filter_by(spotkey_id=spotkey_id).filter_by(transport_type=transport_type).order_by(desc(Spot.priority))
    spots_list = [serialize(spot) for spot in spots]

    if not spots:
        return jsonify({'error': 'No Spots.',
                 'error_code': 1})
    return jsonify({'spots': spots_list})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port = port, debug=True)

