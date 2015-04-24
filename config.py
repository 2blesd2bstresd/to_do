# config.py
import os
# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'deoavno39l5b77' 
USERNAME = 'ybkatgvscdceyo' 
PASSWORD = 'EpI-LS7-ceaExRerbNtpeLc-UY' 
CSRF_ENABLED = True 
SECRET_KEY = 'my_precious'

KEY = 'AKIAJOWTE7ICGRTG4HFQ'
SECRET = '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'
BUCKET = 'spotkey-host'


# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# DB URL
URL = '//ybkatgvscdceyo:EpI-LS7-ceaExRerbNtpeLc-UY@ec2-54-163-238-96.compute-1.amazonaws.com:5432/deoavno39l5b77'

# database URI
SQLALCHEMY_DATABASE_URI = 'postgres://ybkatgvscdceyo:EpI-LS7-ceaExRerbNtpeLc-UY@ec2-54-163-238-96.compute-1.amazonaws.com:5432/deoavno39l5b77'
