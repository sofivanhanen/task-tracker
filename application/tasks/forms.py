from flask_wtf import FlaskForm
from wtforms import StringField, validators, BooleanField


class TaskForm(FlaskForm):
    name = StringField("Task name", [validators.Length(min=2, max=100)])

    class Meta:
        csrf = False


class EditForm(FlaskForm):
    name = StringField("Task name", [validators.Length(min=2, max=100)])
    done = BooleanField("Done")

    class Meta:
        csrf = False
