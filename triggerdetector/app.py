import os

from common.mq.kafka import consumer, producer
from common.log.logger import get_logger
from common.log.cid import set_cid
from trigger_word import process

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
CONSUMER_TOPIC = os.environ.get('TOPIC_DETECTOR_CONSUMER')
PRODUCER_TOPICS = [topic.strip() for topic in str(os.environ.get('TOPICS_DETECTOR_PRODUCER')).split(",")]

logger = get_logger(__name__)

if __name__ == '__main__':
    consumer = consumer(KAFKA_BROKER_URL, CONSUMER_TOPIC)

    for message in consumer:
        data: dict = message.value
        cid: str = data['cid']
        set_cid(cid)
        res = process(data)

        if res:
            send = producer(KAFKA_BROKER_URL)
            for topic in PRODUCER_TOPICS:
                send(topic, res)

