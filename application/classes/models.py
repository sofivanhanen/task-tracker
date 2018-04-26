from application import db, classtask
from application.models import Base
from sqlalchemy.sql import text


class Class(Base):

    name = db.Column(db.String(144), nullable=False)
    count = 0

    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)

    # Getting the tasks relevant to this class from classtask table
    # backref creates a similar list of classes for tasks
    tasks = db.relationship('Task', secondary=classtask, lazy='subquery',
                            backref='classes')

    def __init__(self, name):
        self.name = name
        self.count = get_total_tasks_for_class(self.id)

    @staticmethod
    def get_total_tasks_for_class(class_id):
        stmt = text(
            "SELECT COUNT(task.id) FROM task INNER JOIN classtask ON classtask.task_id = task.id INNER JOIN class ON class.id = classtask.class_id WHERE class.id = " + str(class_id))
        res = db.engine.execute(res)
        for row in res:
            # res contains only one row
            return row[0]
