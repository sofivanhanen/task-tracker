from flask_wtf import FlaskForm
from wtforms import StringField, validators

class TaskForm(FlaskForm):
    name = StringField("Task name", [validators.Length(min=2, max=100)])

    class Meta:
        csrf = False
