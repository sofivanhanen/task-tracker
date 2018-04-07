from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.tasks.models import Task
from application.workingperiods.forms import WorkingPeriodForm


@app.route("/workingperiods/new", methods=["GET", "POST"])
@login_required
def working_periods_new():

    form = WorkingPeriodForm(request.form)
    tasks = Task.query.filter_by(account_id=current_user.id).all()
    form.task.choices = [(task.id, task.name) for task in tasks]

    if request.method == "GET":
        return render_template("workingperiods/new.html", form=form)

    if not form.validate():
        return render_template("workingperiods/new.html", form=form)

    return redirect(url_for("index"))
