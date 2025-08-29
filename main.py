from connection import RabbitMQConnection

print("Starting connection to RabbitMQ...")
c1 = RabbitMQConnection()
c2 = RabbitMQConnection()
print("Are both connections the same instance?", c1 is c2)

with RabbitMQConnection() as connection:
    print("connection channel:",connection.get_channel())
    print("connection is connected? ",connection.is_connected())
    print("✅ Successfully connected to RabbitMQ")