import numpy as np 
import scipy
import h5py
from keras.layers import Embedding, recurrent, Activation, Dense, Flatten
import os
from keras import backend as K
from keras import metrics
from keras.callbacks import *
from keras.preprocessing import sequence
from keras.models import Sequential,load_model
from keras.layers import LSTM
from keras.layers.wrappers import Bidirectional
from keras.layers.core import Dropout
from keras.backend.tensorflow_backend import set_session
from util import *
import visual
import preprocess

from keras.preprocessing.text import one_hot


import tensorflow as tf
import matplotlib.pyplot as plt

# X_train,Y_train,X_test,Y_test = preprocess.dataz5ss()
X_train,Y_train,X_test,Y_test = preprocess.dataz3ss()


batch_size = 512

model = Sequential()
model.add(Embedding(4, 100, input_length=len(X_train[0])))
model.add(Bidirectional(LSTM(100, return_sequences=True, dropout=0.2, recurrent_dropout=0.2)))
# model.add(Attention(max_features))
model.add(Flatten())
model.add(Dense(512))
# model.add(Dropout(0.5))
model.add(Dense(5, activation='softmax'))
# try using different optimizers and different optimizer configs
print(model.summary())

model.compile(loss='mse',
              optimizer='adam',
              metrics=[det_coeff])
  

print('Train...')
history= model.fit(X_train, Y_train,
          batch_size=batch_size,
          epochs=5,
          validation_split=0.2
          )

visual.graph_epoch(history)

scores = model.evaluate(X_test, Y_test,verbose=1,batch_size=batch_size)

Y_pred=model.predict(X_test)

visual.pred_test_visual(Y_pred, Y_test, scores)