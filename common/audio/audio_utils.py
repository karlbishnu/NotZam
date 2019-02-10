from pydub import AudioSegment
import matplotlib.pyplot as plt


def open_audio(path):
    return AudioSegment.from_file(path)


# Used to standardize volume of audio clip
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def get_spectrogram(binary):
    nfft = 256  # Length of each window segment
    fs = 8000  # Sampling frequencies
    noverlap = 120  # Overlap between windows
    pxx, freqs, bins, im = plt.specgram(binary, nfft, fs, noverlap=noverlap)
    return pxx


def graph_spectrogram(sound: AudioSegment):
    return get_spectrogram(sound.get_array_of_samples()[0::])


def graph_spectrogram_from_file(file: str):
    sound = AudioSegment.from_file(file, channels=1)
    return graph_spectrogram(sound)
