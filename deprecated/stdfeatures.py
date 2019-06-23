import os
import sys
import csv
from Util import *
from mfcc import delta
from epd import *
# from python_speech_features import mfcc
import librosa


def main(start, end):
    dir_in = "speech_data"
    dir_out = "features_std"

    students = loads("students.txt")
    for student in students[start:end]:
        if not os.path.exists("%s/%s" % (dir_out, student)):
            os.mkdir("%s/%s" % (dir_out, student))

        for w in range(0, 20):
            for k in range(1, 21):
                # for k in range(11, 12):
                filename = "%s-%02d-%02d" % (student, w, k)
                print(filename)
                # with wave.open("%s/%s/%s.wav" % (dir_in, student, filename), "rb") as fin:
                #     params = fin.getparams()
                #     nframes = params[3]
                #     # print(nframes)

                #     str_data = fin.readframes(nframes)
                #     wave_data = np.fromstring(str_data, dtype=np.int16)

                #     C = mfcc(wave_data, samplerate=sample_rate,
                #              winlen=0.02, nfilt=26)
                #     D1 = delta(C, 2)
                #     D2 = delta(D1, 1)
                #     features = np.concatenate((C, D1, D2), axis=1)[3:C.shape[0]-3]
                wave_data, sr = librosa.load(
                    "%s/%s/%s.wav" % (dir_in, student, filename), sr=sample_rate)

                frames = list(
                    map(lambda frame: windowing(frame), getframes(preemphasis(wave_data))))
                (s1, e1, s2, e2, s3, e3, amps, zcr) = enddection(frames)

                C = librosa.feature.mfcc(
                    y=wave_data[s3*frame_step:e3*frame_step], sr=sr, n_mfcc=13)
                C = C.T
                D1 = delta(C, 2)
                D2 = delta(D1, 1)
                features = np.concatenate((C, D1, D2), axis=1)[3:C.shape[0]-3]
                with open("%s/%s/%s.csv" % (dir_out, student, filename), "w") as fout:
                    writer = csv.writer(fout, lineterminator="\n")
                    for line in features:
                        writer.writerow(line)


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        start = max(int(sys.argv[1]), 0)
        end = min(int(sys.argv[2])+1, 34)
    else:
        start = 0
        end = 34
    print(start, end)
    main(start, end)
