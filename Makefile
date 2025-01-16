DOCKER_LOCAL_FILE=docker-compose.local.yaml

env:
	poetry shell

dep:
	poetry update

lint: env
	black . --diff && flake8 .

serve: env dep run
	poetry run python ./ask_me_bot/main.py

run:
	docker compose -f $(DOCKER_LOCAL_FILE) up -d --build

stop:
	docker compose -f $(DOCKER_LOCAL_FILE) down

migrate: env
	alembic upgrade head