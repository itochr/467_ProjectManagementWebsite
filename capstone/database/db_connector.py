import pymysql
import os


# from dotenv import load_dotenv, find_dotenv
#
# # Load our environment variables from the .env file in the root of our project.
# load_dotenv(find_dotenv())

# # Set the variables in our application with those environment variables
# host = os.environ.get("340DBHOST")
# user = os.environ.get("340DBUSER")
# passwd = os.environ.get("340DBPW")
# db = os.environ.get("340DB")

def connect_to_database():
    """
    connects to a database and returns a database objects
    """
    timeout = 10
    db_connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="defaultdb",
        host="mysql-osu-capstone-capstone-project-management.l.aivencloud.com",
        password="AVNS_jJ5EndBYUZa_wWh4np5",
        read_timeout=timeout,
        port=27713,
        user="avnadmin",
        write_timeout=timeout,
    )
    return db_connection


def execute_query(db_connection=None, query=None, query_params=()):
    """
    executes a given SQL query on the given db connection and returns a Cursor object

    db_connection: a MySQLdb connection object created by connect_to_database()
    query: string containing SQL query

    returns: A Cursor object as specified at https://www.python.org/dev/peps/pep-0249/#cursor-objects.
    You need to run .fetchall() or .fetchone() on that object to actually acccess the results.

    """

    if db_connection is None:
        print("No connection to the database found! Have you called connect_to_database() first?")
        return None

    if query is None or len(query.strip()) == 0:
        print("query is empty! Please pass a SQL query in query")
        return None

    print("Executing %s with %s" % (query, query_params));
    # Create a cursor to execute query. Why? Because apparently they optimize execution by retaining a reference according to PEP0249
    cursor = db_connection.cursor(pymysql.cursors.DictCursor)

    '''
    params = tuple()
    #create a tuple of paramters to send with the query
    for q in query_params:
        params = params + (q)
    '''
    # TODO: Sanitize the query before executing it!!!
    cursor.execute(query, query_params)
    # this will actually commit any changes to the database. without this no
    # changes will be committed!
    db_connection.commit();
    return cursor


if __name__ == '__main__':
    print("Executing a sample query on the database using the credentials from db_credentials.py")
    db = connect_to_database()
    query = "SELECT * from bsg_people;"
    results = execute_query(db, query);
    print("Printing results of %s" % query)

    for r in results.fetchall():
        print(r)
