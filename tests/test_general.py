import os

def test_run_mode_value_at_run_time():
    print("verifying RUN_MODE environment variable is set to test at run time...")
    assert os.environ["RUN_MODE"] == "test"