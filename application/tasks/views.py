from application import app, db, current_user
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from application.tasks.models import Task
from application.tasks.forms import TaskForm, EditForm
from application.workingperiods.models import WorkingPeriod
from sqlalchemy.sql import collate


@app.route("/tasks", methods=["GET"])
@login_required
def tasks_index():
    return render_template("tasks/list.html", tasks=Task.query.filter_by(account_id=current_user.id).order_by(Task.done.asc(), collate(Task.name, 'NOCASE')).all())


@app.route("/tasks/new/")
@login_required
def tasks_form():
    return render_template("tasks/new.html", form=TaskForm())


@app.route("/tasks/<task_id>/", methods=["GET"])
@login_required
def tasks_details(task_id):

    t = Task.query.get(task_id)
    if t.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    time = Task.get_total_time_spent_on_task(task_id)
    wps = WorkingPeriod.find_working_periods_with_string_for_task(task_id)

    return render_template("tasks/details.html", task=t, total_time=time, working_periods=wps)


@app.route("/tasks/<task_id>/", methods=["POST"])
@login_required
def tasks_set_done(task_id):

    t = Task.query.get(task_id)
    if t.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    t.done = True
    db.session().commit()

    return redirect(url_for("tasks_index"))


@app.route("/tasks/<task_id>/delete/confirm/")
@login_required
def tasks_confirm_delete(task_id):

    t = Task.query.get(task_id)
    if t.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    return render_template("tasks/delete.html", task=t)


@app.route("/tasks/<task_id>/delete/")
@login_required
def tasks_delete_task(task_id):

    t = Task.query.get(task_id)
    if t.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    wps = db.session.query(WorkingPeriod).filter(
        WorkingPeriod.task_id == task_id).all()
    for wp in wps:
        wp.task_id = None

    db.session.delete(t)
    db.session.commit()

    return redirect(url_for("tasks_index"))


@app.route("/tasks/<task_id>/edit/", methods=["GET", "POST"])
@login_required
def tasks_edit_task(task_id):

    t = Task.query.get(task_id)
    if t.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    form = EditForm(request.form)

    if request.method == "GET":
        form.name.default = t.name
        form.done.default = t.done
        form.process()
        return render_template("tasks/edit.html", form=form, task=t)

    if not form.validate():
        return render_template("tasks/edit.html", form=form, task=t)

    t.name = form.name.data
    t.done = form.done.data

    db.session().commit()

    return redirect(url_for("tasks_details", task_id=task_id))


@app.route("/tasks/", methods=["POST"])
@login_required
def tasks_create():
    form = TaskForm(request.form)

    if not form.validate():
        return render_template("tasks/new.html", form=form)

    t = Task(form.name.data)
    t.account_id = current_user.id

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("tasks_index"))
