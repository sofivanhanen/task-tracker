from flask_wtf import FlaskForm
from wtforms import StringField, validators, BooleanField


class TaskForm(FlaskForm):
    name = StringField("Task name", validators=[validators.Length(
        min=2, max=100), validators.DataRequired()])

    class Meta:
        csrf = False


class EditForm(FlaskForm):
    name = StringField("Task name", validators=[validators.Length(
        min=2, max=100), validators.DataRequired()])
    done = BooleanField("Done")

    class Meta:
        csrf = False
