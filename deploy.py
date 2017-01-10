import os
import sys

def deploy():
    sys.stdout.write("***********************Linting************************\n")
    linted = os.system('pylint uncannly > pylint.log')
    if linted != 0:
        return sys.stdout.write('Linting errors; see pylint.log.\n')

    sys.stdout.write("***********************Testing************************\n")
    tested = os.system('nosetests')
    if tested != 0:
        return sys.stdout.write('Some tests failed.\n')

    sys.stdout.write("*************Updating Production Database*************\n")
    updated_production_database = os.system('python data/initialize_database.py --production')
    if updated_production_database != 0:
        return sys.stdout.write('Production database update failed.\n')

    sys.stdout.write("**********************Deploying***********************\n")
    os.system('cf push')

deploy()
