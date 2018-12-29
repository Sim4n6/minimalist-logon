import sqlite3 as lite
from hashlib import sha1


def encrypt_password(password):
	""" encrypt password using sh1 and upper case the result """
	return sha1(password.encode('UTF-8')).hexdigest().upper()


def create_db(db_name_arg):
	""" intialize the database for the first time and create the table users if does not exist """
	try:
		conn0 = lite.connect(db_name_arg)
		c0 = conn0.cursor()
		c0.execute(
			'''CREATE TABLE users(employee_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, 
						email TEXT NOT NULL, password TEXT NOT NULL );''')
		conn0.commit()
	except lite.Error as e:
		conn0.rollback()
		print(e.args[0])
	finally:
		conn0.close()


def check_credentials_correct(db_name_arg, username_arg, password_arg):
	""" check whether credentials typed are correct and returns the result in a list """
	result = []
	try:
		# Establish Connection
		conn3 = lite.connect(db_name_arg)
		c3 = conn3.cursor()
		# Find user If there is any take proper action
		find_user = '''SELECT * FROM users WHERE username = ? and password = ?'''
		c3.execute(find_user, [username_arg, encrypt_password(password_arg)])
		result = c3.fetchall()
	except lite.Error as e:
		conn3.rollback()
		print(e.args[0])
	finally:
		conn3.close()

	return result


def check_if_already_registered(db_name_arg, username_arg):
	""" check whether a user is already registred and returns the result in a list of typles """
	result = []
	try:
		conn4 = lite.connect(db_name_arg)
		cursor = conn4.cursor()
		# count the number of users in the database that have the same username and uname
		num_same_user = '''SELECT COUNT(*) FROM users WHERE username = ? '''
		cursor.execute(num_same_user, [username_arg])
		result = cursor.fetchall()
	except lite.Error as e:
		conn4.rollback()
		print(e.args[0])
	finally:
		conn4.close()

	return result


def insert_user(db_name_arg, username_arg, email_arg, password_arg):
	""" insert a user with a password and a name into the database """
	try:
		# establish a connection to the database a get a cursor
		connection = lite.connect(db_name_arg)
		cursor = connection.cursor()
		# define a function for encrypting password
		connection.create_function('encrypt', 1, encrypt_password)
		# insert the user with uname and encrypted password inside the database
		insert = '''INSERT INTO users (username, email, password) VALUES(?, ?, encrypt(?))'''
		cursor.execute(insert, [username_arg, email_arg, password_arg])
		# commit the insert statement
		connection.commit()
	except lite.Error as e:
		connection.rollback()
		print(e.args[0])
	finally:
		connection.close()
