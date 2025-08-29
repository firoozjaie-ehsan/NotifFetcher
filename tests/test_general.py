import os

def test_run_mode_value_at_run_time():
    assert os.environ["RUN_MODE"] == "test"