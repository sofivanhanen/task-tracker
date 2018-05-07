from application import app, db, current_user
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from application.tasks.models import Task
from application.tasks.forms import EditForm, TaskFormBase
from application.classes.models import Class
from application.workingperiods.models import WorkingPeriod
from sqlalchemy.sql import collate
from sqlalchemy import func
import logging
from wtforms import BooleanField


@app.route("/tasks/", defaults={'page': 1})
@app.route("/tasks/page/<int:page>/")
@login_required
def tasks_index(page):
    per_page = 5
    tasks = Task.query.filter_by(account_id=current_user.id).order_by(
        Task.progress.asc(), func.lower(Task.name)).paginate(page, per_page, error_out=False)
    return render_template("tasks/list.html", tasks=tasks)


@app.route("/tasks/new/", methods=["GET", "POST"])
@login_required
def tasks_new():
    form = TaskFormBase(request.form)

    # Just for the record, I have no idea what I'm doing here
    # This is apparently how you get a custom number of fields
    # But I have no idea how to make a new version of the same form in case of failure
    class TaskForm(TaskFormBase):
        pass

    classes = Class.query.filter_by(account_id=current_user.id).all()
    for c in classes:
        setattr(TaskForm, str(c.id), BooleanField(c.name))

    # For some reason this doesn't copy errors
    new = TaskForm()
    new.name = form.name
    new.estimate = form.estimate

    # ...but this works anyhow
    if not new.validate():
        return render_template("tasks/new.html", form=new)

    t = Task(new.name.data)
    t.account_id = current_user.id
    t.estimate = (new.estimate.data)

    # Checking which classes were selected
    for field in new:
        try:
            # If short_name is int, this does not throw error and it is a booleanfield describing a class with the id short_name
            c = Class.query.get(int(field.short_name))
            if (field.data):
                t.classes.append(c)
        except ValueError:
            pass

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("tasks_details", task_id=t.id))


@app.route("/tasks/<task_id>/", methods=["GET"])
@login_required
def tasks_details(task_id):

    t = Task.query.get(task_id)
    if t.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    time = Task.get_total_time_spent_on_task(task_id)
    wps = WorkingPeriod.query.filter_by(task_id=task_id)

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
        form.progress.default = t.progress
        form.process()
        return render_template("tasks/edit.html", form=form, task=t)

    if not form.validate():
        return render_template("tasks/edit.html", form=form, task=t)

    t.name = form.name.data
    t.done = form.done.data
    if not t.done:
        t.progress = form.progress.data
    else:
        t.progress = 1.0

    db.session().commit()

    return redirect(url_for("tasks_details", task_id=task_id))
