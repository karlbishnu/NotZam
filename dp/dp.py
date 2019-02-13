import os
import numpy as np
from datetime import date

from common.log.logger import get_logger
from common.audio.audio_utils import open_audio
from label import insert_ones
from overlay import insert_audio_clip
from common.audio.audio_utils import match_target_amplitude, graph_spectrogram


logger = get_logger(__name__)


def create_training_example(background, activates, negatives, Ty = 1375, file_name="train.wav"):
    """
    Creates a training example with a given background, activates, and negatives.

    Arguments:
    background -- a 10 second background audio recording
    activates -- a list of audio segments of the word "activate"
    negatives -- a list of audio segments of random words that are not "activate"

    Returns:
    x -- the spectrogram of the training example
    y -- the label at each time step of the spectrogram
    """

    # Set the random seed
    np.random.seed(18)

    # Make background quieter
    background = background - 20

    # Step 1: Initialize y (label vector) of zeros (≈ 1 line)
    y = np.zeros([1, Ty])

    # Step 2: Initialize segment times as empty list (≈ 1 line)
    previous_segments = []

    # Select 0-4 random "activate" audio clips from the entire list of "activates" recordings
    number_of_activates = np.random.randint(0, 5)
    random_indices = np.random.randint(len(activates), size=number_of_activates)
    random_activates = [activates[i] for i in random_indices]

    # Step 3: Loop over randomly selected "activate" clips and insert in background
    for random_activate in random_activates:
        # Insert the audio clip on the background
        background, segment_time = insert_audio_clip(background, random_activate, previous_segments)
        # Retrieve segment_start and segment_end from segment_time
        segment_start, segment_end = segment_time
        # Insert labels in "y"
        y = insert_ones(y, segment_end)

    # Select 0-2 random negatives audio recordings from the entire list of "negatives" recordings
    number_of_negatives = np.random.randint(0, 3)
    random_indices = np.random.randint(len(negatives), size=number_of_negatives)
    random_negatives = [negatives[i] for i in random_indices]

    # Step 4: Loop over randomly selected negative clips and insert in background
    for random_negative in random_negatives:
        # Insert the audio clip on the background
        background, _ = insert_audio_clip(background, random_negative, previous_segments)

    # Standardize the volume of the audio clip
    background = match_target_amplitude(background, -20.0)

    # Export new training example
    file_handle = background.export(file_name, format="wav")

    # Get and plot spectrogram of the new recording (background with superposition of positive and negatives)
    x = graph_spectrogram(background)

    return x, y


def load_backgrounds(data):
    backgrounds = []

    background_paths = data['backgroundSlices']
    logger.info("input: %s", background_paths)
    for background_path in background_paths:
        backgrounds.append(open_audio(background_path))

    return backgrounds


def load_all_waves(root):
    audios = {"audios":[]}
    for path, dirs, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith("mp3"):
                full_path = path+"/"+filename
                audio = open_audio(full_path)
                audios["audios"].append({"path": full_path, "audio": audio})

    return audios


def load_raw_audios(root):
    activates = load_all_waves(root+'/activates')
    negatives = load_all_waves(root+'/negatives')
    return activates, negatives


def process(data):
    root = 'assets'
    date_str = date.today().isoformat()
    path = root+'/'+date_str
    backgrounds = load_backgrounds(data)
    activates, negatives = load_raw_audios(root)

    for background in backgrounds:
        create_training_example(background, activates, negatives)
    os.makedirs(path, exist_ok=True)
    seq = len(os.listdir(path))

    return None
