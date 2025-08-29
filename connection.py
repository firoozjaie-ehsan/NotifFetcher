from pika import ConnectionParameters, PlainCredentials, BlockingConnection, exceptions
import time
import config

class RabbitMQConnection:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, host = "rabbitmq", port = 5672, username = "admin", password = "admin"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        
        
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exit_type, exit_val, exit_tb):
        self.close()
    
    
    def connect(self):
        retries = 0
        while retries < 30:
            try:
                print(f"🔄 Trying to connect... host={self.host}, port={self.port}, user={self.username}")
                credential = PlainCredentials(self.username, self.password)
                parameters = ConnectionParameters(host=self.host, port=self.port, credentials=credential)   
                self.connection = BlockingConnection(parameters)
                print("Connected to RabbitMQ server.")
                return
            except exceptions.AMQPConnectionError as e:
                print(f"Failed to connect to RabbitMQ server: {e}")
                retries += 1
                waiting_time =config.Config().waiting_factor() ** retries
                print(f"Retrying in {waiting_time} seconds...")
                time.sleep(waiting_time)
        print("Max retries reached. Could not connect to RabbitMQ server. stopping the program.")
    def is_connected(self):
        print("is open?", self.connection.is_open if self.connection else False)
        return self.connection is not None and self.connection.is_open
    
    def close(self):
        if self.is_connected():
            self.connection.close()
            self.connection = None
            print("Connection to RabbitMQ closed.")
    
    def get_channel(self):
        if self.is_connected():
            return self.connection.channel()
        else:
            return None
    