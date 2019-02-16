import os
import numpy as np
from datetime import date

from common.log.logger import get_logger
from common.audio.audio_utils import open_audio
from label import insert_ones
from overlay import insert_audio_clip
from common.audio.audio_utils import match_target_amplitude, graph_spectrogram


logger = get_logger(__name__)


def create_training_example(background, activates, negatives, Ty = 1375):
    """
    Creates a training example with a given background, activates, and negatives.

    Arguments:
    background -- a 10 second background audio recording
    activates -- a list of tuple of file paths and audio segments of the word "activate"
    negatives -- a list of tuple of file paths and audio segments of random words that are not "activate"

    Returns:
    x:numpy.ndarray -- the spectrogram of the training example
    y:numpy.ndarray -- the label at each time step of the spectrogram
    background:pydub.AudioSegment - created raw data
    random_activates:list -- a list of inserted activates info. The tuple is composed of paths and AudioSegments
    random_negatives:list -- a list of inserted negatives info. The tuple is composed of paths and AudioSegments
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
        background, segment_time = insert_audio_clip(background, random_activate[1], previous_segments)
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
        background, _ = insert_audio_clip(background, random_negative[1], previous_segments)

    # Standardize the volume of the audio clip
    background = match_target_amplitude(background, -20.0)

    # Get and plot spectrogram of the new recording (background with superposition of positive and negatives)
    x = graph_spectrogram(background)

    return x, y, background, random_activates, random_negatives


def load_backgrounds(data):
    backgrounds = []

    background_paths = data['backgroundSlices']
    logger.info("input: %s", background_paths)
    for background_path in background_paths:
        backgrounds.append(open_audio(background_path))

    return backgrounds


def load_all_waves(root):
    audios = []
    for path, dirs, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith("mp3"):
                full_path = path+"/"+filename
                audio = open_audio(full_path)
                audios.append((full_path, audio))

    return audios


def load_raw_audios(root):
    activates = load_all_waves(root+'/activates')
    negatives = load_all_waves(root+'/negatives')
    return activates, negatives


def make_root_dir(asset_root):
    date_str = date.today().isoformat()
    date_path = asset_root + '/' + date_str
    os.makedirs(date_path, exist_ok=True)
    dir_seq = len(os.listdir(date_path))
    path = date_path + '/' + date_str + '-' + str.format('%03d' % dir_seq)
    os.makedirs(path, exist_ok=True)
    return path


def save(asset_root, X, Y, training_examples):
    saved_file_path_dict = {}
    path = make_root_dir(asset_root)

    xy_train_path = path + '/XY_train'
    os.makedirs(xy_train_path)
    x_path = xy_train_path+'/X.npy'
    y_path = xy_train_path+'/Y.npy'
    np.save(x_path, X)
    np.save(y_path, Y)

    saved_file_path_dict['x'] = x_path
    saved_file_path_dict['y'] = y_path

    raw_audios = []
    saved_file_path_dict['rawAudios'] = raw_audios
    raw_audio_root_path = path + '/raw_audios'
    os.makedirs(raw_audio_root_path)
    for i, training_example in enumerate(training_examples):
        raw_audio_path = raw_audio_root_path+'/'+str(i)+'.wav'
        training_example.export(raw_audio_path, format='wav')
        raw_audios.append(raw_audio_path)

    return saved_file_path_dict


def process(data):
    asset_root = 'assets'

    backgrounds = load_backgrounds(data)
    activates, negatives = load_raw_audios(asset_root)

    X = np.zeros((len(backgrounds), 5511, 101))
    Y = np.zeros((len(backgrounds), 1375))
    training_examples = []
    for i, background in enumerate(backgrounds):
        x, y, training_example, random_activates, random_negatives\
            = create_training_example(background, activates, negatives)
        logger.info('numOfActivates[{num_of_activates}], '
                    'randomActivates[{random_activates}], '
                    'numOfNegatives[{num_of_negatives}], '
                    'randomNegatives[{random_negatives}]'
            .format(num_of_activates=len(activates),
                    random_activates=random_activates,
                    num_of_negatives=len(negatives),
                    random_negatives=random_negatives))
        X[i] = x
        Y[i] = y
        training_examples.append(training_example)

    return save(asset_root, X, Y, training_examples)
