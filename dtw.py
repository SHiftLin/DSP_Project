import os
import csv
from Util import *
from kmeans import kmeans

dir_in = "features"
dir_table = "dtwtable"
dir_model = "dtw"
word_num = 20
cluster_num = 10


def cost(a, b):
    res = 0
    for x, y in zip(a, b):
        res += (x-y)*(x-y)
    return res


def dtw(A, B):
    n = len(A)+2
    m = len(B)+2
    if n > 0:
        p = len(A[0])
    else:
        p = 1
    A = np.concatenate((np.zeros((1, p)), A, np.zeros((1, p))))
    B = np.concatenate((np.zeros((1, p)), B, np.zeros((1, p))))
    f = [[0]*m for i in range(0, n)]
    for i in range(1, n):
        f[i][0] = f[i-1][0]+cost(A[i], B[0])
    for j in range(1, m):
        f[0][j] = f[0][j-1]+cost(A[0], B[j])
    for i in range(1, n):
        for j in range(1, m):
            f[i][j] = min(f[i-1][j-1], f[i-1][j], f[i][j-1])+cost(A[i], B[j])
    return f[n-1][m-1]


def disttable(points):
    n = len(points)
    dist = [[0]*n for i in range(0, n)]
    for i in range(0, n):
        dist[i][i] = 0
        for j in range(i+1, n):
            dist[i][j] = dtw(points[i], points[j])
            dist[j][i] = dist[i][j]
    return dist


def readtable(w, n):
    table = np.loadtxt("%s/%d.csv" % (dir_table, w), delimiter=',')
    table = table[:, :n]
    table = table[:n]
    return table


def calcScore(centers, obseq):
    d = inf
    for center in centers:
        d = min(d, dtw(center, obseq))
    return -d


students = loads("students.txt")
models = []
word_obseqs_test = []
word_centers = []
for w in range(0, word_num):
    obseqs = []
    for student in students:
        for k in range(1, 21):
            filename = "%s-%02d-%02d" % (student, w, k)
            obseq = np.loadtxt("%s/%s/%s.csv" %
                               (dir_in, student, filename), delimiter=',')
            obseqs.append(obseq)

    obseqs_train = obseqs[:-100]
    word_obseqs_test.append(obseqs[-100:])

    word_centers.append(
        kmeans(obseqs_train, readtable(w, len(obseqs_train)), 10))
    
    print("model %d finished" % w)

reg = []
for word in range(0, word_num):
    reg.append([0]*word_num)
    obseqs_test = word_obseqs_test[word]
    for obseq in obseqs_test:
        decision = 0
        score_max = -inf
        for i in range(0, word_num):
            score = calcScore(word_centers[i], obseq)
            if score > score_max:
                score_max = score
                decision = i
        reg[word][decision] += 1

# print(reg)
cnt = 0
acc = 0
for word in range(0, word_num):
    print(reg[word])
    acc += reg[word][word]
    cnt += sum(reg[word])
print(1.0*acc/cnt)
