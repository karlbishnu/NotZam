from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt


def open_audio(path):
    return AudioSegment.from_file(path)


# Used to standardize volume of audio clip
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def get_spectrogram(ndarray):
    plt.subplot(2, 1, 1)
    nfft = 200  # Length of each window segment
    fs = 8000  # Sampling frequencies
    noverlap = 120  # Overlap between windows
    pxx, freqs, bins, im = plt.specgram(ndarray, nfft, fs, noverlap=noverlap)
    return pxx


def graph_spectrogram(sound: AudioSegment):
    mono = sound.split_to_mono()[0].get_array_of_samples()
    return get_spectrogram(np.array(mono))


def graph_spectrogram_from_file(file: str):
    sound = open_audio(file)
    return graph_spectrogram(sound)
