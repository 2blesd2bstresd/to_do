from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yymrdbzqoowsqh:1bmpBpFOiKPLzweXcuX04FASwB@ec2-23-21-183-70.compute-1.amazonaws.com:5432/d7p0rp7lvl3e7b'
db = SQLAlchemy(app)