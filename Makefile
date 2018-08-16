start:
	dev_appserver.py app.yaml

deploy:
	./bin/deploy.sh

build:
	python -m bin.compile_assets

setup:
	./bin/setup.sh

seed:
	python -m bin.initialize_database
