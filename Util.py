import os
import sys
import csv
import json
import math
import wave
import numpy as np
import matplotlib.pyplot as plt

inf = 1 << 60
sample_rate = 16000
frame_len = 0.02
frame_size = int(frame_len*sample_rate)
frame_step = int(frame_size/2)


def loads(filename):
    data = []
    with open(filename, "r") as fin:
        for line in fin:
            data.append(line[:-1])
    return data


def plot(data):
    n = len(data)
    #time = np.arange(0, n) * (1.0 / sample_rate)
    plt.plot(data)
    plt.show()


def normalize(data):
    return data/max(abs(data))


def preemphasis(wave_data):
    n = len(wave_data)
    res = []
    q = 0
    alpha = 0.95
    for p in wave_data:
        res.append(p-alpha*q)
        q = p
    return res


def getframes(wave_data):
    n = len(wave_data)
    frames = []
    for i in range(0, n-frame_size+1, frame_step):
        frame = []
        for j in range(0, frame_size):
            frame.append(wave_data[i+j])
        frames.append(frame)
    return frames


def readoriginwave(filepath):
    with wave.open(filepath, "rb") as fin:
        params = fin.getparams()
        nframes = params[3]

        wave_data = np.fromstring(fin.readframes(nframes), dtype=np.int16)
    return normalize(wave_data)


def readprocessedwave(filepath):
    with wave.open(filepath, "rb") as fin:
        params = fin.getparams()
        nframes = params[3]

        wave_data = np.fromstring(fin.readframes(nframes), dtype=np.int16)
    return preemphasis(normalize(wave_data))


def hamming(i, n):
    return 0.54-0.46*math.cos(2*math.pi*i/(n-1))


def windowing(frame):
    n = len(frame)
    res = []
    for i, x in enumerate(frame):
        res.append(hamming(i, n)*x)
    return res


def sign(x):
    if x == 0:
        return 0
    if x > 0:
        return 1
    return -1


def getzcrs(sw):
    res = 0
    q = 0
    for p in sw:
        res += 0.5*abs(sign(p)-sign(q))
        q = p
    return res


def getamps(sw):
    res = 0
    for p in sw:
        res += abs(p)
    return res


def getenergy(sw):
    res = 0
    for p in sw:
        res += p*p
    return res


def padzeros(data, N=10000):
    n = len(data)
    if n < N:
        return np.concatenate((data, np.zeros(N-n)))
    else:
        return data[:N]
