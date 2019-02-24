import os

from common.mq.kafka import consumer, producer
from common.log.logger import get_logger
from common.log.cid import set_cid
from trainer import process

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
CONSUMER_TOPIC = os.environ.get('TOPIC_TRAINING_CONSUMER')
PRODUCER_TOPICS = [topic.strip() for topic in str(os.environ.get('TOPICS_TRAINER_PRODUCER')).split(",")]

logger = get_logger(__name__)

send = producer(KAFKA_BROKER_URL)


if __name__ == '__main__':
    consumer = consumer(KAFKA_BROKER_URL, CONSUMER_TOPIC)

    for message in consumer:
        data: dict = message.value
        cid: str = data['cid']
        set_cid(cid)
        data['callback'] = {'topics': PRODUCER_TOPICS, 'send': send}
        logger.info(data)
        process(data)

