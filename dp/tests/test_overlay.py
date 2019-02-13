import unittest
from unittest.mock import patch
from overlay import is_overlapping, insert_audio_clip
from pydub import AudioSegment
from common.audio.audio_utils import open_audio, graph_spectrogram


class TestOverlay(unittest.TestCase):
    def setUp(self):
        self.background: AudioSegment = open_audio('test-asset/backgrounds/1.mp3')
        self.activate: AudioSegment = open_audio('test-asset/activates/3_act2.wav')

    def test_overlapped(self):
        self.assertTrue(is_overlapping((2305, 2950), [(824, 1532), (1900, 2305), (3424, 3656)]))

    def test_not_overlapped(self):
        self.assertFalse(is_overlapping((950, 1430), [(2000, 2550), (260, 949)]))

    @patch('numpy.random.randint', return_value=2254)
    def test_insert_audio_clip(self, rand):
        audio_clip, segment_time = insert_audio_clip(self.background, self.activate, [(3790, 4400)])
        self.assertEqual((2254, 3169), segment_time)
        self.assertEqual(len(self.background), len(audio_clip))

    def test_spectrogram(self):
        print(len(self.background.get_array_of_samples()[0::]))
        print(len(self.background.get_array_of_samples()[1:]))
        print(graph_spectrogram(self.background).shape)

