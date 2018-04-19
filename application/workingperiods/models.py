from application import db
from application.models import Base
from sqlalchemy.sql import text
from datetime import *


class WorkingPeriod(Base):

    time = db.Column(db.DateTime, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    quality = db.Column(db.Float)

    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    details_string = None

    def __init__(self, time, length, quality):
        self.time = time
        self.length = length
        self.quality = quality

    # Method used in task's details view, to list working periods related to the task.
    # We also create the details_string to easily show data on the working period
    @staticmethod
    def find_working_periods_with_string_for_task(task_id):
        stmt = text("SELECT working_period.time, working_period.length, working_period.quality, working_period.id FROM working_period WHERE working_period.task_id = " + str(task_id))
        res = db.engine.execute(stmt)

        response = []
        for row in res:

            workstring = "On "
            # On heroku time is returned as datetime. On local, using SQLite, it's returned as string...
            if type(row[0]) is str:
                workstring += row[0]
            else:
                workstring += row[0].strftime("%c")
            workstring += ", worked for " + str(row[1]) + " minutes."
            if row[2] is not None:
                workstring += (" Quality was " + str(row[2]) + ".")

            wp = WorkingPeriod.query.get(row[3])
            wp.details_string = workstring

            response.append(wp)

        return response
