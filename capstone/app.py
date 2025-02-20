from flask import Flask, render_template, json, jsonify, request, redirect, session, url_for
import pymysql
import os
import database.db_connector as db

# Configuration
app = Flask(__name__)
app.secret_key = 'secretsecretsecret'
# app.config['SESSION_TYPE'] = 'filesystem'
db_connection = db.connect_to_database()
cursor = db_connection.cursor(pymysql.cursors.DictCursor)


# Routes
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	if request.method == 'POST' and 'accountUsername' in request.form and 'password' in request.form:
		accountUsername = request.form['accountUsername']
		password = request.form['password']
		query = 'SELECT * FROM Accounts WHERE accountUsername = %s AND accountPassword = %s'
		# Citation: https://stackoverflow.com/a/47957611/18182802
		inputs = (accountUsername, password)
		cursor.execute(query, inputs)
		user = cursor.fetchone()
		if user:
			session['loggedin'] = True
			session['accountID'] = user['accountID']
			session['accountUsername'] = user['accountUsername']
			session['accountFirstName'] = user['accountFirstName']
			session['accountLastName'] = user['accountLastName']
			session['accountTeamID'] = user['accountTeamID']
			session['accountRole'] = user['accountRole']
			screenMsg = 'Logged in successfully !'
			return redirect(url_for('main'))
		else:
			screenMsg = 'Please enter correct username / password!'
		return render_template('login.j2', screenMsg = screenMsg)
	return render_template("login.j2")

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('accountID', None)
	session.pop('accountUsername', None)
	session.pop('accountFirstName', None)
	session.pop('accountLastName', None)
	session.pop('accountTeamID', None)
	session.pop('accountRole', None)
	session.pop('accountPassword', None)
	return redirect(url_for('login'))

@app.route('/main', methods=['GET', 'POST'])
def main():
	return render_template("main.j2", accountFirstName=session['accountFirstName'])

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
	if request.method == "GET":
		if 'loggedin' not in session or not session['loggedin']:
			screenMsg = 'Please login to continue'
			return render_template('login.j2', screenMsg = screenMsg)
		# query = 'SELECT * FROM Projects'					# [Vish]: Uncomment to use without parameters
		queryUserTasks = """
		SELECT * FROM Tasks t
		JOIN Accounts a ON t.taskAssignee=a.accountID
		WHERE t.taskAssignee = %s
		"""

		userInputs = (session['accountID'])
		queryTeamTasks = """
		SELECT * FROM Tasks t
		JOIN Accounts a ON t.taskAssignee=a.accountID
		JOIN AccountTeams at ON  a.accountTeamID=at.accountTeamID
		WHERE a.accountTeamID = %s
		"""

		teamInputs = (session['accountTeamID'])
		cursor.execute(queryUserTasks, userInputs)
		userTasksFetch = cursor.fetchall()
		cursor.execute(queryTeamTasks, teamInputs)
		teamTasksFetch = cursor.fetchall()
		# cursor.execute(query)  									# [Vish]: Uncomment to use without parameters

		if userTasksFetch and teamTasksFetch:
			# screenMsg = json.dumps(userTasksFetch)				# [Vish]: Uncomment to get json of query
			screenMsg = f"Printing Tasks for account {session['accountUsername']}"
			return render_template('tasks.j2', screenMsg = screenMsg, accountUsername = session['accountUsername'], userTasks = userTasksFetch, teamTasks = teamTasksFetch)
		else:
			screenMsg = 'Please enter correct username and password'
			return render_template('login.j2', screenMsg = screenMsg)

	if request.method == "POST":
		if request.form.get("addTaskSubmit"):
			tAssignee = request.form["tAssignee"]
			tAssignedDate = request.form["tAssignedDate"]
			tDueDate = request.form["tDueDate"]
			tStatus = request.form["tStatus"]
			tSprint = request.form["tSprint"]
			tSubject = request.form["tSubject"]

			query = "INSERT INTO Tasks (taskAssignee, taskAssigned, taskDue, taskStatus, taskSprint, taskSubject) VALUES (%s, %s,%s,%s, %s, %s)"
			cursor.execute(query, (tAssignee, tAssignedDate, tDueDate, tStatus, tSprint, tSubject ))
			cursor.connection.commit()

			# redirect back to people page
			return redirect("/tasks")
	else:
		return render_template("tasks.j2")

@app.route('/help', methods=['GET', 'POST'])
def help():
	return render_template("help.j2")

