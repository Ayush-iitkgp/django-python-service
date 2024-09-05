# Python Django Service

1. Using poetry as the package manager. Install poetry version 1.6.1

## Run the tests
1. `docker-compose up -d`
2. exec into the container
3. `poetry run pytest`


## Test the API endpoint locally
1. `docker-compose up -d`
2. `make create-migration`
3. make migrate
4. make create-superuser
5. make run
6. Login to django admin localhost:8000/admin
7. Create an API Key
8. Use the curl the command
