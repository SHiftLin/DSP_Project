import os
import numpy as np
import matplotlib.pyplot as plt

os.system("g++ kmeans_test.cpp -o kmeans_test")
os.system("./kmeans_test")

clf = []
initc = []
centers = []
with open("kmeans_test_result.txt", "r") as fin:
    for i, line in enumerate(fin):
        point = []
        for item in line.split(','):
            x, y = item.split()
            point.append([float(x), float(y)])
        if i == 0:
            initc = np.asarray(point)
        elif i == 1:
            centers = np.asarray(point)
        else:
            clf.append(point)

for cluster in clf:
    point = np.asarray(cluster)
    x = point[:, 0]
    y = point[:, 1]
    plt.scatter(x, y, s=10)

x = initc[:, 0]
y = initc[:, 1]
plt.scatter(x, y, marker='+', s=100)

x = centers[:, 0]
y = centers[:, 1]
plt.scatter(x, y, marker='x', s=100)
plt.show()
