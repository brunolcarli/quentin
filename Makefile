install:
	pip install -r quentin/requirements/${ENV_REF}.txt

run:
	python3 manage.py run

migrate:
	python3 -c 'from core.db_handler import migrate; from quentin.settings import MYSQL_CONFIG; migrate(MYSQL_CONFIG["MYSQL_DATABASE"])'

docker_run:
	make migrate
	make run

test:
	python3 -c 'from core.db_handler import migrate; migrate("test_db")'
	pytest tests
	python -c "from core.db_handler import flush_test_database; flush_test_database()"

