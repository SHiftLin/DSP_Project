from Util import inf
import random


def initcenters(K, n):
    idx = list(range(0, n))
    random.shuffle(idx)
    return idx[:K]


def kmeans(points, dist, K, round=100):
    n = len(points)
    centers = initcenters(K, n)

    for r in range(0, round):
        print("round %d" % r)
        cluster = [[centers[k]] for k in range(0, K)]
        for x in range(0, n):
            dist_min = inf
            c = 0
            for k in range(0, K):
                if dist[x][centers[k]] < dist_min:
                    dist_min = dist[x][centers[k]]
                    c = k
            cluster[c].append(x)

        centers = []
        for k in range(0, K):
            dist_min = inf
            center = cluster[k][0]
            for x in cluster[k]:
                dist_sum = 0
                for y in cluster[k]:
                    dist_sum += dist[x][y]
                if dist_sum < dist_min:
                    dist_min = dist_sum
                    center = x
            centers.append(center)

    return [points[center] for center in centers]
