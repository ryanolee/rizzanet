stop:
	docker-compose down 

start_admin: start
	docker exec rizzanet-web bash --login -c "cd /app/rizzanet/admin/admin_app && yarn install && yarn run start"

build_admin: start
	docker exec rizzanet-web bash --login -c "cd /app/rizzanet/admin/admin_app && yarn install && yarn run build_rizzanet"

start:
	@docker-compose up --detach 

in: start
	docker exec -it rizzanet-web bash

reinstall: start
	docker exec rizzanet-web bash --login -c "cd /app/ && flask rizzanet drop_db --force && flask rizzanet install"

install: start
	docker exec rizzanet-web bash --login -c "cd /app/ && flask rizzanet install"

reindex: start
	docker exec rizzanet-web bash --login -c "cd /app/ && flask rizzanet reindex_elasticsearch"

up: start
down: stop

dev: start
	docker exec rizzanet-web bash --login -c "cd /app/ && flask rizzanet reindex_elasticsearch"

log:
	docker-compose up

build:
	docker-compose build
