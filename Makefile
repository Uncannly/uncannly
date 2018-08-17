start:
	~/AppData/Local/Google/"Cloud SDK"/google-cloud-sdk/bin/dev_appserver.py app.yaml

deploy:
	./bin/deploy.sh

build:
	python -m bin.compile_assets

setup:
	./bin/setup.sh

seed:
	python -m bin.initialize_database
