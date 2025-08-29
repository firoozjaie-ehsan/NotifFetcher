from connection import RabbitMQConnection


def test_rabbitmq_singleton():
    print("Starting verify singleton RabbitMQ connection  in test_rabbitmq_singleton...")
    c1 = RabbitMQConnection()
    c2 = RabbitMQConnection()
    print("Are both connections the same instance?", c1 is c2)
    assert c1 is c2, "RabbitMQConnection is not a singleton!"
    with RabbitMQConnection() as connection:
        print("connection channel:",connection.get_channel())
        print("connection is connected? ",connection.is_connected())
        assert connection.is_connected(), "Failed to connect to RabbitMQ"