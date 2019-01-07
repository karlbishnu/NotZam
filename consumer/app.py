"""Example Kafka consumer."""

import json
import os

from kafka import KafkaConsumer
from common.log.logger import get_logger
from common.log.cid import set_cid


KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TOPIC = os.environ.get('UPLOAD_TOPIC')
logger = get_logger(__name__)

if __name__ == '__main__':
    print("%s $s" % KAFKA_BROKER_URL, TOPIC)
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value),
    )

    for message in consumer:
        transaction: dict = message.value
        cid: str = transaction['cid']
        set_cid(cid)
        logger.info(transaction)
