from flask import Flask, render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User

# ---------- Display Routes ----------

@app.route('/')
def index():
    if "user_id" in session:
        return redirect('/dashboard')
    return render_template("reg_log.html")

# ---------- Action Routes ----------

@app.route('/users/create', methods = ["POST"])
def create_user():
    if User.registration_validator(request.form):
        session["user_id"] = User.create(request.form)
    return redirect('/')

@app.route('/login', methods = ["POST"])
def login():
    if not User.login_validator(request.form):
        flash("Invalid Login", "login")
        return redirect('/')
    user = User.get_by_email(request.form)
    session["user_id"] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')