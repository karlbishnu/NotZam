"""Example Kafka slicer."""

import os

from common.mq.kafka import consumer, producer
from common.log.logger import get_logger
from common.log.cid import set_cid
from pydub import AudioSegment

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TOPIC = os.environ.get('UPLOAD_TOPIC')
SLICES = os.environ.get('SLICES')
DURATION = os.environ.get('DURATION')

logger = get_logger(__name__)

producer = producer(KAFKA_BROKER_URL)


def slice_sound(path):
    try:
        sound: AudioSegment = AudioSegment.from_file(path, channel=1)
        logger.info(sound.duration_seconds)
    except FileNotFoundError as e:
        logger.error("file:{path} not found".format(path=path))
    except Exception as e:
        logger.error("exception occurs : {e}".format(e=e))


def process(data):
    path: str = data['path']
    if path.find('/backgrounds') != -1:
        slice_sound(path)


if __name__ == '__main__':
    consumer = consumer(KAFKA_BROKER_URL, TOPIC)

    for message in consumer:
        data: dict = message.value
        cid: str = data['cid']
        set_cid(cid)
        logger.info(data)
        process(data)
