import configparser
import json
from datetime import datetime

import pika
from faker import Faker

from src.connection import session
from src.models import Contact

config = configparser.ConfigParser()
config.read("config.ini")

UNAME = config.get("RB", "user")
PWORD = config.get("RB", "pass")
HOST = config.get("RB", "host")
PORT = config.get("RB", "port")
EXC = config.get("RB", "exchange")
QUE = config.get("RB", "queue")

credentials = pika.PlainCredentials(UNAME, PWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST, port=PORT, credentials=credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange=EXC, exchange_type="direct")
channel.queue_declare(queue=EXC, durable=True)
channel.queue_bind(exchange=EXC, queue=QUE)

fake = Faker()


def seed_contacts():
    for i in range(10):
        Contact(
            fullname=fake.name(), email=fake.email(), phone=fake.phone_number()
        ).save()


def main():
    contacts = Contact.objects()
    for contact in contacts:
        message = {"id": str(contact.id)}

        channel.basic_publish(
            exchange=EXC,
            routing_key=QUE,
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        print(f" [x] Sent {message}")
    connection.close()


if __name__ == "__main__":
    seed_contacts()
    main()
