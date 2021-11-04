from app.dao.database import db


class DukeDB(db.Model):
    __tablename__ = 'duke'
    uid = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(32))
    url = db.Column(db.String(32))
    x = db.Column(db.Float())
    y = db.Column(db.Float())
    embedding = db.Column(db.LargeBinary())

    def __repr__(self):
        return '<Duke {}>'.format(self.uid)
