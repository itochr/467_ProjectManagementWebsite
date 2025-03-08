from flask import Flask, render_template, json, jsonify, request, redirect, session, url_for
import pymysql
import os
import database.db_connector as db

# Configuration
app = Flask(__name__)
app.secret_key = 'secretsecretsecret'
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
		queryUserTasks = """
		SELECT * FROM Tasks t
		JOIN Accounts a ON t.taskAssignee=a.accountID
		JOIN Statuses stat on t.taskStatus=stat.statusID
		JOIN Sprints sp on t.taskSprint=sp.sprintID
		JOIN Projects p on t.taskProject=p.projectID
		WHERE t.taskAssignee = %s
		"""
		userInputs = (session['accountID'])
		queryTeamTasks = """
		SELECT * FROM Tasks t
		JOIN Accounts a ON t.taskAssignee=a.accountID
		JOIN AccountTeams at ON  a.accountTeamID=at.accountTeamID
		JOIN Statuses stat on t.taskStatus=stat.statusID
		JOIN Sprints sp on t.taskSprint=sp.sprintID
		JOIN Projects p on t.taskProject=p.projectID
		WHERE a.accountTeamID = %s
		"""
		# Get Statuses
		queryStatuses = 'SELECT * FROM Statuses'
		teamInputs = (session['accountTeamID'])
		# Get User Tasks
		cursor.execute(queryUserTasks, userInputs)
		userTasksFetch = cursor.fetchall()
		# Get Team Tasks
		cursor.execute(queryTeamTasks, teamInputs)
		teamTasksFetch = cursor.fetchall()
		cursor.execute(queryStatuses)
		statusFetch = cursor.fetchall()
		# Get Team Members
		queryTeamMembers = 'SELECT * FROM Accounts WHERE accountTeamID = %s'
		cursor.execute(queryTeamMembers, teamInputs)
		teamMemberFetch = cursor.fetchall()
		# Get Team Projects
		queryTeamProjects = 'SELECT * FROM Projects WHERE accountTeamID = %s'
		cursor.execute(queryTeamProjects, teamInputs)
		teamProjects = cursor.fetchall()
		# Get Team Sprints
		queryTeamSprints = 'SELECT * FROM Sprints WHERE accountTeamID = %s'
		cursor.execute(queryTeamSprints, teamInputs)
		sprintsFetch = cursor.fetchall()
		# Render Page if DB queries execute
		if userTasksFetch and teamTasksFetch:
			screenMsg = f"Printing Tasks for account {session['accountUsername']}"
			return render_template('tasks.j2',
						  screenMsg = screenMsg,
						  userAccountID = session['accountID'],
						  accountUsername = session['accountUsername'],
						  accountFirstName = session['accountFirstName'],
						  accountLastName = session['accountLastName'],
						  userTasks = userTasksFetch,
						  teamTasks = teamTasksFetch,
						  statuses = statusFetch,
						  team = teamMemberFetch,
						  projects = teamProjects,
						  teamSprints = sprintsFetch)
		else:
			screenMsg = 'Please enter correct username and password'
			return render_template('login.j2', screenMsg = screenMsg)
	if request.method == "POST":
		if 'addTaskSubmit' in request.form:
			tAssignee = request.form["tAssignee"]
			tAssignedDate = request.form["tAssignedDate"]
			tDueDate = request.form["tDueDate"]
			tStatus = request.form["tStatus"]
			tSprint = request.form["tSprint"]
			tProject = request.form["tProject"]
			tSubject = request.form["tSubject"]
			tDescription = request.form["tDescription"]
			# Task Query for Insert
			query = """
			INSERT INTO Tasks
			(taskAssignee, taskAssigned, taskDue, taskStatus,
			taskSprint, taskProject, taskSubject, taskDescription)
			VALUES (%s, %s,%s,%s, %s, %s, %s, %s)"""
			cursor.execute(query, (tAssignee, tAssignedDate, tDueDate, tStatus, tSprint, tProject, tSubject, tDescription))
			cursor.connection.commit()
			return redirect(url_for('tasks'))
		# Task Query for Update
		elif 'updateTask' in request.form:
			taskID = request.form['taskID']
			taskAssignee = request.form["taskAssignee"]
			taskAssigned = request.form["taskAssigned"]
			taskDue = request.form["taskDue"]
			taskStatus = request.form["taskStatus"]
			taskSprint = request.form["taskSprint"]
			taskProject = request.form["taskProject"]
			taskSubject = request.form["taskSubject"]
			taskDescription = request.form["taskDescription"]
			update_query = """
                UPDATE Tasks
                SET taskAssignee = %s, taskAssigned = %s, taskDue = %s,
				taskStatus = %s, taskSprint = %s, taskProject = %s,
				taskSubject = %s, taskDescription = %s
                WHERE taskID = %s
                """
			cursor.execute(update_query,(taskAssignee, taskAssigned, taskDue, taskStatus, taskSprint, taskProject, taskSubject, taskDescription, taskID))
			cursor.connection.commit()
			return redirect(url_for('tasks'))
		# Task Query for Delete
		elif 'deleteTask' in request.form:
			taskID = request.form['taskID']
			delete_query = "DELETE FROM Tasks WHERE taskID = %s"
			cursor.execute(delete_query, taskID)
			cursor.connection.commit()
			return redirect(url_for('tasks'))
	else:
		return redirect(url_for('tasks'))

