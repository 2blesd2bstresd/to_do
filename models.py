from views import db
import datetime

class User(db.Model):

	__tablename__ = "users"

	user_id = db.Column(db.Integer, primary_key=True, unique=True)
	first_name = db.Column(db.String)
	last_name = db.Column(db.String)
	email = db.Column(db.String)
	username = db.Column(db.String, nullable=True)
	password = db.Column(db.Integer, nullable=True)
	create_date = db.Column(db.Date, default=datetime.datetime.utcnow(), nullable=False)

	def __init__(self, first_name, last_name, email, username, password):

		self.first_name = first_name
		self.due_date = due_date
		self.priority = priority
		self.status = status
		self.user_id = user_id

	def __repr__(self):
		return '<name %r>' % (self.name)