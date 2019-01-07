from time import sleep
import json
from common.log.logger import get_logger

from kafka import KafkaConsumer, KafkaProducer

logger = get_logger(__name__)


def consumer(broker, topic):
    kafka_consumer = KafkaConsumer(
        topic,
        bootstrap_servers=broker,
        value_deserializer=lambda value: json.loads(value),
        auto_offset_reset='earliest',
    )

    logger.info("Kafka consumer of {broker}-{topic} started".format(broker=broker, topic=topic))
    return kafka_consumer


def serializer(m):
    return json.dumps(m).encode('utf-8')


def producer(broker):
    kafka_producer = KafkaProducer(bootstrap_servers=broker,
                                   value_serializer=lambda m: json.dumps(m).encode('utf-8'))
    logger.info("Kafka producer of {broker} started".format(broker=broker))

    def send(topic, message):
        future = kafka_producer.send(topic, message)
        sleep(1)
        logger.info("topic : {topic} sent: {message}".format(topic=topic, message=serializer(message)))
        return future

    return send
