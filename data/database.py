import os, json, urlparse

import psycopg2
from cfenv import AppEnv

def connect():
	if os.environ.get('VCAP_SERVICES') is None:
		credentials = 'postgres://postgres:5554d58@localhost:5432/mydb'
	else:
		credentials = AppEnv().get_service(label='elephantsql').credentials['uri']

	parsed_credentials = urlparse.urlparse(credentials)
	return psycopg2.connect(
		database=parsed_credentials.path[1:],
		user=parsed_credentials.username,
		password=parsed_credentials.password,
		host=parsed_credentials.hostname
	)

def disconnect(connection):
	connection.commit()
	connection.close()

def execute(connection, sql):
	cur = connection.cursor()
	cur.execute(sql)
	cur.close()

def fetch(sql):
	connection = connect()
	cur = connection.cursor()
	cur.execute(sql)
	results = cur.fetchall()
	cur.close()
	disconnect(connection)
	return results