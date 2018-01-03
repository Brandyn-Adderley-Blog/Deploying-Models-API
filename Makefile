
create_project:
	docker-compose run web django-admin.py startproject deploy_models ./Model-Deployment

build:
	docker-compose build

create_app:
	docker-compose run web django-admin.py startapp api ./Model-Deployment/api

migrate_data:
	docker exec -it djangoweb_01 python manage.py makemigrations
	docker exec -it djangoweb_01 python manage.py migrate

up:
	docker-compose up -d

down:
	docker-compose down

start:
	docker-compose start

stop:
	docker-compose stop

django-dev:
	docker-compose run -p 8000:8000 web python ./Model-Deployment/manage.py runserver 0.0.0.0:8000

jupyter-web:
	docker-compose run -p 8888:8888 web jupyter-notebook --no-browser --port 8888 --ip='*' --allow-root

bash-web:
	docker exec -it djangoweb_01 bash

log-web:
	docker-compose logs web
