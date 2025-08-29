from unittest.mock import patch
from pika import BlockingConnection
from connection import RabbitMQConnection
from config import Config as AppConfig
import pytest

@pytest.fixture
def config():
    return AppConfig()

@pytest.fixture
def rabbitmq_connection(config):
    return RabbitMQConnection(
        host=config.RABBITMQ_HOST,
        port=config.RABBITMQ_PORT,
        username=config.RABBITMQ_USER,
        password=config.RABBITMQ_PASS,
    )

def test_rabbitmq_singleton_instance():
    print("Starting verify singleton RabbitMQ connection  in test_rabbitmq_singleton_instance...")
    c1 = RabbitMQConnection()
    c2 = RabbitMQConnection()
    print("Are both connections the same instance?", c1 is c2)
    assert c1 is c2, "RabbitMQConnection is not a singleton!"
    with RabbitMQConnection() as connection:
        print("connection channel:",connection.get_channel())
        print("connection is connected? ",connection.is_connected())
        assert connection.is_connected(), "Failed to connect to RabbitMQ"
        

def test_connect_successfully(rabbitmq_connection):
    print("Starting test_connect_successfully...")
    with patch.object(BlockingConnection, '__init__', return_value=None), patch.object(BlockingConnection, 'is_open', return_value=True):
        rabbitmq_connection.connect()
        assert rabbitmq_connection.connection is not None, "Connection should be established"
        assert rabbitmq_connection.connection.is_open, "Connection should be open"