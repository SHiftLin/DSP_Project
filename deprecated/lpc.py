from Util import *
from scipy import linalg


def calcR(sw, k):
    n = len(sw)
    res = 0
    for i in range(k, n):
        res += sw[i]*sw[i-k]
    return res


def singleLPC(sw, p=20):
    R = np.zeros(p+1)
    A = np.zeros((p, p))
    B = np.zeros(p)
    for j in range(0, p+1):
        R[j] = calcR(sw, j)
    if max(R) == 0:
        return np.zeros(p)
    for i in range(0, p):
        for j in range(0, p):
            A[i][j] = R[abs(i-j)]
        B[i] = R[i+1]
    return linalg.solve(A, B)


def LPC(frames, p=20):
    A = np.zeros((len(frames), p))
    for i, frame in enumerate(frames):
        A[i] = singleLPC(frame, p)
    return A
