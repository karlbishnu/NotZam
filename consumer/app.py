"""Example Kafka consumer."""

import json
import os

from kafka import KafkaConsumer, KafkaProducer
import logging

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TOPIC = os.environ.get('UPLOAD_TOPIC')


if __name__ == '__main__':
    print("%s $s" % KAFKA_BROKER_URL, TOPIC)
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value),
    )

    for message in consumer:
        transaction: dict = message.value
        logging.info("[cid: %s]" % transaction["cid"])
        print(transaction)  # DEBUG
