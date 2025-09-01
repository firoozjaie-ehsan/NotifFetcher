import json
from pika import BasicProperties
from pika import exceptions as pika_exceptions

class RabbitMQProducer():
    def __init__(self, connection):
        self.connection = connection
        self.channel = None
        
    def published_message(self, exchange, routing_key, data):
        if self.channel is None:
            self.channel = self.connection.get_channel()
        
        if self.channel is not None:
            try:
                self.channel.exchange_declare(exchange=exchange, exchange_type='topic')
                message = json.dumps(data)
                properties = BasicProperties(content_type='application/json', delivery_mode=2)
                self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message, properties=properties)
                print("published message to exchange:", exchange, "with routing key:", routing_key)
            except pika_exceptions.ConnectionClosedByBroker:
                print("connection closed by broker: failed to publish message")
        else:
            print("failed to obtain channel for publishing message")