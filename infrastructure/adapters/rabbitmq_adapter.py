import json
import pika
from application.ports.message_broker import MessagePublisher, MessageConsumer
from infrastructure import config

class RabbitMQPublisher(MessagePublisher):
    def __init__(self):
        self.credentials = pika.PlainCredentials(config.RABBITMQ_USER, config.RABBITMQ_PASSWORD)
        self.parameters = pika.ConnectionParameters(
            host=config.RABBITMQ_HOST,
            port=config.RABBITMQ_PORT,
            virtual_host=config.RABBITMQ_VHOST,
            credentials=self.credentials
        )
        self.connection = None
        self.channel = None

    def _connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()

    def publish(self, topic: str, message: dict) -> None:
        self._connect()
        self.channel.queue_declare(queue=topic, durable=True)
        body = json.dumps(message)
        self.channel.basic_publish(
            exchange="",
            routing_key=topic,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Hacer el mensaje persistente
            )
        )
        print(f" [x] Enviado a RabbitMQ en '{topic}': {body}")

    def close(self) -> None:
        if self.connection and self.connection.is_open:
            self.connection.close()


class RabbitMQConsumer(MessageConsumer):
    def __init__(self):
        self.credentials = pika.PlainCredentials(config.RABBITMQ_USER, config.RABBITMQ_PASSWORD)
        self.parameters = pika.ConnectionParameters(
            host=config.RABBITMQ_HOST,
            port=config.RABBITMQ_PORT,
            virtual_host=config.RABBITMQ_VHOST,
            credentials=self.credentials
        )
        self.connection = None
        self.channel = None

    def _connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()

    def consume(self, topic: str, callback_fn) -> None:
        self._connect()
        self.channel.queue_declare(queue=topic, durable=True)

        def callback(ch, method, properties, body):
            try:
                data = json.loads(body.decode("utf-8"))
                callback_fn(data)
            except Exception as e:
                print(f" [!] Error al procesar mensaje en callback: {e}")

        self.channel.basic_consume(
            queue=topic,
            on_message_callback=callback,
            auto_ack=True
        )
        print(f" [*] Esperando mensajes en la cola '{topic}'. Presiona CTRL+C para salir.")
        self.channel.start_consuming()

    def close(self) -> None:
        if self.connection and self.connection.is_open:
            self.connection.close()
            print(" [x] Conexión de consumidor de RabbitMQ cerrada.")
