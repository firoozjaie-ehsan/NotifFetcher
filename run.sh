
# Different modes of running the application

# for testing
docker compose --env-file .env.test up --build          for testing with build
docker compose --env-file .env.test up                  for testing without build
docker exec -it python_test python main.py              run main in test container

# for debugging mode
docker compose --env-file .env.dev up --build           for development and debug with build
docker compose --env-file .env.dev up                   for run without build
docker exec -it python_debug python main.py

# for production mode
docker compose --env-file .env.prod up --build          for production with build
docker compose --env-file .env.prod up                  for production without build
docker exec -it python_production python main.py

# common commands
# build and run
docker-compose build python-app
docker-compose up -d
docker compose ps
docker compose logs -f python-app
docker exec -it python_test bash
docker compose down -v



# run test
docker exec -it python_test pytest .       run all tests without show print in console
docker exec -it python_test pytest -s        run all tes with show print in console
docker exec -it python_test pytest -v        show more details
docker exec -it python_test pytest -v -k "test_singleton_connection"   run specific test
docker exec -it python_test pytest -v -k "test_singleton_connection" --maxfail=1 --disable-warnings -q   stop on first fail and disable warnings

