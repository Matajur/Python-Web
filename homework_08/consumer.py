import configparser
import json
import sys
import time
import os

import pika

from src.connection import session
from src.models import Contact

config = configparser.ConfigParser()
config.read("config.ini")

UNAME = config.get("RB", "user")
PWORD = config.get("RB", "pass")
HOST = config.get("RB", "host")
PORT = config.get("RB", "port")
QUE = config.get("RB", "queue")

credentials = pika.PlainCredentials(UNAME, PWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST, port=PORT, credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue=QUE, durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] Received {message}")
    result = send_message(message)
    if result == True:
        contact = Contact.objects(id=message.get("id"))
        contact[0].update(status=True)
        print(f" [x] Done: {method.delivery_tag}")
        ch.basic_ack(delivery_tag=method.delivery_tag)


def send_message(message):
    time.sleep(1)
    contact = Contact.objects(id=message.get("id"))
    print(f" [V] Sent message to {contact[0].fullname}")
    return True


channel.basic_qos(prefetch_count=5)  # pool size
channel.basic_consume(queue=QUE, on_message_callback=callback)


if __name__ == "__main__":
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except:
            os._exit(0)
