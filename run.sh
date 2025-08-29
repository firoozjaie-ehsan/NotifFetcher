
docker-compose build python-app
docker-compose up -d
docker compose ps
docker compose logs -f python-app
docker exec -it python_test bash
docker compose down -v

# run main
docker exec -it python_test python main.py 

# run test
docker exec -it python_test pytest .       run all tests without show print in console
docker exec -it python_test pytest -s        run all tes with show print in console
docker exec -it python_test pytest -v        show more details
docker exec -it python_test pytest -v -k "test_singleton_connection"   run specific test
docker exec -it python_test pytest -v -k "test_singleton_connection" --maxfail=1 --disable-warnings -q   stop on first fail and disable warnings
