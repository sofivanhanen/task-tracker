from application import app, db, current_user
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from application.classes.models import Class
from application.classes.forms import ClassForm

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

    return redirect(url_for("index"))
