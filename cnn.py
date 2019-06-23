import time
import random
import keras
from keras.models import Sequential, load_model
from keras.layers import Conv1D, Dense, MaxPooling1D
from keras.layers.core import Flatten
from keras.callbacks import ModelCheckpoint
from Util import *
from epd import plotends
import pickle

# dir_in = "speech_data"
dir_in = "speech_data"
dir_model = "cnn"
word_num = 20
M = 15000

# students = loads("students.txt")
# X = np.zeros((33*20*20, M))
# Y = np.zeros(33*20*20)
# cnt = 0
# idx = [i for i in range(0, X.shape[0])]
# random.shuffle(idx)
# for student in students:
#     with open("epd/%s.json" % student, 'r') as fin:
#         endpoints = json.loads(fin.read())
#     for w in range(0, word_num):
#         for k in range(1, 21):
#             filename = "%s-%02d-%02d" % (student, w, k)
#             wave_data = readprocessedwave(
#                 ("%s/%s/%s.wav") % (dir_in, student, filename))
#             (s1, e1, s2, e2, s3, e3) = endpoints[filename]
#             # X[idx[cnt]] = padzeros(
#             #     wave_data[s3*frame_step:(e3+1)*frame_step+1], M)
#             # Y[idx[cnt]] = w
#             X[cnt] = padzeros(
#                 wave_data[s3*frame_step:(e3+1)*frame_step+1], M)
#             Y[cnt] = w
#             cnt += 1
# X = np.expand_dims(X, axis=-1)

# X_test = X[-1200:]
# Y_test = Y[-1200:]
# X = X[:-1200]
# Y = Y[:-1200]

# with open("%s/cnn_xtrain.pkl" % dir_model, "wb") as finput:
#     pickle.dump(X, finput)
# with open("%s/cnn_ytrain.pkl" % dir_model, "wb") as finput:
#     pickle.dump(Y, finput)
# with open("%s/cnn_xtest.pkl" % dir_model, "wb") as finput:
#     pickle.dump(X_test, finput)
# with open("%s/cnn_ytest.pkl" % dir_model, "wb") as finput:
#     pickle.dump(Y_test, finput)


with open("%s/cnn_xtrain.pkl" % dir_model, "rb") as finput:
    X = pickle.load(finput)
with open("%s/cnn_ytrain.pkl" % dir_model, "rb") as finput:
    Y = pickle.load(finput)
with open("%s/cnn_xtest.pkl" % dir_model, "rb") as finput:
    X_test = pickle.load(finput)
with open("%s/cnn_ytest.pkl" % dir_model, "rb") as finput:
    Y_test = pickle.load(finput)

# with open("%s/cnn_xinput.pkl" % dir_model, "wb") as finput:
#     pickle.dump(X, finput)
# with open("%s/cnn_yinput.pkl" % dir_model, "wb") as finput:
#     pickle.dump(Y, finput)


# with open("%s/cnn_xinput.pkl" % dir_model, "rb") as finput:
#     X = pickle.load(finput)
# with open("%s/cnn_yinput.pkl" % dir_model, "rb") as finput:
#     Y = pickle.load(finput)
# print(X.shape)
# print(Y.shape)

Y = keras.utils.to_categorical(Y, word_num)

model = Sequential()
model.add(Conv1D(128, kernel_size=5, activation='relu',
                 input_shape=(X.shape[1], X.shape[2])))
model.add(MaxPooling1D(pool_size=5))
model.add(Conv1D(64, kernel_size=5, activation='relu'))
model.add(MaxPooling1D(pool_size=5))
model.add(Conv1D(32, kernel_size=5, activation='relu'))
model.add(MaxPooling1D(pool_size=5))
model.add(Conv1D(32, kernel_size=5, activation='relu'))
model.add(MaxPooling1D(pool_size=5))
model.add(Conv1D(32, kernel_size=5, activation='relu'))
model.add(MaxPooling1D(pool_size=5))
model.add(Flatten())
model.add(Dense(20, activation='softmax'))
model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

filepath = "cnn/{epoch:02d}-{val_acc:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True,
                             mode='max')
callbacks_list = [checkpoint]

t1 = time.time()

model.fit(X, Y, batch_size=124, epochs=20, verbose=1,
          validation_split=0.1, callbacks=callbacks_list)

# model = load_model('cnn/17-0.91.hdf5')

t2 = time.time()

Y_pred = model.predict(X_test, batch_size=124)
reg = [[0]*word_num for i in range(0, word_num)]
acc = 0
cnt = 0
for p, y in zip(Y_pred, Y_test):
    d = np.argmax(p)
    reg[int(y)][d] += 1
    cnt += 1
    if d == int(y):
        acc += 1
for line in reg:
    print(line)
print(1.0*acc/cnt)
t3 = time.time()
print(t3-t2, (t3-t2)/1200)
