import os
import unittest
from unittest.mock import patch

from pydub import AudioSegment


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
        path = "test-source/noise.wav"
        duration = 10
        res = app.slice_sound(path, duration)

        sound: AudioSegment = AudioSegment.from_file(path, channel=1)
        self.assertEqual(int(int(sound.duration_seconds)/duration)+1, len(res))
        for file in res:
            os.remove(file)

    def test_parsing_env(self):
        expected = ['topic1', 'topic2', 'topic3']
        res = [topic.strip() for topic in str('topic1, topic2 ,topic3').split(",")]
        self.assertListEqual(expected, res)



if __name__ == '__main__':
    unittest.main()
