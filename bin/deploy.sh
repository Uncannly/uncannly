#!/bin/bash

set -e
echo "***********************\nLinting\n************************"
pylint uncannly > pylint.log
echo "*************\nUpdating Production Database\n*************"
python data/initialize_database.py --production
echo "**********************\nDeploying\n***********************"
cf push