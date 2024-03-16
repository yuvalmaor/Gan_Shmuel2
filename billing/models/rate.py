from app import db

class Rate(db.Model):
    __tablename__ = 'Rates'  # Specify the table name explicitly to match the schema
    product_id = db.Column(db.String(50), primary_key=True)
    rate = db.Column(db.Integer, default=0)
    scope = db.Column(db.String(50), db.ForeignKey('provider.id'))
    provider = db.relationship('Provider', backref='rates')