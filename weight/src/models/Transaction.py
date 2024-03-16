from ..database import db

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer(), primary_key=True)
    datetime = db.Column(db.DateTime, default = None)
    direction = db.Column(db.String(10), default = None)
    truck = db.Column(db.String(50), default = None)
    containers = db.Column(db.String(10000), default = None)
    bruto = db.Column(db.Integer(), default = None)
    truckTara = db.Column(db.Integer(), default = None)
    neto = db.Column(db.Integer(), default = None)
    produce = db.Column(db.String(50), default = None)
    session_id = db.Column(db.Integer(), default = None)

    def __repr__(self):
        return f'<Container {self.container_id}>'
