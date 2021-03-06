import unittest
import numpy as np

from trainer import training
from keras.models import Model, load_model
from keras.callbacks import BaseLogger
from pydub import AudioSegment
from scipy.io import wavfile


class TestTrainer(unittest.TestCase):
    def setUp(self):
        self.X = np.load("resources/XY_train/X.npy")
        self.Y = np.load("resources/XY_train/Y.npy")
        self.model = load_model('resources/model/tr_model.h5')
        self.X_dev = np.load("resources/XY_dev/X_dev.npy")
        self.Y_dev = np.load("resources/XY_dev/Y_dev.npy")

    def test_training(self):
        #np.save("resources/XY_train/X_copy.npy", self.X)
        callback = [BaseLogger()]
        model: Model = training(model=self.model, X=self.X, Y=self.Y, callbacks=callback)


        loss, acc = model.evaluate(self.X_dev, self.Y_dev)

        print(acc)  # 9312872886657715
        model.save('resources/model/test_model.h5')

    def test_model(self):
        model:Model = load_model('resources/model/tr_model.h5')
        model.summary()
        loss, acc = model.evaluate(self.X_dev, self.Y_dev)
        print(acc)

    def test_X(self):
        print(self.X.shape)
        print(len(self.X.shape))

    def test_pydub_comparison_with_scipy(self):
        path = 'resources/raw_data/dev/1.wav'
        _, wav = wavfile.read(path)
        wav = wav[:,0]
        audio = AudioSegment.from_file(path).split_to_mono()[0].get_array_of_samples()
        audio = np.array(audio)
        self.assertEqual(wav.shape, audio.shape)
        np.testing.assert_array_equal(wav, audio)
