from Util import *
from scipy.fftpack import fft as FFT
from scipy.fftpack import dct as DCT


def hz2mel(hz):
    return 2595 * np.log10(1 + hz / 700.0)


def mel2hz(mel):
    return 700 * (10**(mel/2595.0) - 1)


def singleMFCC(frame, L=26, hz_low=0, hz_high=sample_rate/2, cnt=13, nfft=256):
    X = FFT(frame, n=nfft)
    P = abs(X)*abs(X)/nfft
    mel = np.linspace(hz2mel(hz_low), hz2mel(hz_high), L+2)
    hz = mel2hz(mel)
    f = np.ceil(nfft*hz/sample_rate).astype(np.int16)
    s = np.zeros(L)
    for i in range(0, L):
        for j in range(f[i], f[i+1]):
            s[i] += P[j]*(j-f[i])/(f[i+1]-f[i])
        for j in range(f[i+1], f[i+2]):
            s[i] += P[j]*(f[i+2]-j)/(f[i+2]-f[i+1])
        s[i] = math.log(s[i]+1e-5)
    cofs = DCT(s, norm='ortho')[:cnt]
    return cofs


def MFCC(frames, L=22, hz_low=0, hz_high=sample_rate/2, cnt=13):
    C = np.zeros((len(frames), cnt))
    for i, frame in enumerate(frames):
        C[i] = singleMFCC(frame, L, hz_low, hz_high, cnt)
    return C


def delta(C, n):  # [cofs_frame1,cofs_frame2,....,] n*13
    nframes = C.shape[0]
    D = np.zeros(C.shape)
    for i in range(0, nframes):
        if i < n:
            D[i] = C[i+n]
        elif i+n >= nframes:
            D[i] = -C[i-n]
        else:
            D[i] = C[i+n]-C[i-n]
    return D
