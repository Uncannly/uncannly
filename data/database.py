import os, urlparse

import psycopg2
from cfenv import AppEnv

class Database:
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
  if os.environ.get('VCAP_SERVICES') is None:
    credentials = 'postgres://postgres:5554d58@localhost:5432/uncannly'
  else:
    credentials = AppEnv().get_service(label='elephantsql').credentials['uri']

  parsed_credentials = urlparse.urlparse(credentials)
  return psycopg2.connect(
    database=parsed_credentials.path[1:],
    user=parsed_credentials.username,
    password=parsed_credentials.password,
    host=parsed_credentials.hostname
  )