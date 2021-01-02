DOCKER_CMD=docker exec -it blog

_config-env:
	[ -f fazendoissoerrado/.env ] || cp fazendoissoerrado/.env.sample fazendoissoerrado/.env

_upgrade-pip:
	${DOCKER_CMD} pip install --upgrade pip

build:
	docker-compose up -d

setup: _config-env _upgrade-pip
	${DOCKER_CMD} pip install -r requirements.txt

migrate:
	${DOCKER_CMD} python manage.py migrate

bash:
	${DOCKER_CMD} sh

run:
	${DOCKER_CMD} gunicorn fazendoissoerrado.wsgi:application --bind 0.0.0.0:8000 --workers 3

start:
	${DOCKER_CMD} python manage.py runserver 0.0.0.0:8000
