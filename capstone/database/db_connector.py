import pymysql
import os

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
	if db_connection is None:
		print("No connection to the database found! Have you called connect_to_database() first?")
		return None
	if query is None or len(query.strip()) == 0:
		print("query is empty! Please pass a SQL query in query")
		return None

	print("Executing %s with %s" % (query, query_params));
	cursor = db_connection.cursor(pymysql.cursors.DictCursor)
	cursor.execute(query, query_params)
	db_connection.commit();
	return cursor


if __name__ == '__main__':
	print("Executing a sample query on the database using the credentials from db_credentials.py")
	db = connect_to_database()
	query = "SELECT * from Projects;"
	results = execute_query(db, query);
	print("Printing results of %s" % query)

	for r in results.fetchall():
		print(r)
