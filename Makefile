run-db:
	docker run --name coffee_postgres -p 5432:5432 -e POSTGRES_PASSWORD=coffee -e POSTGRES_DB=coffee -v ${PWD}/db_data:/var/lib/postgresql/data -d postgres
