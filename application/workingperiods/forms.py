from flask_wtf import FlaskForm
from wtforms import validators, IntegerField, DecimalField, DateTimeField


class WorkingPeriodForm(FlaskForm):

    time = DateTimeField("Date and time started")
    length = IntegerField("Length of session in minutes")
    quality = DecimalField("Estimated quality of the session. 1.0 is excellent, 0.5 is average")

    class Meta:
        csrf = False
