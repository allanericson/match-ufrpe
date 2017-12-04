from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db, lm
from validate_email import validate_email

from app.models.tables import User
from app.models.forms import LoginForm


@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data, form.name.data, form.email.data )
        query = User.query.filter_by(username=form.username.data).first()
        addr = form.email.data.split('@')
        if addr[1] == 'ufrpe.br':
            if query is None:
                db.session.add(user)
                db.session.commit()
                flash("Voce foi cadastrado")
                return redirect(url_for("index"))
            else:
                flash("Usuario ja cadastrado")
                return redirect(url_for("signup"))
        else:
            flash("Endereço de email invalido.")
            return redirect(url_for('signup'))
    else:
        print(form.errors)
    return render_template("signup.html", form=form)
@app.route("/login", methods=['get' , 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user == None:
            flash("Usuario não cadastrado")
            redirect(url_for("index"))
        else:
            if form.password.data == user.password:
                login_user(user)
                flash("Logged in.")
                return redirect(url_for("index"))
            else:
                flash("Invalid Login.")
                redirect(url_for("index"))
    else:
        print(form.errors)
    
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))

@app.route("/teste")
def teste():
    i = User.query.filter_by(username="pedro").first()
    db.session.delete(i)
    db.session.commit()
    return "OK"
    