from flask_wtf import FlaskForm
from wtforms import validators, StringField


class ClassForm(FlaskForm):
    name = StringField("Name", validators=[validators.Length(min=2, max=100), validators.DataRequired()])

    class Meta:
        csrf = False
