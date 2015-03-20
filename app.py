#!flask/bin/python
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import urlparse
from flask import Flask, jsonify, abort, request
from datetime import datetime
import json


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

def get_conn_cursor():

    print "URL: ", url

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


app = Flask(__name__)


@app.route('/')
def hi():
    return 'vielkom and bienvenue.'

@app.route('/add_user/<name>', methods=['GET'])
def add_user(name):
    c = get_conn_cursor()
    try:
        query = str("INSERT INTO users (first_name) VALUES (\'%s\')" % name)
        c.execute(query)
    except psycopg2.Error as e:
        print 'HERES THE ERROR: ', e.diag.message_primary
        return 'nooooo'
    return 'success!'

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):

    # get the query cursor
    c = get_conn_cursor()

    # get the user info
    c.execute("SELECT id, first_name, last_name, profile_url FROM users WHERE id=%s" % user_id)
    u = c.fetchone()

    if not u:
        abort(404)

    user = {}
    user['id'] = u.get('id', None)
    user['first_name'] = u.get('first_name', None)
    user['last_name'] = u.get('last_name', None)
    user['profile_url'] = u.get('profile_url', None)

    # get the users spotkeys
    c.execute("SELECT id, name, owner_id FROM spotkeys WHERE owner_id=%s" % user_id)
    spotkeys = []
    for sk in c.fetchall():
        spotkey = {'name' : sk.get('name', None),
                   'id' : sk.get('id', None),
                   'owner_id' : sk.get('owner_id', None)}
        spotkeys.append(spotkey)
    for sk in spotkeys:
        c.execute("SELECT id, longitude, latitude, picture_url FROM spots WHERE spotkey_id=%s" % sk.get('id', None))
    user['spotkeys'] = spotkeys



    # get the users contacts
    contacts = []
    c.execute("SELECT first_user, first_user_id, first_user_profile_url FROM Contacts WHERE second_user_id=%s" % user_id)
    for con in c.fetchall():
        contact = {'username': con.get('first_user', None),
                   'id': con.get('first_user_id', None),
                   'profile_url': con.get('first_user_profile_url', None)}
        contacts.append(contact)

    c.execute("SELECT second_user, second_user_id, second_user_profile_url FROM Contacts WHERE first_user_id=%s" % user_id)
    for con in c.fetchall():
        contact = {'username': con.get('second_user', None),
                   'id': con.get('second_user_id', None),
                   'profile_url': con.get('second_user_profile_url', None)}
        contacts.append(contact)
    user['contacts'] = contacts
    
    return jsonify(user)


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

    print "SPOTKEY TRANSPORT TYPE: ", spotkey_id, ': ', transport_type
    try:
        c.execute("SELECT * FROM spots WHERE spotkey_id={0} AND transport_type=\'{1}\' ORDER BY priority".format(spotkey_id, transport_type))
        spots=c.fetchall()
    except:
        spots = ''

    if not spots:
        return jsonify({'error': 'No Spots.',
                 'error_code': 1})
    return jsonify({'spots': spots})



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port = port)

