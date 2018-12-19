from flask import Flask, url_for, render_template, session, redirect, request, flash
from db import initialize_db, check_credentials_correct, insert_user, check_if_already_registered

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8zZERUNdnJE'
db_name = "shifts.db"


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
	initialize_db(db_name)  # TODO keep it temporairement
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

	# initialize_db(db_name)
	# if 'username' in session: # TODO another check to implement in preference in login.page
	#   return render_template("success_form.html", user_logged=session["username"])
	# return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def login_check():
	if request.method == 'POST':
		if request.form["submit_btn"] == "new user":
			return redirect(url_for("register_user"))
		elif request.form["submit_btn"] == "login":
			result = check_credentials_correct(db_name, request.form["username"], request.form["password"])
			if result:
				session['username'] = request.form['username']
				return render_template("auth/success_form.html", user_logged=request.form["username"])
			else:
				flash('could not connect !')
				return redirect(url_for("login_check"))
	elif request.method == 'GET':
		return render_template("auth/login_form.html")
	else:
		return "a request has been made from a client to server : asking for something"


@app.route('/register', methods=['GET', 'POST'])
def register_user():
	if request.method == 'GET':
		return render_template("auth/register_form.html")
	elif request.method == 'POST':
		result = check_if_already_registered(db_name, request.form["username"], request.form["name"])
		if result:
			flash('Username taken try a different one, please.')
			return redirect(url_for("register_user"))
		else:
			insert_user(db_name, request.form["username"], request.form["name"], request.form["password"])
			flash('new account created successfully ')
			return redirect(url_for("login_check"))
	else:
		return "else request method "


@app.route("/success", methods=['GET', 'POST'])
def success():
	if 'username' in session:
		if request.method == "GET":
			return render_template("success_form.html", user_logged=session["username"])
		elif request.method == "POST":
			if request.form["yes_no_btn"] == "yes":
				flash("yes clicked")
			elif request.form["yes_no_btn"] == "no":
				flash("no clicked")
			return render_template("auth/success.html", user_logged=session["username"])
		else:
			return redirect(url_for("logout"))
	else:
		return redirect(url_for("logout"))


@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))


if __name__ == "__main__":
	app.config["ENV"] = "development"
	app.run("127.0.0.1", "5000", debug=True)
