
build:
	docker compose --env-file secrets.env build

run:
	docker compose up --no-build

stop:
	docker compose down
