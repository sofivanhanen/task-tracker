from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# Many-to-many relationship table between tasks and classes
classtask = db.Table('classtask',
                     db.Column('class_id', db.Integer, db.ForeignKey(
                         'class.id')),
                     db.Column('task_id', db.Integer, db.ForeignKey('task.id')))

from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

from application import views

from application.tasks import models
from application.tasks import views

from application.auth import models
from application.auth import views

from application.workingperiods import models
from application.workingperiods import views

from application.auth.models import User

from application.stats import views

from application.classes import models
from application.classes import views


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


try:
    db.create_all()
except:
    pass
