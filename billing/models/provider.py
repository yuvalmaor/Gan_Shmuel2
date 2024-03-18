from app import db

class Provider(db.Model):
    __tablename__ = 'Provider'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))