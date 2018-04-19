from application import app, db, current_user
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from application.tasks.models import Task
from application.workingperiods.models import WorkingPeriod


@app.route("/stats/")
@login_required
def stats_index():
    return render_template("stats/index.html")
