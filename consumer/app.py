"""Example Kafka consumer."""

import os

from common.mq.kafka import consumer
from common.log.logger import get_logger
from common.log.cid import set_cid


KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TOPIC = os.environ.get('UPLOAD_TOPIC')
logger = get_logger(__name__)

if __name__ == '__main__':
    consumer = consumer(KAFKA_BROKER_URL, TOPIC)

    for message in consumer:
        transaction: dict = message.value
        cid: str = transaction['cid']
        set_cid(cid)
        logger.info(transaction)
