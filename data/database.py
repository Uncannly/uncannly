import os
import sys
import urlparse

import psycopg2
from cfenv import AppEnv

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
    if len(sys.argv) > 1 and (sys.argv[1] == "--production" or sys.argv[1] == "-p"):
        with open('production_database_credentials.txt', 'r') as credentials_file:
            credentials = credentials_file.read().replace('\n', '')
    elif os.environ.get('VCAP_SERVICES') is not None:
        credentials = AppEnv().get_service(label='elephantsql').credentials['uri']
    else:
        credentials = 'postgres://postgres:duperuser@localhost:5432/uncannly'

    parsed_credentials = urlparse.urlparse(credentials)
    return psycopg2.connect(
        database=parsed_credentials.path[1:],
        user=parsed_credentials.username,
        password=parsed_credentials.password,
        host=parsed_credentials.hostname
    )