@app.route('/projects', methods=['GET', 'POST'])
def projects():
	if 'loggedin' not in session or not session['loggedin']:
		screenMsg = 'Please login to continue'
		return render_template('login.j2', screenMsg = screenMsg)

	if request.method == 'POST':
		if 'createProject' in request.form:
			projectName = request.form['projectName']
			projectStart = request.form['projectStart']
			projectEnd = request.form['projectEnd']
			projectStatus = request.form['projectStatus']
			accountTeamID = session['accountTeamID']

			insert_query = """
		    INSERT INTO Projects (projectName, projectStart, projectEnd, accountTeamID, projectStatus) 
		    VALUES (%s, %s, %s, %s, %s)
		    """
			cursor.execute(insert_query, (projectName, projectStart, projectEnd, accountTeamID, projectStatus))
			db_connection.commit()

		elif 'editProject' in request.form:
			projectID = request.form['projectID']
			projectName = request.form['projectName']
			projectStart = request.form['projectStart']
			projectEnd = request.form['projectEnd']

			update_query = """
					UPDATE Projects 
					SET projectName = %s, projectStart = %s, projectEnd = %s 
					WHERE projectID = %s AND accountTeamID = %s
					"""
			cursor.execute(update_query, (projectName, projectStart, projectEnd, projectID, session['accountTeamID']))
			db_connection.commit()

		elif 'deleteProject' in request.form:
			projectID = request.form['projectID']
			delete_query = "DELETE FROM Projects WHERE projectID = %s AND accountTeamID = %s"
			cursor.execute(delete_query, (projectID, session['accountTeamID']))
			db_connection.commit()

		elif 'updateStatus' in request.form:
			projectID = request.form['projectID']
			newStatus = request.form['projectStatus']

			update_query = """
		    UPDATE Projects 
		    SET projectStatus = %s 
		    WHERE projectID = %s AND accountTeamID = %s
		    """
			cursor.execute(update_query, (newStatus, projectID, session['accountTeamID']))
			db_connection.commit()

		return redirect(url_for('projects'))

	# query = 'SELECT * FROM Projects'					# [Vish]: Uncomment to use without parameters
	query = 'SELECT * FROM Projects WHERE accountTeamID = %s'

	inputs = (session['accountTeamID'])

	cursor.execute(query, inputs)
	# cursor.execute(query)  							# [Vish]: Uncomment to use without parameters

	# projects = cursor.fetchone()  					# [Vish]: Uncomment to get single record in query
	# projects = json.dumps(cursor.fetchall()) 			# [Vish]: Uncomment to get json of query
	projects = cursor.fetchall()
	if projects:
		# screenMsg = json.dumps(projects)				# [Vish]: Uncomment to get json of query
		screenMsg = f"Printing Projects for accountTeamID {session['accountTeamID']}"
		return render_template('projects.j2', screenMsg = screenMsg, accountUsername = session['accountUsername'], projects = projects)
	else:
		screenMsg = 'Please enter correct username and password'
		return render_template('login.j2', screenMsg = screenMsg)

@app.route('/account_creation', methods=['GET', 'POST'])
def accountCreation():
	query = "SELECT * FROM Accounts;"
	cursor = db.execute_query(db_connection=db_connection, query=query)
	results = cursor.fetchall()
	# results = json.dumps(cursor.fetchall())
	# return results
	if request.method == "POST":
		if request.form.get("addAccountSubmit"):
			accountUsername = request.form["accountUsername"]
			accountFirstName = request.form["accountFirstName"]
			accountLastName = request.form["accountLastName"]
			accountPassword = request.form["accountPassword"]
			accountTeamID = request.form["accountTeamID"]
			accountRole = request.form["accountRole"]
			
			query = "INSERT INTO Accounts (accountUsername, accountFirstName, accountLastName, accountPassword, accountTeamID, accountRole) VALUES (%s, %s, %s, %s, %s, %s)"
			cursor.execute(query, (accountUsername, accountFirstName, accountLastName, accountPassword, accountTeamID, accountRole ))
			cursor.connection.commit()

			# redirect back to people page
			return redirect(url_for('login'))

	return render_template("account_creation.j2", data = results)

@app.route('/accounts', methods=['GET', 'POST'])
def accountAdmin():
	query = "SELECT * FROM Accounts;"
	cursor = db.execute_query(db_connection=db_connection, query=query)
	results = cursor.fetchall()
	# results = json.dumps(cursor.fetchall())
	# return results
	if request.method == "POST":
		if request.form.get("addAccountSubmit"):
			accountUsername = request.form["accountUsername"]
			accountFirstName = request.form["accountFirstName"]
			accountLastName = request.form["accountLastName"]
			accountPassword = request.form["accountPassword"]
			accountTeamID = request.form["accountTeamID"]
			accountRole = request.form["accountRole"]
			
			query = "INSERT INTO Accounts (accountUsername, accountFirstName, accountLastName, accountPassword, accountTeamID, accountRole) VALUES (%s, %s, %s, %s, %s, %s)"
			cursor.execute(query, (accountUsername, accountFirstName, accountLastName, accountPassword, accountTeamID, accountRole ))
			cursor.connection.commit()

			# redirect back to people page
			return redirect("/accounts")

	return render_template("accounts.j2", data = results)

@app.route("/delete_account/<int:id>")
def delete_account(id):
	print("Delete Account Reached")
	# mySQL query to delete the person with our passed id
	query = "DELETE FROM Accounts WHERE accountID = '%s';"
	cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id))
	results = cursor.fetchall()

	return redirect("/accounts")

# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_accounts/<int:accountID>", methods=["POST", "GET"])
def edit_accounts(accountID):
	print("here")
	if request.method == "GET":
		query = "SELECT * FROM Accounts WHERE accountID = %s" % (accountID)
		cursor = db.execute_query(db_connection=db_connection, query=query)
		data = cursor.fetchall()

		return render_template("edit_accounts.j2", data=data)


@app.route("/update_account", methods=["POST"])
def update_account():
	# grab account form inputs
	accountID = request.form["accountID"]
	accountUsername = request.form["accountUsername"]
	accountFirstName = request.form["accountFirstName"]
	accountLastName = request.form["accountLastName"]
	accountPassword = request.form["accountPassword"]
	accountTeamID = request.form["accountTeamID"]
	accountRole = request.form["accountRole"]

	query = "UPDATE Accounts SET accountUsername = %s, accountFirstName = %s, accountLastName = %s, accountPassword = %s, accountTeamID = %s, accountRole = %s WHERE accountID = %s"
	print(query)
	cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(accountUsername, accountFirstName, accountLastName, accountPassword, accountTeamID, accountRole, accountID ))
	cursor.connection.commit()

	# redirect back to people page
	return redirect("/accounts")


# Listener
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 9112))
	app.run(port=port, debug=True)
