from flask import Flask, url_for, render_template, session, redirect, request, flash
import sqlite3 as lite
from hashlib import sha1
import db

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8zZERUNdnJE'
db_name = "shifts.db"


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
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
	# if 'username' in session:
	#   return render_template("success_form.html", user_logged=session["username"])
	# return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def login_check():
	if request.method == 'POST':
		if request.form["submit_btn"] == "new user":
			return redirect(url_for("register_user"))
		else:
			try:
				# Establish Connection
				conn3 = lite.connect(db_name)
				c3 = conn3.cursor()
				# Find user If there is any take proper action
				find_user = '''SELECT * FROM users WHERE username = ? and password = ?'''
				c3.execute(find_user, [request.form["username"], encrypt_password(request.form["password"])])
				result = c3.fetchall()
				app.logger.debug("----" + str(result))
				if result:
					session['username'] = request.form['username']
					return render_template("auth/success_form.html", user_logged=request.form["username"])
				else:
					flash('could not connect !')
			except lite.Error as e:
				conn3.rollback()
				app.logger.error("An error occurred : ", e.args[0])
			finally:
				conn3.close()
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
		is_stay = True
		try:
			conn4 = lite.connect(db_name)
			c4 = conn4.cursor()
			# Find Existing username if any take proper action
			find_user = '''SELECT DISTINCT username, name FROM user WHERE username = ? and name = ? '''
			c4.execute(find_user, [request.form["username"], request.form["name"]])
			if c4.fetchall():
				flash('Username taken try a different one, please.')
				is_stay = True
			else:
				# defined a function for encrypting password
				conn4.create_function('encrypt', 1, encrypt_password)
				# Create New Account
				insert = '''INSERT INTO users (username, name, password) VALUES(?, ?, encrypt(?))'''
				c4.execute(insert, [request.form["username"], request.form["name"], request.form["password"]])
				conn4.commit()
				flash('new account created successfully ')
				is_stay = False
		except lite.Error as e:
			conn4.rollback()
			app.logger.error("An error occurred : " + e.args[0])
			flash('an error occurred')
		finally:
			conn4.close()
			if is_stay:
				return redirect(url_for("register_user"))
			else:
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


def encrypt_password(password):
	return sha1(password.encode('UTF-8')).hexdigest().upper()


if __name__ == "__main__":
	app.config["ENV"] = "development"
	app.run("127.0.0.1", "5000", debug=True)
