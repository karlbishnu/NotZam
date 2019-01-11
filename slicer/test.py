import unittest
from unittest.mock import patch


class KafkaMessage:
    def __init__(self, count):
        self.value = {"cid": count, "path": "/test"}


def _mock_kafka_msg():
    count = 0
    while count < 10:
        message = KafkaMessage(count)
        yield message
        count += 1


class SliceTests(unittest.TestCase):

    @patch('common.mq.kafka.producer', return_value=None)
    def test_runs(self, producer):
        import app
        app.slice_sound(None)


if __name__ == '__main__':
    unittest.main()
