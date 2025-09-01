from unittest.mock import MagicMock, patch
from pika import BlockingConnection
from connection import RabbitMQConnection
from pika.exceptions import AMQPConnectionError
from config import Config as AppConfig
from unittest.mock import PropertyMock

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
    with patch.object(BlockingConnection, '__init__', return_value=None), \
        patch.object(BlockingConnection, 'is_open', new_callable=PropertyMock, return_value=True):
        # Mock the BlockingConnection to simulate a successful connection
        rabbitmq_connection.connect()
        assert rabbitmq_connection.connection is not None, "Connection should be established"
        assert rabbitmq_connection.connection.is_open, "Connection should be open"
        

def test_connect_failed(rabbitmq_connection):
    print("Starting test_connect_failed...")
    with patch.object(BlockingConnection, '__init__', side_effect = AMQPConnectionError("connection failed")):
        assert rabbitmq_connection.connection is None, "Connection should be established"


def test_is_connected(rabbitmq_connection):
    print("Starting test_is_connected...")
    with patch.object(BlockingConnection, '__init__', return_value=None), patch.object(BlockingConnection, 'is_open', return_value=True):
        rabbitmq_connection.connect()
        assert rabbitmq_connection.is_connected()
        

def test_is_connected_false(rabbitmq_connection):
    print("Starting test_is_connected...")
    with patch.object(BlockingConnection, '__init__', return_value=None), patch.object(BlockingConnection, 'is_open', return_value=True):
        assert not rabbitmq_connection.is_connected()
        
def test_close(rabbitmq_connection):
    print("Starting test_close...")
    connction_mock = MagicMock(BlockingConnection)
    rabbitmq_connection.connection = connction_mock
    rabbitmq_connection.close()
    connction_mock.close.assert_called_once()
    assert rabbitmq_connection.connection is None, "Connection should be None after close"
    
def test_get_channel_not_connected(rabbitmq_connection):
    print("Starting test_get_channel_not_connected...")
    assert rabbitmq_connection.get_channel() is None, "Channel should be None if not connected"

def test_get_channel_connected(rabbitmq_connection):
    print("Starting test_get_channel_connected...")
    connction_mock = MagicMock(BlockingConnection)
    channel_mock = MagicMock()
    connction_mock.channel.return_value = channel_mock
    rabbitmq_connection.connection = connction_mock
    channel = rabbitmq_connection.get_channel()
    assert channel_mock is channel, "Should return the mocked channel"