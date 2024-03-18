from app import db

class Rate(db.Model):
    __tablename__ = 'Rates'
    product_id = db.Column(db.String(50), primary_key=True)
    rate = db.Column(db.Integer, default=0)
    scope = db.Column(db.Integer, db.ForeignKey('Provider.id')) 
    provider = db.relationship('Provider', backref='rates')
