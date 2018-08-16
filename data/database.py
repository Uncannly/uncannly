import os
import sys
import urlparse

import MySQLdb

CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

class Database(object):
    def __init__(self):
        self.connection = connect()

    def disconnect(self):
        self.connection.commit()
        self.connection.close()

    def execute(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()

    @staticmethod
    def fetch(sql):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        connection.commit()
        connection.close()
        return results

def connect():
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        cloudsql_unix_socket = os.path.join( '/cloudsql', CLOUDSQL_CONNECTION_NAME)
        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD,
            db='uncannly-production-database'
        )
    else:
        db = MySQLdb.connect(
            host='127.0.0.1',
            port=3306,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD,
            db='uncannly-production-database'
        )

    return db
