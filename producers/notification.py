from connection import RabbitMQConnection
from config import Config
from producers.base import RabbitMQProducer

def send_notification():
    user_notfications = {
        "user1":{
            "notification":{"email":True,"sms":False},
            "email":"user1@example.com",
            "phone":"+1234567890"
        },
        "user2":{
            "notification":{"email":True,"sms":True},
            "email":"user2@exaple.com",
            "phone":"+0987654321"
        },
        "user3":{
            "notification":{"email":False,"sms":True},
            "email":"user3@exaple.com",
            "phone":"+1122334455"
        },
    }

    config = Config(override=True)
    with RabbitMQConnection(host = config.RABBITMQ_HOST, port = config.RABBITMQ_PORT, username= config.RABBITMQ_USER,
                            password= config.RABBITMQ_PASS) as connection:
        producer = RabbitMQProducer(connection)
        for user_id, user_data in user_notfications.items():
            notification_data = user_data["notification"]
            email = user_data["email"]
            phone = user_data["phone"]
            
            for notif_type, enabled in notification_data.items():
                if enabled:
                    routing_key = f"notification.{notif_type}"
                    message = {
                        "user_id": user_id,
                        "type": notif_type,
                        "email": email,
                        "phone": phone,
                        "message": f"This is a {notif_type} notification for {user_id}"
                    }
                    producer.published_message(exchange=config.EXCHANGE_NAME, routing_key=routing_key, data=message)
                    print(f"Sent {notif_type} notification to {user_id}")