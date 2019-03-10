import numpy as np

from keras.models import Model, load_model
from keras.optimizers import Adam
from callback import KafkaCallback


def training(model=None, X=None, Y=None, callbacks = []):
    opt = Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, decay=0.01)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=["accuracy"])
    model.fit(X, Y, batch_size=5, epochs=1, callbacks=callbacks, verbose=0)

    return model


def process(data):
    callback = data['callback']
    kafka_callback = KafkaCallback(callback['topics'], callback['send'])

    X: np.ndarray = np.load("resources/XY_train/X.npy")
    Y: np.ndarray = np.load("resources/XY_train/Y.npy")
    model: Model = load_model('resources/model/tr_model.h5')
    training(model, X, Y, [kafka_callback])
