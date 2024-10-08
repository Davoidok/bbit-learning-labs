import pika
import os

from producer_interface import mqProducerInterface

class mqProducer(mqProducerInterface):

    def __init__(self, routing_key, exchange_name) -> None:
        # Save parameters to instance variable
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        self.setupRMQConnection()
    
    def setupRMQConnection(self) -> None:
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        connection = pika.BlockingConnection(parameters=con_params)
        self.connection = connection
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="Exchange Name", exchange_type="topic")
    
    def publishOrder(self, message: str) -> None:
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message,
        )
        self.channel.close()
        self.connection.close()        


