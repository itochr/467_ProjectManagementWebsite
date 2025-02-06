from flask import Flask, render_template, json, jsonify, request, redirect, session, url_for
import pymysql
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
app.secret_key = 'sadfadsgdsfhs'
# app.config["SESSION_PERMANENT"] = True
# app.config["PERMANENT_SESSION_LIFETIME"] = 300
app.config['SESSION_TYPE'] = 'filesystem'



db_connection = db.connect_to_database()
cursor = db_connection.cursor(pymysql.cursors.DictCursor)


# Routes
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	screenMsg = ''
	if request.method == 'POST' and 'accountUsername' in request.form and 'password' in request.form:
		accountUsername = request.form['accountUsername']
		password = request.form['password']
		query = 'SELECT * FROM Accounts WHERE accountUsername = %s AND accountPassword = %s'

		# Citation: https://stackoverflow.com/a/47957611/18182802
		inputs = (accountUsername, password)
		cursor.execute(query, inputs)
		user = cursor.fetchone()

		# results = json.dumps(cursor.fetchone())
		# return results
		if user:
			session['loggedin'] = True
			session['accountID'] = user['accountID']
			session['accountUsername'] = user['accountUsername']
			# session['accountFirstName'] = user['accountFirstName']
			screenMsg = 'Logged in successfully !'
			accountFirstName = user['accountFirstName']
			return render_template('main.j2', accountFirstName = accountFirstName)
		else:
			screenMsg = 'Please enter correct username / password!'
		return render_template('login.j2', screenMsg = screenMsg)
	return render_template("login.j2")

@app.route('/main', methods=['GET', 'POST'])
def main():
	return render_template("main.j2")

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
	return render_template("tasks.j2")

@app.route('/help', methods=['GET', 'POST'])
def help():
	return render_template("help.j2")

@app.route('/projects', methods=['GET', 'POST'])
def projects():
	screenMsg = ''
	if request.method == 'POST' and 'accountUsername' in request.form and 'password' in request.form:
		accountUsername = request.form['accountUsername']
		password = request.form['password']
		query = 'SELECT * FROM Accounts WHERE accountUsername = %s AND accountPassword = %s'

		# Citation: https://stackoverflow.com/a/47957611/18182802
		inputs = (accountUsername, password)
		cursor.execute(query, inputs)
		user = cursor.fetchone()

		# results = json.dumps(cursor.fetchone())
		# return results
		if user:
			session['loggedin'] = True
			session['accountID'] = user['accountID']
			session['accountUsername'] = user['accountUsername']
			# session['accountFirstName'] = user['accountFirstName']
			screenMsg = 'Logged in successfully !'
			accountFirstName = user['accountFirstName']
			return render_template('main.j2', accountFirstName = accountFirstName)
		else:
			screenMsg = 'Please enter correct username / password!'
		return render_template('login.j2', screenMsg = screenMsg)
	return render_template("projects.j2")

@app.route('/accounts', methods=['GET', 'POST'])
def accountAdmin():
	query = "SELECT * FROM Accounts;"
	cursor = db.execute_query(db_connection=db_connection, query=query)
	results = cursor.fetchall()
	# results = json.dumps(cursor.fetchall())
	# return results
	return render_template("accounts.j2", accounts = results)


# Listener
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 9112))
	app.run(port=port, debug=True)
