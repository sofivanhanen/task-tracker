from application import app, db, current_user
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from application.tasks.models import Task
from application.workingperiods.forms import WorkingPeriodForm
from application.workingperiods.models import WorkingPeriod


@app.route("/workingperiods/new/", methods=["GET", "POST"])
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

    t = Task.query.get(form.task.data)
    if t.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    wp.task_id = form.task.data

    # If progress was given
    if form.progress.data != None:
        t.progress = form.progress.data

    db.session().add(wp)
    db.session().commit()

    return redirect(url_for("tasks_details", task_id=wp.task_id))

@app.route("/workingperiods/<wp_id>/delete/confirm")
@login_required
def working_periods_delete_confirm(wp_id):

    wp = WorkingPeriod.query.get(wp_id)

    t = Task.query.get(wp.task_id)
    if t.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    return render_template("workingperiods/delete.html", wp=wp)

@app.route("/workingperiods/<wp_id>/delete/")
@login_required
def working_periods_delete(wp_id):

    wp = WorkingPeriod.query.get(wp_id)

    t = Task.query.get(wp.task_id)
    if t.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    db.session.delete(wp)
    db.session.commit()

    return redirect(url_for("tasks_details", task_id=t.id))