# Route to update Task based on Drag & Drop
@app.route("/updateTaskStatus", methods=['GET', 'POST'])
def update_task_status():
	try:
		# Parse JSON request
		data = request.get_json()
		taskID = data.get("taskID")
		taskStatus = data.get("taskStatus")
		# Validate request data
		if not taskID or not taskStatus:
			return jsonify({"error": "Missing taskID or taskStatus"}), 400
		query = "UPDATE Tasks SET taskStatus = %s WHERE taskID = %s"
		cursor.execute(query, (taskStatus, taskID))
		cursor.connection.commit()
		return jsonify({"message": "Task status update success", "taskID": taskID, "newStatus": taskStatus}), 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@app.route('/help', methods=['GET', 'POST'])
def help():
	return render_template("help.j2", accountID=session['accountID'])

@app.route('/projects', methods=['GET', 'POST'])
def projects():
	if 'loggedin' not in session or not session['loggedin']:
		screenMsg = 'Please login to continue'
		return render_template('login.j2', screenMsg=screenMsg)
	# Project query for Create
	if request.method == 'POST':
		if 'createProject' in request.form:
			projectName = request.form['projectName']
			projectStart = request.form['projectStart']
			projectEnd = request.form['projectEnd']
			projectStatus = request.form['projectStatus']
			accountTeamID = session['accountTeamID']
			status_id = None
			if isinstance(projectStatus, str) and not projectStatus.isdigit():
				query = "SELECT statusID FROM Statuses WHERE statusName = %s"
				cursor.execute(query, (projectStatus,))
				status_result = cursor.fetchone()
				if status_result:
					status_id = status_result['statusID']
				else:
					status_id = 1
			else:
				status_id = projectStatus
			insert_query = """
            INSERT INTO Projects (projectName, projectStart, projectEnd, accountTeamID, projectStatus)
            VALUES (%s, %s, %s, %s, %s)
            """
			cursor.execute(insert_query, (projectName, projectStart, projectEnd, accountTeamID, status_id))
			db_connection.commit()
		#  Project query for Update
		elif 'editProject' in request.form:
			projectID = request.form['projectID']
			projectName = request.form['projectName']
			projectStart = request.form['projectStart']
			projectEnd = request.form['projectEnd']
			projectStatus = request.form.get('projectStatus')
			if projectStatus:
				status_id = None
				if isinstance(projectStatus, str) and not projectStatus.isdigit():
					query = "SELECT statusID FROM Statuses WHERE statusName = %s"
					cursor.execute(query, (projectStatus,))
					status_result = cursor.fetchone()
					if status_result:
						status_id = status_result['statusID']
				else:
					status_id = projectStatus
				update_query = """
                UPDATE Projects
                SET projectName = %s, projectStart = %s, projectEnd = %s, projectStatus = %s
                WHERE projectID = %s AND accountTeamID = %s
                """
				cursor.execute(update_query,
							   (projectName, projectStart, projectEnd, status_id, projectID, session['accountTeamID']))
			else:
				update_query = """
                UPDATE Projects
                SET projectName = %s, projectStart = %s, projectEnd = %s
                WHERE projectID = %s AND accountTeamID = %s
                """
				cursor.execute(update_query,
							   (projectName, projectStart, projectEnd, projectID, session['accountTeamID']))
			db_connection.commit()
		# Project query for Delete
		elif 'deleteProject' in request.form:
			projectID = request.form['projectID']
			delete_query = "DELETE FROM Projects WHERE projectID = %s AND accountTeamID = %s"
			cursor.execute(delete_query, (projectID, session['accountTeamID']))
			db_connection.commit()
		return redirect(url_for('projects'))
	cursor.execute('SELECT * FROM Statuses')
	statuses = cursor.fetchall()
	query = '''
    SELECT p.*, s.statusName
    FROM Projects p
    LEFT JOIN Statuses s ON p.projectStatus = s.statusID
    WHERE p.accountTeamID = %s
    '''
	inputs = (session['accountTeamID'])
	cursor.execute(query, inputs)
	projects = cursor.fetchall()
	if projects:
		screenMsg = f"Printing Projects for accountTeamID {session['accountTeamID']}"
		return render_template('projects.j2', screenMsg=screenMsg, accountUsername=session['accountUsername'],
							   projects=projects, statuses=statuses)
	else:
		screenMsg = 'No projects found for your team'
		return render_template('projects.j2', screenMsg=screenMsg, accountUsername=session['accountUsername'],
							   projects=[], statuses=statuses)

