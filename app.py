#!flask/bin/python
import os
import psycopg2
import urlparse
from flask import Flask, jsonify, abort, request


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

def get_conn_cursor():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    c = conn.cursor()
    return conn, c


app = Flask(__name__)

users = [
    {
        'id': 1,
        'name': u'Max',
        'profile_url': u'http://bit.ly/1xz3ZlP',
        'spotkeys': [{'name': u'home', 'id': 1},
                    {'name': u'work', 'id': 5}],
        'contacts': [{'name': u'Angelica', 'id': 2,},
                     {'name': u'Tim', 'id': 3}] 
    },
    {
        'id': 2,
        'title': u'Angelica',
        'profile_url': u'http://bit.ly/1xz3ZlP',
        'spotkeys': [{'name': u'home', 'id': 2}],
        'contacts': [{'name': u'Max', 'id': 1,},
                     {'name': u'Tim', 'id': 3}] 
    },
    {
        'id': 3,
        'name': u'Tim',
        'profile_url': u'http://bit.ly/1xz3ZlP',
        'spotkeys': [{'name': u'home', 'id': 3}],
        'contacts': [{'name': u'Angelica', 'id': 2,},
                     {'name': u'Max', 'id': 1}] 
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
    print 'HERES THE REQUEST: ', request.headers
    return 'vielkom and bienvenue.'

@app.route('/add_user', methods=['GET'])
def add_user(name):
    print 'get this party started'
    try:
        conn, c = get_conn_cursor()
        c.execute('INSERT INTO Users (first_name) VALUES (%s)' % first_name)
        conn.commit()
        return 'success!'
    except:
        return 'no soup for you'

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = [u for u in users if u['id'] == user_id]
    if not user:
        abort(404)
    return jsonify({'user': user[0]})

@app.route('/spotkey/<int:spotkey_id>', methods=['GET'])
def get_spotkey(spotkey_id):
    spotkey = [sk for sk in spotkeys if sk['id'] == spotkey_id]
    if not spotkey:
        abort(404)
    return jsonify({'spotkey': spotkey[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port = port)
