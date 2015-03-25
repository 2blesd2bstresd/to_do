# config.py
import os
# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'ec2-23-21-183-70.compute-1.amazonaws.com' 
USERNAME = 'yymrdbzqoowsqh' 
PASSWORD = '1bmpBpFOiKPLzweXcuX04FASwB' 
CSRF_ENABLED = True 
# SECRET_KEY = 'my_precious'
# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# database URI
SQLALCHEMY_DATABASE_URI = 'postgres://yymrdbzqoowsqh:1bmpBpFOiKPLzweXcuX04FASwB@ec2-23-21-183-70.compute-1.amazonaws.com:5432/d7p0rp7lvl3e7b'
