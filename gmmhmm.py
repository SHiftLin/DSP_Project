import os
import time
import numpy as np
import pickle
import random
from hmmlearn import hmm
from Util import *

dir_in = "features"
dir_model = "gmmhmm"
word_num = 20
test_size = 3*20

t1 = time.time()

students = loads("students.txt")
models = []
word_obseqs_test = []
for w in range(0, word_num):
    obseqs = []
    lengths = []
    for student in students:
        for k in range(1, 21):
            filename = "%s-%02d-%02d" % (student, w, k)
            obseq = np.loadtxt("%s/%s/%s.csv" %
                               (dir_in, student, filename), delimiter=',')
            obseq = np.concatenate(
                (obseq[:, :13], obseq[:, 20:33], obseq[:, 40:53]), axis=1)
            # if(obseq.shape[0] < 1):
            #     obseq = obseqs[-1]
            if len(obseq.shape) == 1:
                obseq = obseq[np.newaxis, :]
            obseqs.append(obseq)
            lengths.append(len(obseq))

    obseqs_train = obseqs
    random.shuffle(obseqs)
    word_obseqs_test.append(obseqs[:int(len(obseqs)/10)])
    #obseqs_train = obseqs[:-test_size]
    #lengths = lengths[:-test_size]
    # word_obseqs_test.append(obseqs[-test_size:])

    model = hmm.GMMHMM(n_components=5, n_mix=5,
                       covariance_type='diag', n_iter=1000)
    model.fit(np.concatenate(obseqs_train), lengths)
    models.append(model)
    with open("%s/%d_all.pkl" % (dir_model, w), "wb") as fmodel:
        pickle.dump(model, fmodel)
    print("model %d finished" % w)

t2 = time.time()

reg = []
for word in range(0, word_num):
    reg.append([0]*word_num)
    obseqs_test = word_obseqs_test[word]
    for obseq in obseqs_test:
        decision = 0
        score_max = -inf
        for i in range(0, word_num):
            score = models[i].score(obseq)
            if score > score_max:
                score_max = score
                decision = i
        reg[word][decision] += 1

# print(reg)
cnt = 0
acc = 0
for word in range(0, word_num):
    acc += reg[word][word]
    cnt += sum(reg[word])
    print(reg[word], 1.0*reg[word][word]/sum(reg[word]))
print(1.0*acc/cnt)

t3 = time.time()

print(t2-t1, t3-t2, 1.0*(t3-t2)/(test_size*20))
