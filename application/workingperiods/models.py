from application import db
from application.models import Base
from sqlalchemy.sql import text
from datetime import *
from sqlalchemy import orm


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

    # When getting objects from database, __init__ isn't called, but the below reconstructor is
    @orm.reconstructor
    def init_on_load(self):
        self.details_string = "On "
        # On some systems / sql versions, time is returned as string
        if type(self.time) is not datetime:
            self.details_string += str(self.time)
        else:
            self.details_string += self.time.strftime("%B %e, %Y, at %-H:%M")
        self.details_string += ", worked for " + str(self.length) + " minutes."
        if self.quality is not None:
            self.details_string += (" Quality was " + str(self.quality) + ".")
