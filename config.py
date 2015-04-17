# config.py
import os
# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'd7p0rp7lvl3e7b' 
USERNAME = 'ngdndiaovlpgps' 
PASSWORD = 'yBzzZ1UBU7c2phcIMBfB4HHA5u' 
CSRF_ENABLED = True 
SECRET_KEY = 'my_precious'

KEY = 'AKIAJOWTE7ICGRTG4HFQ'
SECRET = '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'
BUCKET = 'spotkey-host'


# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# DB URL
URL = '//ngdndiaovlpgps:yBzzZ1UBU7c2phcIMBfB4HHA5u@ec2-23-21-183-70.compute-1.amazonaws.com:5432/d7p0rp7lvl3e7b'

# database URI
SQLALCHEMY_DATABASE_URI = 'postgres://ngdndiaovlpgps:yBzzZ1UBU7c2phcIMBfB4HHA5u@ec2-23-21-183-70.compute-1.amazonaws.com:5432/d7p0rp7lvl3e7b'
