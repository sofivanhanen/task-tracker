from flask_wtf import FlaskForm
from wtforms import StringField, validators, BooleanField, IntegerField, DecimalField


class TaskForm(FlaskForm):
    name = StringField("Task name", validators=[validators.Length(
        min=2, max=100), validators.DataRequired()])
    estimate = IntegerField("Optional: Estimate time this task will take in minutes", validators=[validators.NumberRange(min=0), validators.Optional(True)])

    class Meta:
        csrf = False


class EditForm(FlaskForm):
    name = StringField("Task name", validators=[validators.Length(
        min=2, max=100), validators.DataRequired()])
    done = BooleanField("Done")
    progress = DecimalField(
        "Optional: Current progress. 1 is finished, 0.5 is halfway done", validators=[validators.NumberRange(max=1.0, min=0.0), validators.Optional(True)])

    class Meta:
        csrf = False
