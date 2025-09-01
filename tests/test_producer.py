from producers.base import RabbitMQProducer
from pika.exceptions import ConnectionClosedByBroker
from unittest.mock import MagicMock

def test_publish_message(capsys):
    connection = MagicMock()
    producer = RabbitMQProducer(connection) 
    channel = MagicMock()
    channel.exchange_declare.return_value = None
    channel.basic_publish.return_value = None
    
    connection.get_channel.return_value = channel
    exchange = 'test_exchange'
    routing_key = 'test.key'
    message = {'data': 'test_message'}
    
    producer.published_message(exchange = exchange, routing_key = routing_key, data = message)
    channel.basic_publish.assert_called_once()
    channel.exchange_declare.assert_called_once()
    
    capture = capsys.readouterr()
    assert capture.out.startswith("published message to exchange")


def test_publish_message_failed(capsys):
    connection = MagicMock()
    producer = RabbitMQProducer(connection)
    
    channel = MagicMock()
    channel.exchange_declare.return_value = None
    channel.basic_publish.return_value = None
    
    def side_effect(exchange, routing_key, body, properties):
        raise ConnectionClosedByBroker(0, "sample reason")
    
    channel.basic_publish.side_effect = side_effect
    connection.get_channel.return_value = channel
    
    exchange = 'test_exchange'
    routing_key = 'test.key'
    message = {'data': 'test_message'}
    
    producer.published_message(exchange = exchange, routing_key = routing_key, data = message)
    
    capture = capsys.readouterr()
    assert capture.out.startswith("connection closed by broker: failed to publish message")
