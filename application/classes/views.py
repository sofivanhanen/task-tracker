from application import app, db, current_user
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from application.classes.models import Class
from application.classes.forms import ClassForm


@app.route("/classes/")
@login_required
def classes_index():

    classes = Class.query.filter_by(account_id=current_user.id).all()

    for c in classes:
        c.set_count()

    return render_template("classes/list.html", classes=classes)


@app.route("/classes/new/", methods=["GET", "POST"])
@login_required
def classes_new():

    form = ClassForm(request.form)

    if request.method == "GET":
        return render_template("classes/new.html", form=ClassForm())

    if not form.validate:
        return render_template("classes/new.html", form=form)

    c = Class(form.name.data)
    c.account_id = current_user.id

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("classes_details", class_id=c.id))


@app.route("/classes/<class_id>/")
@login_required
def classes_details(class_id):

    c = Class.query.get(class_id)
    if c.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    c.set_count()

    return render_template("classes/details.html", c=c)


@app.route("/classes/<class_id>/delete/confirm/")
@login_required
def classes_confirm_delete(class_id):

    c = Class.query.get(class_id)
    if c.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    return render_template("classes/delete.html", c=c)


@app.route("/classes/<class_id>/delete/")
@login_required
def classes_delete_class(class_id):

    c = Class.query.get(class_id)
    if c.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    # Deleting relationships to tasks
    c.tasks = []
    # Deleting the class object
    db.session().delete(c)
    db.session().commit()

    return redirect(url_for("classes_index"))

@app.route("/classes/<class_id>/edit/", methods=["GET", "POST"])
@login_required
def classes_edit_class(class_id):

    c = Class.query.get(class_id)

    if c.account_id != current_user.id:
        return redirect(url_for("auth_unauthorized"))

    form = ClassForm(request.form)

    if request.method == "GET":
        form.name.default = c.name
        form.process()
        return render_template("classes/edit.html", form=form, c=c)

    if not form.validate():
        return render_template("classes/edit.html", form=form, c=c)

    c.name = form.name.data
    db.session().commit()

    return redirect(url_for("classes_details", class_id=class_id))
