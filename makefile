

stop:
	docker-compose down

start_admin: start
	docker exec rizzanet-web bash --login -c "cd /app/rizzanet/admin/admin_app && yarn install && yarn run start"

build_admin: start
	docker exec rizzanet-web bash --login -c "cd /app/rizzanet/admin/admin_app && yarn install && yarn run build_rizzanet"

start:
	docker-compose up -d

in: start
	docker exec -it rizzanet-web bash

up: start
down: stop
