import os

from common.audio.audio_utils import open_audio
from common.log.logger import get_logger

MIN_BACK_DURATION_SEC = os.environ.get('MIN_BACK_DURATION_SEC')

logger = get_logger(__name__)


def slice_sound(path, duration_sec=MIN_BACK_DURATION_SEC):
    res = []
    try:
        sound = open_audio(path).split_to_mono()[0]
        total_duration = len(sound)
        duration_millis = duration_sec * 1000

        for i in range(0, total_duration, duration_millis):
            target = "1-" + str(i) + ".wav"
            end = i+duration_millis-1 if i+duration_millis-1 < total_duration else total_duration
            buf = sound[i:end]
            buf.export(out_f=target, format="wav").close()
            res.append(target)

    except FileNotFoundError as e:
        logger.error("file:{path} not found".format(path=path))
    except Exception as e:
        logger.error("exception occurs : {e}".format(e=e))
    return res


def process(data):
    path: str = data['path']
    if path.find('/backgrounds') != -1:
        return slice_sound(path)

    return None
