from application import db
from application.models import Base


class WorkingPeriod(Base):

    time = db.Column(db.DateTime, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    quality = db.Column(db.Float)

    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __init__(self, time, length, quality):
        self.time = time
        self.length = length
        self.quality = quality