@app.route("/updateProjectStatus", methods=['POST'])
def update_project_status():
	try:
		if 'loggedin' not in session or not session['loggedin']:
			return jsonify({"error": "Not logged in"}), 401
		data = request.get_json()
		if not data:
			return jsonify({"error": "No JSON data received"}), 400
		projectID = data.get("projectID")
		projectStatus = data.get("projectStatus")
		print(f"Received update request: projectID={projectID}, projectStatus={projectStatus}")
		if not projectID or not projectStatus:
			return jsonify({"error": "Missing projectID or projectStatus"}), 400
		project_query = "SELECT * FROM Projects WHERE projectID = %s"
		cursor.execute(project_query, (projectID,))
		project = cursor.fetchone()
		if not project:
			return jsonify({"error": f"Project with ID {projectID} not found"}), 404
		status_query = "SELECT * FROM Statuses WHERE statusID = %s"
		cursor.execute(status_query, (projectStatus,))
		status = cursor.fetchone()
		if not status:
			return jsonify({"error": f"Status with ID {projectStatus} not found"}), 404
		query = "UPDATE Projects SET projectStatus = %s WHERE projectID = %s"
		cursor.execute(query, (projectStatus, projectID))
		cursor.connection.commit()
		print(f"Successfully updated project {projectID} to status {projectStatus}")
		return jsonify({
			"message": "Project status updated successfully",
			"projectID": projectID,
			"newStatus": projectStatus
		}), 200
	except Exception as e:
		print(f"Error in update_project_status: {str(e)}")
		return jsonify({"error": str(e)}), 500

@app.route('/sprints', methods=['GET', 'POST'])
def sprints():
	if request.method == "GET":
		querySprints = '''
		SELECT *
		FROM Sprints
		WHERE accountTeamID = %s
		'''
		queryInputs = (session['accountTeamID'])
		cursor.execute(querySprints, queryInputs)
		sprintsFetch = cursor.fetchall()
		return render_template("sprints.j2", sprints = sprintsFetch)
	else:
		return render_template("sprints.j2")

@app.route('/account_creation', methods=['GET', 'POST'])
def accountCreation():
	query = "SELECT * FROM Accounts;"
	cursor = db.execute_query(db_connection=db_connection, query=query)
	results = cursor.fetchall()
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
			# Redirect back to Login page
			return redirect(url_for('login'))
	return render_template("account_creation.j2", data = results)

@app.route('/accounts', methods=['GET', 'POST'])
def accountAdmin():
	query = "SELECT * FROM Accounts;"
	cursor = db.execute_query(db_connection=db_connection, query=query)
	results = cursor.fetchall()
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
			return redirect("/accounts")
	return render_template("accounts.j2", data = results)

@app.route("/delete_account/<int:id>")
def delete_account(id):
	# MySQL query to delete the account with our passed id
	query = "DELETE FROM Accounts WHERE accountID = '%s';"
	cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id))
	results = cursor.fetchall()
	return redirect("/accounts")

# Route for edit functionality, updating the attributes of the account
# Similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_accounts/<int:accountID>", methods=["POST", "GET"])
def edit_accounts(accountID):
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
	# Redirect back to accounts page
	return redirect("/accounts")

@app.route("/edit_password/<int:accountID>", methods=["POST", "GET"])
def edit_password(accountID):
	if request.method == "GET":
		query = "SELECT * FROM Accounts WHERE accountID = %s" % (accountID)
		cursor = db.execute_query(db_connection=db_connection, query=query)
		data = cursor.fetchall()
		return render_template("edit_password.j2", data=data)

@app.route("/update_password", methods=["POST"])
def update_password():
	# Grab account form inputs
	accountID = request.form["accountID"]
	accountUsername = request.form["accountUsername"]
	accountFirstName = request.form["accountFirstName"]
	accountLastName = request.form["accountLastName"]
	accountPassword = request.form["accountPassword"]
	accountTeamID = request.form["accountTeamID"]
	accountRole = request.form["accountRole"]
	query = "UPDATE Accounts SET accountPassword = %s WHERE accountID = %s"
	print(query)
	cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(accountPassword, accountID ))
	cursor.connection.commit()
	# Redirect back to Help page
	return redirect("/help")

# Listener
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 9112))
	app.run(port=port, debug=True)
