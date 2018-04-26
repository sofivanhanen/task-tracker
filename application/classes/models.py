from application import db, classtask
from application.models import Base


class Class(Base):

    name = db.Column(db.String(144), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)

    # Getting the tasks relevant to this class from classtask table
    # backref creates a similar list of classes for tasks
    tasks = db.relationship('Task', secondary=classtask, lazy='subquery',
                            backref='classes')

    def __init__(self, name):
        self.name = name
