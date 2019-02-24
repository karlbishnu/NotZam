from keras.callbacks import ProgbarLogger, BaseLogger, Callback

from common.log.logger import get_logger

logger = get_logger(__name__)

class KafkaCallback(Callback):
    def __init__(self, topics, send):
        self.topics = topics
        self.send = send

    def on_train_begin(self, logs={}):
        logger.info(str.format("topics={topics}, params={params}", topics=str(self.topics), params=str(self.params)))
        for topic in self.topics:
            self.send(topic, self.params)


    def on_train_end(self, logs={}):
        #self.params <class 'dict'>: {'batch_size': 5, 'epochs': 1, 'steps': None, 'samples': 26, 'verbose': 0, 'do_validation': False, 'metrics': ['loss', 'acc']}
        print(self)
        return

    def on_epoch_begin(self, epoch, logs={}):
        print(self)
        print(epoch)
        return

    def on_epoch_end(self, epoch, logs={}):
        print(self)
        print(epoch)
        #<class 'dict'>: {'loss': 0.06660731781560641, 'acc': 0.9757202657369467}
        return

    def on_batch_begin(self, batch, logs={}):
        print(self)
        print(batch)
        #<class 'dict'>: {'batch': 3, 'size': 5}
        return

    def on_batch_end(self, batch, logs={}):
        print(self)
        print(batch)
        #logs = {'batch': 0, 'size': 5, 'loss': 0.08930002, 'acc': 0.97367275}
        #<class 'dict'>: {'batch': 1, 'size': 5, 'loss': 0.07182132, 'acc': 0.96770906}
        #<class 'dict'>: {'batch': 2, 'size': 5, 'loss': 0.034722205, 'acc': 0.9870545}
        return