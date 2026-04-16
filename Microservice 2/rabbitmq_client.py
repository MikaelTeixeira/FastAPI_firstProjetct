import json
from typing import Any, Callable

import pika

RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672


def publish_message(queue_name: str, event_type: str, payload: dict[str, Any]) -> bool:
    connection = None

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        message = json.dumps({"event_type": event_type, "payload": payload})
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )
        return True
    except Exception:
        return False
    finally:
        if connection and connection.is_open:
            connection.close()


def consume_messages(
    queue_name: str,
    handler: Callable[[dict[str, Any]], None],
) -> None:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        handler(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print(f"Listening to queue: {queue_name}")
    channel.start_consuming()
