
build:
	docker-compose --env-file secrets.env build

run:
	docker-compose -env-file secrets.env up

stop:
	docker-compose down
