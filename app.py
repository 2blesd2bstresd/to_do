#!flask/bin/python
import os
from flask import Flask, jsonify, abort
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
    return 'vielkom and bienvenue.'

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
