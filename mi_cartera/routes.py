from mi_cartera import app
from mi_cartera.models import Movement, MovementDAOsqlite
from flask import render_template, request, redirect, flash, url_for
from mi_cartera.forms import MovementForm, RegisterForm

dao = MovementDAOsqlite(app.config.get("PATH_SQLITE"))

@app.route("/")
def index():
    try:
        movements = dao.get_all()
        return render_template("index.html", the_movements=movements, title="Todos")
    except ValueError as e:
        flash("Su fichero de datos está corrupto")
        flash(str(e))
        return render_template("index.html", the_movements=[], title="Todos")


@app.route("/new_movement", methods=["GET", "POST"])
def new_mov():
    form = MovementForm()
    if request.method == "GET":
        return render_template("new.html", the_form = form, title="Alta de movimiento")
    else:
        if form.validate():
            try:
                dao.insert(Movement(str(form.date.data), form.abstract.data,
                                    form.amount.data, form.currency.data))
                return redirect("/")
            except ValueError as e:
                flash(str(e))
                return render_template("new.html", the_form=form, title="Alta de movimiento")
        else:
            return render_template("new.html", the_form=form, title="Alta de movimiento")

      

@app.route("/update_movement/<int:pos>", methods=["GET", "POST"])
def upd_mov(pos):
    if request.method == "GET":
        mov = dao.get(pos)
        if mov:
            return render_template("update.html", title="Modificación de movimiento",
                                the_form=mov, pos=pos)
        else:
            flash(f"Registro {pos} inexistente")
            return redirect(url_for("index"))
    else:
        data = request.form
        try:
            mv = Movement(data["date"], data["abstract"],
                                data["amount"], data["currency"])
            dao.update(pos, mv)
            return redirect(url_for("index"))
        except ValueError as e:
            flash(str(e))
            return render_template("update.html", the_form=data, title="Modificación de movimiento")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "GET":
        return render_template("example.html", the_form = form)
    else:
        if form.validate():
            flash("Login correcto")
            return redirect(url_for("index"))
        else:
            return render_template("example.html", the_form=form)
