from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=2, max=20)])
    password = PasswordField("Password", [validators.Length(min=2, max=20)])

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=2, max=20)])
    name = StringField("Nickname", [validators.Length(min=1, max=100)])
    password = PasswordField("Password", [validators.Length(min=2, max=20)])

    class Meta:
        csrf = False
