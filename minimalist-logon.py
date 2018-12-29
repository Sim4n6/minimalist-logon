from flask import Flask, url_for, render_template, session, redirect, request, flash
from db import create_db, check_credentials_correct, insert_user, check_if_already_registered
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8zZERUNdnJE'
db_name = "db_login.db"


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
	if not os.path.exists(db_name):
		create_db(db_name)

	if request.method == "GET":
		return render_template("index.html")
	elif request.method == "POST":
		if request.form["logon_btn"] == "yes_logon":
			flash("logon btn clicked")
			return redirect(url_for("login_check"))
		elif request.form["logon_btn"] == "no_register":
			flash("register clicked")
			return redirect(url_for("register_user"))
	else:
		return redirect(url_for("logout"))


@app.route('/login', methods=['POST', 'GET'])
def login_check():
	if request.method == 'GET':
		return render_template("auth/login_form.html")
	elif request.method == 'POST':
		if request.form["submit_btn"] == "new user":
			flash("Register a new user button clicked")
			return redirect(url_for("register_user"))
		elif request.form["submit_btn"] == "login":
			result = check_credentials_correct(db_name, request.form["username"], request.form["password"])
			if result:
				session['username'] = request.form['username']
				return redirect(url_for("success", userlogged=request.form['username']))
			else:
				flash('Could not connect with the typed credentials !')
				return redirect(url_for("login_check"))
	else:
		return redirect(url_for("logout"))


@app.route('/register', methods=['GET', 'POST'])
def register_user():
	if request.method == 'GET':
		return render_template("auth/register_form.html")
	elif request.method == 'POST':
		if request.form["submit_btn"] == "cancel":
			return redirect(url_for("index"))
		elif request.form["submit_btn"] == "create new user":
			# result is a a list of tuples
			result = check_if_already_registered(db_name, request.form["username"])
			print(result)
			if result[0] != (0,):
				flash('Username taken try a different one, please.')
				return redirect(url_for("register_user"))
			else:
				insert_user(db_name, request.form["username"], request.form["email"], request.form["password"])
				flash('New account created successfully.')
				return redirect(url_for("login_check"))
	else:
		return redirect(url_for("logout"))


@app.route("/success", methods=['GET', 'POST'])
def success():
	if 'username' in session:
		flash(session["username"])
		if request.method == "GET":
			return render_template("auth/success_form.html", user_logged=session['username'])
		elif request.method == "POST":
			if request.form["yes_no_btn"] == "yes":
				flash("yes btn clicked")
			elif request.form["yes_no_btn"] == "no":
				flash("no btn clicked")
			return render_template("auth/success_form.html", user_logged=session["username"])
		else:
			return redirect(url_for("logout"))
	else:
		return redirect(url_for("logout"))


@app.route('/logout')
def logout():
	session.pop('username', None)
	flash("logged out ! ")
	return redirect(url_for('index'))


if __name__ == "__main__":
	app.config["ENV"] = "development"
	app.run("127.0.0.1", "5000", debug=True)
