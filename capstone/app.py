from flask import Flask, render_template, json, jsonify, redirect
from flask import request
from flask_mysqldb import MySQL
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()
mysql = MySQL(app)


# Routes

@app.route('/')
def login():
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
    return render_template("projects.j2")

@app.route('/account_creation', methods=['GET', 'POST'])
def accountCreation():

    if request.method == "POST":
        # fire off i user presses Create Account
        if request.form.get("Create_Account"):
            # grab user form inputs
            username = request.form["username"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            password = request.form["password"]
            accountTeam = "TeamA"
            accountRole = "Developer"
            

            # account for null age AND homeworld
            if username != "" and first_name != "" and last_name != "" and password != "":
                # mySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO Accounts (accountUsername, accountFirstName, accountLastName, accountPassword, accountTeam, accountRole) VALUES (%s, %s, %s, %s, %s, %s)"
                # cur = mysql.connection.cursor()
                # cur.execute(query, (username, first_name, last_name, password, accountTeam, accountRole))
                # mysql.connection.commit()
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, password, accountTeam, accountRole))
                results = cursor.fetchall()
                return render_template("accounts.j2", accounts = results)

    return render_template("account_creation.j2")

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
