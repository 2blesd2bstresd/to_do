# config.py
import os
# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'd7v42p7jdric0f' 
USERNAME = 'wkobrhjtxlhagg' 
PASSWORD = 'tClZy72_NPXiFpwt7IRVh1vSAa' 
CSRF_ENABLED = True 
SECRET_KEY = 'my_precious'

KEY = 'AKIAJOWTE7ICGRTG4HFQ'
SECRET = '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'
BUCKET = 'spotkey-host'


# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# DB URL
URL = '//wkobrhjtxlhagg:tClZy72_NPXiFpwt7IRVh1vSAa@ec2-23-23-225-50.compute-1.amazonaws.com:5432/d7v42p7jdric0f'

# database URI
SQLALCHEMY_DATABASE_URI = 'postgres://wkobrhjtxlhagg:tClZy72_NPXiFpwt7IRVh1vSAa@ec2-23-23-225-50.compute-1.amazonaws.com:5432/d7v42p7jdric0f'
