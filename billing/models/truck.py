from app import db

class Truck(db.Model):
    __tablename__ = 'Trucks'  # Specify the table name explicitly to match the schema
    id = db.Column(db.String(10), primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship('Provider', backref='trucks')