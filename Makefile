
build:
	docker-compose --env-file secrets.env build

run:
	docker-compose up --env-file secrets.env

stop:
	docker-compose down
