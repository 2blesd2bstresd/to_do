from app import db
import datetime

class Test(db.Model):

	__tablename__ = "test"

	value = db.Column(db.String, primary_key=True)

	def __init__(self, value):

		self.value = name

	def __repr__(self):
		return '<name %r>' % (self.value)

