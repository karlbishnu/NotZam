from kafka import KafkaProducer, KafkaConsumer
import os
from time import sleep
import logging
import json

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
logger = logging.getLogger('notzam')


def mq(topic):
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                             value_serializer=lambda m: serializer(m))
    print("Kafka producer of %s started" % KAFKA_BROKER_URL)

    def send(message):
        future = producer.send(topic, message)
        sleep(1)
        logger.info("sent: %s" % serializer(message))
        return future

    return send


def serializer(m):
    return json.dumps(m).encode('utf-8')

def consume():
    consumer = KafkaConsumer("test", bootstrap_servers=KAFKA_BROKER_URL,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                             auto_offset_reset='earliest')

