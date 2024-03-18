from app import db

class Truck(db.Model):
    __tablename__ = 'Trucks'
    id = db.Column(db.String(10), primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('Provider.id'), nullable=True)