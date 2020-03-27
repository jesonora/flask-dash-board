from app.extensions import db

class Portfolio(db.Model):
    __tablename__ = 'portfolio'

    id = db.Column(db.Integer,  primary_key=True)
    date = db.Column(db.DateTime())
    travel_product = db.Column(db.String())
    sessions_ac = db.Column(db.Integer())
    bookings_ac = db.Column(db.Integer())
    revenue_ac = db.Column(db.Integer())
    spend_ac = db.Column(db.Float())
    day_month = db.Column(db.Integer())
    day_week = db.Column(db.Integer())
    week = db.Column(db.Integer())
    month = db.Column(db.Integer())
    quarter = db.Column(db.Integer())
    year = db.Column(db.Integer())
    sessions_aa = db.Column(db.Integer())
    bookings_aa = db.Column(db.Integer())
    revenue_aa = db.Column(db.Integer())
    spend_aa = db.Column(db.Float())
    category = db.Column(db.String())
    birst_category = db.Column(db.String())
    ga_category = db.Column(db.String())

    @staticmethod
    def get_all_blogposts():
        return Portfolio.query.all()

    @staticmethod
    def get_one_blogpost(date):
        return Portfolio.query.get(date)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return "<User: {}>".format(self.username)

class GeoData(db.Model):
    __tablename__ = 'geodata'

    id = db.Column(db.Integer, primary_key=True)
    name_1 = db.Column(db.String())
    name_2 = db.Column(db.String())
    cc_2 = db.Column(db.String())
    nat2018 = db.Column(db.Float())
    geometry = db.Column(db.String())

    def __repr__(self):
        return "<User: {}>".format(self.username)

