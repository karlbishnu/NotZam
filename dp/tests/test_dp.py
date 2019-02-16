import unittest
from unittest.mock import patch

from dp import load_raw_audios, make_root_dir, save
import os
import numpy as np
from shutil import rmtree


def remove_files(root):
    for path, dirs, files in os.walk(root):
        for file in files:
            os.remove(path+'/'+file)

def remove_dirs(root):
    for path, dirs, _ in os.walk(root):
        pass

def remove_dir(root):
    remove_files(root)
    remove_dirs(root)

class TestDp(unittest.TestCase):
    def setUp(self):
        self.asset_root = 'test-asset'

    def test_load_raw_audios(self):
        activates = 0
        item = 0
        raw_data_root = self.asset_root + '/raw-data'
        path, audio = load_raw_audios(raw_data_root)[activates][item]

        self.assertTrue(path.startswith(raw_data_root+'/activates'))
        self.assertNotEqual(-1, str(audio).find('pydub.audio_segment.AudioSegment'))

    def test_json_tuple(self):
        import json
        print(json.dumps((1, 2)))

    def test_nd_array(self):
        X = np.zeros((2, 5511, 101))
        X[1] = np.ones((5511, 101))
        print(X)

    def test_logger(self):
        from common.log.logger import get_logger
        logger = get_logger('test')
        logger.info('test={mesg}'
                    'sss={mesg}'.format(mesg='뭐임?'))

    def test_make_root_dir(self):
        path = make_root_dir('test-asset')
        self.assertTrue(os.access(path, os.F_OK|os.W_OK|os.R_OK))
        os.removedirs(path)

    def test_save(self):
        X = np.zeros((2, 5511, 101))
        Y = np.zeros((1, 1375))
        training_example_path = self.asset_root + '/training-example'
        saved_file_paths = save(training_example_path, X, Y,[])

        for key in ['x', 'y', 'rawAudios']:
            self.assertTrue(saved_file_paths.__contains__(key))

        for path in os.listdir(training_example_path):
            rmtree(training_example_path+'/'+path)

