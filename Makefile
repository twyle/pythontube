update:
	@pip install --upgrade pip

install:
	@pip install -r services/app/requirements.txt

install-dev:
	@pip install -r services/app/requirements-dev.txt

test:
	@python -m pytest --disable-warnings

coverage:
	@coverage run -m pytest --disable-warnings
	@coverage report -m

run:
	@python services/app/manage.py run -h 0.0.0.0

create_db:
	@python services/app/manage.py create_db

gunicorn:
	@cd services/app && gunicorn -b 0.0.0.0:5000 manage:app

lint:
	@black services/app
	@isort services/app
	@flake8
	@pydocstyle  services/app/api
	@pylint --rcfile=.pylintrc ./services/app/api

build-dev:
	@docker build -f ./services/app/Dockerfile -t learning-site-dev:latest ./services/app

run-dev:
	@docker run -p5000:5000 --env-file=./services/app/.env learning-site-dev:latest

build-prod:
	@docker build -f ./services/app/Dockerfile.prod -t learning-site-prod:latest ./services/app

run-prod:
	@docker run -p5000:5000 --env-file=./services/app/.env learning-site-prod:latest

ayv:
	@pip uninstall ayv -y
	@pip install /home/lyle/professional-projects/youtube/dist/ayv-0.5.0-py3-none-any.whl

dev:
	@docker-compose -f docker-compose-dev.yaml up --build

search:
	@docker-compose -f services/search/docker-compose.yml up --build

run-db:
	@docker-compose -f services/database/docker-compose.yml up --build

stop-db:
	@docker-compose -f services/database/docker-compose.yml down -v

create-db: 
	@python services/app/manage.py create_db 

seed-db: 
	@python services/app/manage.py seed_db