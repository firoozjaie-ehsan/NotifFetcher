from connection import RabbitMQConnection


with RabbitMQConnection() as connection:
    print("connection channel:",connection.get_channel())
    print("connection is connected? ",connection.is_connected())
    print("✅ Successfully connected to RabbitMQ")



