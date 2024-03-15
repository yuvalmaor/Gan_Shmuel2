from database import db

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer(), primary_key=True)
    datetime = db.Column(db.DateTime)
    direction = db.Column(db.String(10))
    truck = db.Column(db.String(50))
    containers = db.Column(db.String(10000))
    bruto = db.Column(db.Integer())
    truckTara = db.Column(db.Integer())
    #!custom type
    neto = db.Column(db.Integer(), default="na")
    produce = db.Column(db.String(50))
    session_id = db.Column(db.Integer())

    def __repr__(self):
        return f'<Container {self.container_id}>'
