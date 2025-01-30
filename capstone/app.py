from flask import Flask, render_template, json
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

# @app.route('/sub-page')
# def sub_page():
#     cursor = db_connection.cursor()
#     query = "SELECT * FROM projects-tasks;"

#     cursor.execute(query)

#     results = cursor.fetchall()
#     print(results)
#     return render_template("projects", projects=results)



# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)
