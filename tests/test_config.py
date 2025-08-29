from config import Config
import os
def test_config_singleton():
    config1 = Config()
    config2 = Config()
    assert config1 is config2, "Config should be a singleton"
    
def test_config_default_values():
    os.environ.pop("RABBITMQ_HOST", None)
    os.environ.pop("RABBITMQ_PORT", None)
    os.environ.pop("RABBITMQ_USER", None)
    os.environ.pop("RABBITMQ_PASS", None)
    os.environ.pop("RABBITMQ_VHOST", None)
    os.environ.pop("RUN_MODE", None)
    
    config = Config(load_from_file=False, override = True)
    assert config.RABBITMQ_HOST == "localhost"
    assert config.RABBITMQ_USER == "admin"
    assert config.RABBITMQ_PORT == 5672
    assert config.RABBITMQ_PASS == "admin"
    assert config.RABBITMQ_VHOST == "localhost"
    assert config.RUN_MODE == "DEBUG"
    
    os.environ["RUN_MODE"] = "test"
    
def test_is_test_mode():
    config = Config(override=True)
    
    config.RUN_MODE == "test"
    assert config.is_test_mode() == True
    
    config.RUN_MODE = "debug"
    assert config.is_test_mode() == False
    
    config.RUN_MODE = "prod"
    assert config.is_test_mode() == False
    
    config.RUN_MODE = "test"
    
def test_is_debug_mode():
    config = Config(override=True)
    
    config.RUN_MODE == "test"
    assert config.is_debug_mode() == False
    
    config.RUN_MODE = "debug"
    assert config.is_debug_mode() == True
    
    config.RUN_MODE = "prod"
    assert config.is_debug_mode() == False
    
    config.RUN_MODE = "test"
    
def test_waiting_factor():
    config = Config(override=True)
    
    config.RUN_MODE == "test"
    assert config.waiting_factor() == 0
    
    config.RUN_MODE = "debug"
    assert config.waiting_factor() == 2
    
    config.RUN_MODE = "prod"
    assert config.waiting_factor() == 2
    
    config.RUN_MODE = "test"