#!/usr/bin/env sh

set -e -x

pip install libsass pylint
echo 'export PYTHONPATH=$PYTHONPATH:~/workspace/uncannly' >> ~/.bash_profile

gcloud config configurations create uncannly
gcloud config set project uncannly
gcloud config set account kingwoodchuckii@gmail.com

gcloud auth application-default login

pip install -t env -r requirements.txt

python -m bin.compile_assets
python -m bin.initialize_database
