from Util import *


def subplot(data, s1, e1, s2, e2, s3, e3):
    Tmin = min(data)
    Tmax = max(data)
    h = plt.plot(data)
    plt.plot([s1, s1], [Tmin, Tmax], color='g')
    plt.plot([e1, e1], [Tmin, Tmax], color='g')
    plt.plot([s2, s2], [Tmin, Tmax], color='r')
    plt.plot([e2, e2], [Tmin, Tmax], color='r')
    plt.plot([s3, s3], [Tmin, Tmax], color='orange')
    plt.plot([e3, e3], [Tmin, Tmax], color='orange')
    return h


def plotends(figpath, wave_data, s1, e1, s2, e2, s3, e3, amps=None, zcrs=None):
    plt.clf()
    plt.subplot(3, 1, 1)
    h1 = subplot(wave_data, s1*frame_step, e1 * frame_step, s2 *
                 frame_step, e2*frame_step, s3*frame_step, (e3+1)*frame_step)
    plt.legend(h1, ["s(n)"])
    if amps is not None:
        plt.subplot(3, 1, 2)
        h2 = subplot(amps, s1, e1, s2, e2, s3, e3)
        plt.legend(h2, ["E"])
    if zcrs is not None:
        plt.subplot(3, 1, 3)
        h3 = subplot(zcrs, s1, e1, s2, e2, s3, e3)
        plt.legend(h3, ["Z"])
    plt.savefig(figpath)


def enddection(frames, lower=False):
    n = len(frames)
    zcrs = np.zeros(n)
    amps = np.zeros(n)
    for i in range(0, n):
        zcrs[i] = getzcrs(frames[i])
        amps[i] = getamps(frames[i])

    s1 = 10
    e1 = n-1
    maxamp = max(amps)
    mal = 0.15*maxamp
    if lower:
        mal = 0.1*maxamp
    step = 8
    if lower:
        step = 6
    r = 0
    while (s1 > e1 or (s1 == 10 and e1 == n-1)) and r < 2:
        s1 = 10
        e1 = n-1

        for i in range(10, n):
            if amps[i] > mal and np.mean(amps[i+int(step/2):i+step]) > mal:
                s1 = i
                break
        for i in range(n-1, 10, -1):
            if amps[i] > mal and np.mean(amps[i-step+1:i-int(step/2)+1]) > mal:
                e1 = i
                break
        step -= 2
        r += 1

    s2 = s1
    e2 = e1
    step = 5
    while s2 > 10 and np.mean(amps[s2-step:s2]) < np.mean(amps[s2:s2+step]):
        s2 -= 1
    while e2 < n-step and np.mean(amps[e2-step+1:e2+1]) > np.mean(amps[e2+1:e2+step+1]):
        e2 += 1
    s2 = max(s2, s1-3*step)
    e2 = min(e2, e1+3*step)

    maxzcr = max(zcrs)
    minzcr = min(zcrs[s2:e2+1])
    noise_zcr_avg = np.mean(zcrs[5:15])
    noise_zcr_std = np.std(zcrs[5:15], ddof=1)
    if noise_zcr_avg <= 2*minzcr:
        noise_zcr_avg = np.median(zcrs)
        if noise_zcr_avg <= 2*minzcr:
            noise_zcr_avg = maxzcr*0.5
    elif noise_zcr_avg >= maxzcr*0.7:
        noise_zcr_avg = maxzcr*0.7
    if noise_zcr_std < 1:
        noise_zcr_std = noise_zcr_avg/5
    k = 3
    if noise_zcr_std/noise_zcr_avg > 0.2:
        k = 1.5
    noise_low = noise_zcr_avg-k*noise_zcr_std
    noise_high = noise_zcr_avg+k*noise_zcr_std

    s3 = s2
    e3 = e2
    step = 8
    for i in range(s2-step, -1, -step):
        zcr_avg = np.mean(zcrs[i:i+step])
        if noise_low <= zcr_avg and zcr_avg <= noise_high:
            e3 = i+int(step/2)
            break
        s3 = i
    s3 = max(s3, s2-3*step)
    for i in range(e2+step, n, step):
        zcr_avg = np.mean(zcrs[i-step:i])
        if noise_low <= zcr_avg and zcr_avg <= noise_high:
            e3 = i-int(step/2)
            break
        e3 = i
    e3 = min(e3, e2+5*step)

    while s3 < s2 and amps[s3] < 0.05*maxamp:
        s3 += 1
    while e3 > e2 and amps[e3] < 0.05*maxamp:
        e3 -= 1

    return (s1, e1, s2, e2, s3, e3, amps, zcrs)


# def enddection_easy(frames):
#     n = len(frames)
#     zcrs = np.zeros(n)
#     amps = np.zeros(n)
#     for i in range(0, n):
#         zcrs[i] = getzcrs(frames[i])
#         amps[i] = getamps(frames[i])

#     energy_ave = np.mean(amps)

#     ML = np.mean(amps[:5])
#     MH = energy_ave / 4
#     ML = (ML + MH) / 4
#     zs = np.mean(zcrs[:5])

#     s1 = 10
#     e1 = n-1
#     for i in range(10, n):
#         if amps[i] > MH:
#             s1 = i
#             break
#     for i in range(n-1, 10, -1):
#         if amps[i] > MH:
#             e1 = i
#             break
#     s2 = s1
#     e2 = e1
#     while s2 > 10 and amps[s2] > ML:
#         s2 -= 1
#     while e2 < n and amps[e2] > ML:
#         e2 += 1

#     s3 = s2
#     e3 = e2
#     while s3 > 10 and zcrs[s3] > zs:
#         s3 -= 1
#     while e3 < n and zcrs[e3] > zs:
#         e3 += 1
#     return (s1, e1, s2, e2, s3, e3, amps, zcrs)


def cutwave(wave_data, isLower=False, figpath="tmp.png"):
    frames = [windowing(frame) for frame in getframes(wave_data)]
    (s1, e1, s2, e2, s3, e3, amps, zcrs) = enddection(frames, isLower)
    plotends(figpath, wave_data, s1, e1, s2, e2, s3, e3, amps, zcrs)
    return wave_data[s3*frame_step:(e3+1)*frame_step+1]


def main(start, end):
    dir_in = "speech_data"
    lowers = [14, 16, 19]

    students = loads("students.txt")
    for student in students[start:end]:
        endpoints = {}
        for w in range(0, 20):
            for k in range(1, 21):
                filename = "%s-%02d-%02d" % (student, w, k)
                filepath = "%s/%s/%s.wav" % (dir_in, student, filename)
                figpath = "figures/%s/%s.png" % (student, filename)

                isLower = False
                if w in lowers:
                    isLower = True

                wave_data = readprocessedwave(filepath)
                frames = [windowing(frame) for frame in getframes(wave_data)]

                (s1, e1, s2, e2, s3, e3, amps, zcrs) = enddection(frames, isLower)
                endpoints[filename] = [s1, e1, s2, e2, s3, e3]
                plotends(figpath, wave_data, s1, e1,
                         s2, e2, s3, e3, amps, zcrs)
        with open("epd/%s.json" % student, "w") as fout:
            fout.write(json.dumps(endpoints))


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        start = max(int(sys.argv[1]), 0)
        end = min(int(sys.argv[2])+1, 33)
    else:
        start = 0
        end = 33
    print(start, end)
    main(start, end)
