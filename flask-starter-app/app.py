from flask import Flask, render_template, json
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()


# Routes

@app.route('/')
def root():
    return render_template("login.j2")

@app.route('/bsg-people')
def bsg_people():
    cursor = db_connection.cursor()
    query = "SELECT * FROM bsg_people;"

    cursor.execute(query)

    results = cursor.fetchall()
    print(results)
    return render_template("bsg.j2", bsg_people=results)



# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)
