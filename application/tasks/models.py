from application import db
from application.models import Base
from sqlalchemy.sql import text
from sqlalchemy import orm


class Task(Base):

    name = db.Column(db.String(144), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    estimate = db.Column(db.Integer)
    progress = db.Column(db.Float)

    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)

    parsed_date = None;

    def __init__(self, name):
        self.name = name
        self.done = False
        self.parsed_date = self.date_created.strftime("%B %d, %Y")

    # When getting objects from database, __init__ isn't called, but the below reconstructor is
    @orm.reconstructor
    def init_on_load(self):
        # Can't make a method for this, because this method can't find other methods
        self.parsed_date = self.date_created.strftime("%B %d, %Y")

    @staticmethod
    def get_total_time_spent_on_task(task_id):
        stmt = text(
            "SELECT SUM(working_period.length) FROM working_period WHERE working_period.task_id = " + str(task_id))
        res = db.engine.execute(stmt)
        for row in res:
            # res contains only one row
            return row[0]
