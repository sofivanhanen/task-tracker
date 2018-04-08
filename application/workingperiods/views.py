from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.tasks.models import Task
from application.workingperiods.forms import WorkingPeriodForm
from application.workingperiods.models import WorkingPeriod


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

    wp = WorkingPeriod(form.time.data, form.length.data, form.quality.data)
    wp.task_id = form.task.data

    db.session().add(wp)
    db.session().commit()

    return redirect(url_for("index"))
