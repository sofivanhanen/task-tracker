from application import db
from application.models import Base
from sqlalchemy.sql import text
from datetime import *


class WorkingPeriod(Base):

    time = db.Column(db.DateTime, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    quality = db.Column(db.Float)

    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __init__(self, time, length, quality):
        self.time = time
        self.length = length
        self.quality = quality

    @staticmethod
    def find_working_periods_as_string_for_task(task_id):
        stmt = text("SELECT working_period.time, working_period.length, working_period.quality FROM working_period INNER JOIN task ON task.id = working_period.task_id")
        res = db.engine.execute(stmt)

        # TODO why is time returned as string? Should be a datetime object.
        response = []
        for row in res:
            workstring = "On " + row[0] + \
                ", worked for " + str(row[1]) + " minutes."
            if row[2] is not None:
                workstring += (" Quality was " + str(row[2]) + ".")

            response.append(workstring)

        return response
