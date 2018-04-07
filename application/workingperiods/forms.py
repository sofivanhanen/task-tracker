from flask_wtf import FlaskForm
from wtforms import validators, IntegerField, DecimalField, DateTimeField, SelectField


class WorkingPeriodForm(FlaskForm):

    time = DateTimeField("Date and time started, input in form 1.10.2013 15:20", format="%d.%m.%Y %H:%M")
    length = IntegerField("Length of session in minutes", validators=[
                          validators.InputRequired(), validators.NumberRange(min=0)])
    quality = DecimalField(
        "Estimated quality of the session. 1.0 is excellent, 0.5 is average", validators=[validators.NumberRange(max=1.0, min=0.0), validators.Optional(True)])

    task = SelectField("Task", coerce=int, validators=[validators.InputRequired()])

    class Meta:
        csrf = False
