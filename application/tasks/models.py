from application import db
from application.models import Base
from sqlalchemy.sql import text


class Task(Base):

    name = db.Column(db.String(144), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    estimate = db.Column(db.Integer)
    progress = db.Column(db.Float)

    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)

    def __init__(self, name):
        self.name = name
        self.done = False

    @staticmethod
    def get_total_time_spent_on_task(task_id):
        stmt = text(
            "SELECT SUM(working_period.length) FROM working_period WHERE working_period.task_id = " + str(task_id))
        res = db.engine.execute(stmt)
        for row in res:
            # res contains only one row
            return row[0]
