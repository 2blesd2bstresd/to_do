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

users = [
    {
        'id': 1,
        'name': u'Max',
        'profile_url': u'http://bit.ly/1xz3ZlP',
        'spotkeys': [{'name': u'home', 'id': 1},
                    {'name': u'work', 'id': 5}],
        'contacts': [{'name': u'Angelica', 'id': 2, 'profile_url': u'http://bit.ly/1xz3ZlP'},
                     {'name': u'Tim', 'id': 3, 'profile_url': u'http://bit.ly/1xz3ZlP'}] 
    },
    {
        'id': 2,
        'title': u'Angelica',
        'profile_url': u'http://bit.ly/1xz3ZlP',
        'spotkeys': [{'name': u'home', 'id': 2}],
        'contacts': [{'name': u'Max', 'id': 1, 'profile_url': u'http://bit.ly/1xz3ZlP'},
                     {'name': u'Tim', 'id': 3, 'profile_url': u'http://bit.ly/1xz3ZlP'}] 
    },
    {
        'id': 3,
        'name': u'Tim',
        'profile_url': u'http://bit.ly/1xz3ZlP',
        'spotkeys': [{'name': u'home', 'id': 3}],
        'contacts': [{'name': u'Angelica', 'id': 2, 'profile_url': u'http://bit.ly/1xz3ZlP'},
                     {'name': u'Max', 'id': 1, 'profile_url': u'http://bit.ly/1xz3ZlP'}] 
    },
    {
        'id': 4,
        'title': u'Mike',
        'profile_url': u'http://bit.ly/1xz3ZlP',
        'spotkeys': [{'name': u'home', 'id': 4}],
        'contacts' : [] 
    },
]

spotkeys = [
    {
        'title': 'home',
        'id': 1,
        'owner_id':1,
        'longitude': 37.7813967,
        'latitude': -122.4044686
    },
    {
        'title': 'home',
        'id': 2,
        'owner_id':2,
        'longitude': 37.7813967,
        'latitude': -122.4044686
    },    
    {
        'title': 'home',
        'id': 3,
        'owner_id':3,
        'longitude': 37.7813967,
        'latitude': -122.4044686
    },
    {
        'title': 'home',
        'id': 4,
        'owner_id':4,
        'longitude': 37.7813967,
        'latitude': -122.4044686
    },
    {
        'title': 'work',
        'id': 5,
        'owner_id':1,
        'longitude': 37.7860898,
        'latitude': -122.3942683
    }]

@app.route('/')
def hi():
    print 'HERES THE REQUEST: ', dir(request)
    return 'vielkom and bienvenue.'

@app.route('/add_user/<name>', methods=['GET'])
def add_user(name):
    print "NAMENAMENAME: ", name
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
    c.execute("SELECT id, name FROM spotkeys WHERE owner_id=%s" % user_id)
    spotkeys = []
    for sk in c.fetchall():
        spotkey = {'name' : sk.get('name', None),
                   'id' : sk.get('id', None)}
        spotkeys.append(spotkey)
    user['spotkeys'] = spotkeys

    # get the users contacts
    contacts = []
    c.execute("SELECT first_user, first_user_id FROM Contacts WHERE second_user_id=%s" % user_id)
    for con in c.fetchall():
        contact = {'name': con.get('first_user', None),
                   'id': con.get('first_user_id', None)}
        contacts.append(contact)

    c.execute("SELECT second_user, second_user_id FROM Contacts WHERE first_user_id=%s" % user_id)
    for con in c.fetchall():
        contact = {'name': con.get('second_user', None),
                   'id': con.get('second_user_id', None)}
        contacts.append(contact)
    user['contacts'] = contacts
    
    return jsonify(user)


@app.route('/spotkey/<int:spotkey_id>', methods=['GET'])
def get_spotkey(spotkey_id):
    c = get_conn_cursor()

    try:
        c.execute("SELECT * FROM spotkeys WHERE id=%s" % spotkey_id)
    except:
        return 'SWEET'

    try:
        spotkey=c.fetchone()
    except:
        return "EMPTY QUERY"
    try:
        c.execute("SELECT * FROM spot WHERE id=%s" % spotkey.get('id', None))

        spot = c.fetchone()

        if not spotkey:
            abort(404)
        return jsonify({'spotkey': spotkey,
                        'spot': spot})
    except:
        return 'NOT SWEET'

@app.route('/spot/<int:spot_id>', methods=['GET'])
def get_spot(spot_id):
    c = get_conn_cursor()

    c.execute("SELECT * FROM spots WHERE id=%s" % spot_id)

    spot=c.fetchone()

    if not spot:
        return ({'error': 'No Spot',
                 'error_code': 1})
    return jsonify({'spot': spot})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port = port)






