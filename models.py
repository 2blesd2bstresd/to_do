from app import db

class Test(db.Model):
	
	__tablename__ = "test"
	
	value = db.Column(db.String, primary_key=True)
	
	def __init__(self, value):

		self.value = value

	def __repr__(self):
		return '<value %r>' % (self.value)

