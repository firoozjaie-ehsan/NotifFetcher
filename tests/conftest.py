import os

def pytest_configure(config):
    print("RUN_MODE before set in conftest:", os.environ.get("RUN_MODE"))
    os.environ['RUN_MODE'] = 'test'
    print("RUN_MODE after set in conftest:", os.environ.get("RUN_MODE"))