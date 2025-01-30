from flask import Flask, render_template, json, jsonify
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()


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
