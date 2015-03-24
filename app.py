#!flask/bin/python
import os
import psycopg2
# from functools import wraps
from psycopg2.extras import RealDictCursor
import urlparse
from flask import Flask, jsonify, abort, request, session, Response
# from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import json


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])


app = Flask(__name__)
# app.config.from_object('config')
# db = SQLAlchemy(app)
# from models import User


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
        c.execute("SELECT id, longitude, latitude, picture_url, details, requires_navigation FROM spots WHERE id=%s" % sk.get('primary_spot_id', None))
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

    c.execute("SELECT id, username, first_name, last_name, profile_url FROM users WHERE username=\'{0}\' AND password=\'{1}\'".format(username, password))
    u = c.fetchone()

    if u:
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
    else:
        return 'interesting'
    #     # get the users spotkeys
    #     # user['spotkeys'] = get_spotkeys(user_id)

    #     # get the users contacts
    #     try:
    #         contacts = []
    #         c.execute("SELECT contact_username , contact_id, profile_url FROM Contacts WHERE primary_id=%s" % user_id)
    #         for con in c.fetchall():
    #             contact = {'username': con.get('contact_username', None),
    #                        'id': con.get('contact_id', None),
    #                        'profile_url': con.get('profile_url', None)}
    #             contacts.append(contact)
    #         user['contacts'] = contacts
    #     except:
    #         return 'adding contacts'
        
    #     return jsonify(user)

    # else:
    #     return (make_response(jsonify({'error': 'Incorrect Credentials'}), 401))
    # return 'interesting'


@app.route('/add_user', methods=['POST'])
def register_user():

    form = request.form

    first_name = form.get('first_name', None)
    last_name = form.get('last_name', None)
    email = form.get('email', None)
    username = form.get('username', None)
    password = form.get('password', None)

    c = get_conn_cursor()
    try:
        query = str("""INSERT INTO users (first_name, 
                                        last_name, 
                                         email, 
                                         username, 
                                         password) 
                       VALUES (\'{0}\', 
                               \'{1}\', 
                               \'{2}\', 
                               \'{3}\', 
                               \'{4}\')""".format(first_name, last_name, email, username, password))
        c.execute(query)
    except psycopg2.Error as e:
        r = jsonify({'Error': e})
        r.status_code = 400
        return r
    return jsonify ({'status_code': 200, 'date': datetime.now()})


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
    c.execute("SELECT * FROM spots WHERE spotkey_id={0} AND transport_type=\'{1}\' ORDER BY priority".format(spotkey_id, transport_type))        
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

