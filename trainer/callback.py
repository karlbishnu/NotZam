import time
from keras.callbacks import Callback

from common.log.logger import get_logger

logger = get_logger(__name__)


class KafkaCallback(Callback):
    def __init__(self, topics, send):
        self.topics = topics
        self.send = send
        self.resp = {}
        self.train = {}
        self.curr_epoch = {}
        self.epochs = []
        self.curr_batch = {}
        self.batchs = []

    def on_train_begin(self, logs={}):
        self.epochs = []
        self.train = {'elapsed': None, 'begin': time.time(), 'end': None, 'params': self.params, 'epochs': self.epochs}
        self.resp = {'train': self.train}
        self.kafka()

    def on_train_end(self, logs={}):
        self.train['end'] = time.time()
        self.train['elapsed'] = self.train['end'] - self.train['begin']
        for key, val in logs.items():
            self.train[key] = val
        self.kafka()

    def on_epoch_begin(self, epoch, logs={}):
        self.batchs = []
        self.curr_epoch = {'elapsed': None, 'begin': time.time(), 'end': None, 'batches': self.batchs}
        self.epochs.append(self.curr_epoch)
        self.kafka()

    def on_epoch_end(self, epoch, logs={}):
        self.curr_epoch['end'] = time.time()
        self.curr_epoch['elapsed'] = self.curr_epoch['end'] - self.curr_epoch['begin']
        for key, val in logs.items():
            self.curr_epoch[key] = val
        self.kafka()

    def on_batch_begin(self, batch, logs={}):
        self.curr_batch = {'elapsed': None, 'begin': time.time(), 'end': None}
        self.batchs.append(self.curr_batch)
        self.kafka()

    def on_batch_end(self, batch, logs={}):
        self.curr_batch['end'] = time.time()
        self.curr_batch['elapsed'] = self.curr_batch['end'] - self.curr_batch['begin']
        for key, val in logs.items():
            self.curr_batch[key] = val

        self.kafka()

    def kafka(self):
        for topic in self.topics:
            self.send(topic, self.resp)
