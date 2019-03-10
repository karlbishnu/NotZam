import numpy as np

from keras.engine.saving import load_model
from pydub import AudioSegment
from common.audio.audio_utils import graph_spectrogram, open_audio

model = load_model('model/tr_model.h5')


def predict(x):
    x = graph_spectrogram(x)
    x = x.swapaxes(0, 1)
    x = np.expand_dims(x, axis=0)
    return model.predict(x)


def fit_audio(segment):
    padding = AudioSegment.silent(duration=10000)
    segment = segment[:10000]
    segment = padding.overlay(segment)
    segment = segment.set_frame_rate(44100)
    return segment


def make_output(x, predictions):
    Ty = predictions.shape[1]
    threshold = 0.5
    consecutive_timesteps = 0
    spots = []
    for i in range(Ty):
        consecutive_timesteps += 1
        if predictions[0, i, 0] > threshold and consecutive_timesteps > 75:
            spots.append(((i / Ty) * x.duration_seconds)*1000)
            consecutive_timesteps = 0

    return spots


def process(data):
    segment = open_audio(data['filePath'])
    x = fit_audio(segment)
    predictions = predict(x)
    return make_output(segment, predictions)
