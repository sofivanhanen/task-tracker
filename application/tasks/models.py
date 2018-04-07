from application import db
from application.models import Base


class Task(Base):

    name = db.Column(db.String(144), nullable=False)
    done = db.Column(db.Boolean, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)

    def __init__(self, name):
        self.name = name
        self.done = False


class WorkingPeriod(Base):

    time = db.Column(db.DateTime, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    quality = db.Column(db.Float)

    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def __init__(self, time, length, quality):
        self.time = time
        self.length = length
        self.quality = quality
