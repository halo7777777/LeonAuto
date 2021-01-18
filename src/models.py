from app import db
from sqlalchemy.orm import class_mapper

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(45), primary_key=True)
    password = db.Column(db.String(45), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    
    def as_dict(self):
        # 转json
        return dict((col.name, getattr(self, col.name)) \
        for col in class_mapper(self.__class__).mapped_table.c)