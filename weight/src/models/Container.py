from ..database import db


class Container(db.Model):
    __tablename__ = 'containers_registered'
    container_id = db.Column(db.String(15), primary_key=True)
    weight = db.Column(db.Integer,default = None)
    unit = db.Column(db.String(10), default = None)

    def __repr__(self):
        return f'<Container {self.container_id}>'
