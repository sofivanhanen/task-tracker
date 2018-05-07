from application import app, db, current_user
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from application.tasks.models import Task
from application.workingperiods.models import WorkingPeriod
from application.stats.models import Stats


@app.route("/stats/")
@login_required
def stats_index():
    return render_template("stats/index.html", day_of_week_string=Stats.get_most_worked_day_of_week_string(), total_worked_minutes_string=Stats.get_total_worked_minutes_string(), most_worked_class_string=Stats.get_most_worked_class_string())
