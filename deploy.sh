#!/bin/bash

set -e
echo ""
echo "***********************Linting************************"
echo ""
pylint uncannly > pylint.log || (echo "Linting errors; see pylint.log" && exit 1)
echo ""
echo "*************Updating Production Database*************"
echo ""
python data/initialize_database.py --production || (echo "Prod db init failed." && exit 1)
echo "**********************Deploying***********************"
cf push