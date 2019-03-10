import unittest
import numpy as np
from pydub import AudioSegment
from word_trigger import fit_audio, make_output


class WordTriggerTest(unittest.TestCase):
    def test_fit_audio_padding(self):
        audio = AudioSegment.silent(duration=1)
        output = fit_audio(audio)
        self.assertAlmostEqual(10, output.duration_seconds, delta=0.001)

    def test_fit_audio_trimming(self):
        audio = AudioSegment.silent(duration=20000)
        output = fit_audio(audio)
        self.assertAlmostEqual(10, output.duration_seconds, delta=0.001)

    def test_make_output(self):
        predictions = np.zeros((1, 1375, 1))
        predictions[0][int(1375/2)] = 1
        audio = AudioSegment.silent(duration=5000)
        output = make_output(audio, predictions)
        self.assertEquals(1, len(output))
        self.assertAlmostEqual(2500, output[0], delta=2)

    def test_make_output2(self):
        predictions = np.zeros((1, 1375, 1))
        predictions[0][int(1375 / 3)] = 1
        audio = AudioSegment.silent(duration=5000)
        output = make_output(audio, predictions)
        self.assertEquals(1, len(output))
        self.assertAlmostEqual(1666, output[0], delta=2)