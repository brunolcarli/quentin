install:
	pip install -r quentin/requirements/${ENV_REF}.txt

run:
	python3 main.py

migrate:
	python3 -c 'from core.db_handler import migrate; migrate()'

docker_run:
	make migrate
	make run
