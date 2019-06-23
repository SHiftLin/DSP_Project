import os
import sys
import csv
import json
from Util import *
from epd import enddection, plotends
from mfcc import MFCC, delta
from lpc import LPC

dir_in = "speech_data"
dir_out = "features"
dir_fig = "figures"
endpoints = {}


def getfeatures(filepath, figpath="tmp.png", cached=False):
    wave_data = readprocessedwave(filepath)
    frames = [windowing(frame) for frame in getframes(wave_data)]

    if not cached:
        (s1, e1, s2, e2, s3, e3, amps, zcrs) = enddection(frames)
        plotends(figpath, wave_data, s1, e1, s2, e2, s3, e3, amps, zcrs)
    else:
        filename = filepath.split('/')[-1][:-4]
        (student, w, k) = filename.split('-')
        with open("epd/%s.json" % student, 'r') as fin:
            endpoints = json.loads(fin.read())
        (s1, e1, s2, e2, s3, e3) = endpoints[filename]

    C = MFCC(frames[s3:e3+1], cnt=20)
    D1 = delta(C, 2)
    D2 = delta(D1, 1)
    A = LPC(frames[s3:e3+1], p=10)
    features = np.concatenate((C, D1, D2, A), axis=1)[3:C.shape[0]-3]
    # amps[s3:e3+1][:, np.newaxis]

    return features


def main(start, end):
    students = loads("students.txt")
    for student in students[start:end]:
        if not os.path.exists("%s/%s" % (dir_out, student)):
            os.mkdir("%s/%s" % (dir_out, student))
        if not os.path.exists("%s/%s" % (dir_fig, student)):
            os.mkdir("%s/%s" % (dir_fig, student))
        
        print(student)
        for w in range(0, 20):
            for k in range(1, 21):
                filename = "%s-%02d-%02d" % (student, w, k)
                features = getfeatures(("%s/%s/%s.wav") %
                                       (dir_in, student, filename), cached=True)
                with open("%s/%s/%s.csv" % (dir_out, student, filename), "w") as fout:
                    writer = csv.writer(fout, lineterminator="\n")
                    for line in features:
                        writer.writerow(line)


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        start = max(int(sys.argv[1]), 0)
        end = min(int(sys.argv[2])+1, 33)
    else:
        start = 0
        end = 33
    print(start, end)
    main(start, end)
