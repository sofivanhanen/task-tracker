from application import db, classtask
from application.models import Base
from sqlalchemy.sql import text
from sqlalchemy import orm


class Class(Base):

    name = db.Column(db.String(144), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)

    count = -1
    parsed_date = None

    # Getting the tasks relevant to this class from classtask table
    # backref creates a similar list of classes for tasks
    tasks = db.relationship('Task', secondary=classtask, lazy='subquery',
                            backref='classes')

    def __init__(self, name):
        self.name = name
        self.parsed_date = self.date_created.strftime("%B %d, %Y")
        self.count = len(self.tasks)

    # When getting objects from database, __init__ isn't called, but the below reconstructor is
    @orm.reconstructor
    def init_on_load(self):
        # Can't make a method for these, because this method can't find other methods
        self.parsed_date = self.date_created.strftime("%B %d, %Y")
        self.count = len(self.tasks)
