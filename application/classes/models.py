from application import db
from application.models import Base

class Class(Base):

    name = db.Column(db.String(144), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)

    def __init__(self, name):
        self.name = name

    # Many-to-many relationship table
    classtask = db.Table('classtask',
        db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True),
        db.Column('task_id', db.Integer, db.ForeignKey('task.id', primary_key=True)))
