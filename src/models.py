from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(45), primary_key=True)
    password = db.Column(db.String(45), unique=True)
    def __init__(self, name, pwd):
        self.id = name
        self.password = pwd

    