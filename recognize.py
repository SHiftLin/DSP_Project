import time
import pyaudio
import wave
import pickle
import numpy as np
from multiprocessing import Process
from Util import *
from epd import cutwave
from getfeatures import getfeatures
from hmmlearn import hmm

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "record.wav"
word_num = 20
wordlist = ["数字", "语音", "语言", "识别", "中国", "总工", "北京", "背景", "上海", "商行", "复旦", "饭店",
            "Speech", "Speaker", "Signal", "Process", "Print", "Open", "Close", "Project"]


def useCNN():
    wave_data = padzeros(
        cutwave(readprocessedwave(WAVE_OUTPUT_FILENAME)), 15000)
    wave_data = np.expand_dims(np.expand_dims(wave_data, axis=0), axis=-1)

    import keras
    from keras.models import load_model
    sys.stderr = open(os.devnull, 'w')
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'  # 只显示 Error

    model = load_model('cnn/19-0.90.hdf5')
    decision = np.argmax(model.predict(wave_data, batch_size=124))
    print(wordlist[decision])


def useGMMHMM():
    features = getfeatures(WAVE_OUTPUT_FILENAME)
    features = np.concatenate(
        (features[:, 0:13], features[:, 20:33], features[:, 40:53]), axis=1)

    score_max = -inf
    decision = 0
    for w in range(0, word_num):
        with open("gmmhmm/%d.pkl" % w, "rb") as fmodel:
            model = pickle.load(fmodel)
        score = model.score(features)
        if score > score_max:
            score_max = score
            decision = w
    print(wordlist[decision])


def prompt():
    time.sleep(0.3)
    print("*** start recording")


p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK)

proc = Process(target=prompt)
proc.start()
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
proc.join()
print("*** done")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

useCNN()
#
