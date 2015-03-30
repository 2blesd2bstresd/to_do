from database import db

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    profile_url = db.Column(db.String)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String)

    def __init__(self, username, password, first_name=None, last_name=None, email=None, profile_url=None):

        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.profile_url = profile_url

    def __repr__(self):
        return '<User %r>' & self.username


class Spotkey(db.Model):

    __tablename__ = "spotkeys"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    location_type = db.Column(db.String)
    primary_spot_id = db.Column(db.Integer)
    name = db.Column(db.String)
    create_date = db.Column(db.String, nullable=False)
    share_with_all = db.Column(db.Boolean)

    def __init__(self, owner_id, name, create_date, location_type=None, share_with_all=False, primary_spot_id=None):

        self.owner_id = owner_id
        self.name = name
        self.create_date = create_date
        self.primary_spot_id = primary_spot_id
        self.location_type = location_type
        self.share_with_all = share_with_all

    def __repr__(self):
        return '<Spotkey %r>' % self.name

class Spot(db.Model):

    __tablename__ = "spots"

    id = db.Column(db.Integer, primary_key=True)
    spotkey_id = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.Integer, nullable=False) 
    street_address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zipcode = db.Column(db.String)
    transport_type = db.Column(db.String)
    buzzer_code = db.Column(db.String)
    requires_navigation = db.Column(db.Boolean)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    door_number = db.Column(db.Integer)
    details = db.Column(db.String)
    cross_street = db.Column(db.String)

    def __init__(self, spotkey_id, priority, transport_type='Any', requires_navigation=False, 
                 latitude=None, longitude=None, street_address=None, 
                 city=None, state=None, zipcode=None, buzzer_code=None, door_number=None, 
                 details=None, cross_street=None):

        self.spotkey_id = spotkey_id
        self.priority = priority
        self.transport_type = transport_type
        self.requires_navigation = requires_navigation
        self.latitude = latitude
        self.longitude = longitude
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.buzzer_code = buzzer_code
        self.door_number = door_number
        self.details = details
        self.cross_street = cross_street

    def __repr__(self):
        return '<Spot %r>' % self.priority