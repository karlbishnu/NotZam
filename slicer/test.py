import os
import unittest
from unittest.mock import patch
from pydub import AudioSegment


class SliceTests(unittest.TestCase):

    def test_runs(self):
        import slicer
        path = "test-source/noise.wav"
        duration = 10
        res = slicer.slice_sound(path, duration)

        sound: AudioSegment = AudioSegment.from_file(path, channel=1)
        self.assertEqual(int(int(sound.duration_seconds)/duration)+1, len(res))
        for file in res:
            os.remove(file)

    @patch('common.mq.kafka.producer', return_value=None)
    @patch('os.environ.get', return_value='topic1, topic2 , topic3')
    def test_parsing_env(self, producer, env_topic):
        expected = ['topic1', 'topic2', 'topic3']
        from app import PRODUCER_TOPICS
        self.assertListEqual(expected, PRODUCER_TOPICS)

    @patch('common.mq.kafka.producer', return_value=None)
    @patch('os.environ.get', return_value='topic1')
    def test_parsing_env_single_value(self, producer, env_topic):
        expected = ['topic1']
        from app import PRODUCER_TOPICS
        self.assertListEqual(expected, PRODUCER_TOPICS)


if __name__ == '__main__':
    unittest.main()
