from os import system
from sys import stdout

def deploy():
    stdout.write("***********************Linting************************\n")
    linted = system('pylint uncannly > pylint.log')
    if linted != 0:
        return stdout.write('Linting errors; see pylint.log.\n')

    stdout.write("***********************Testing************************\n")
    tested = system('nosetests')
    if tested != 0:
        return stdout.write('Some tests failed.\n')

    stdout.write("*************Updating Production Database*************\n")
    updated_production_database = system('python bin/initialize_database.py --production')
    if updated_production_database != 0:
        return stdout.write('Production database update failed.\n')

    stdout.write("**********************Deploying***********************\n")
    system('cf push')

deploy()
