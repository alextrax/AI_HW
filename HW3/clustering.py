#!/usr/bin/env python
#coding:utf-8

from sklearn.utils import shuffle
from sklearn.cluster import KMeans
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt

ncolors = 3


trees = misc.imread("trees.png")
trees = np.array(trees, dtype=np.float64) / 255

w, h, d = tuple(trees.shape)
trees_2d = np.reshape(trees, (w * h, d))
kmeans = KMeans(n_clusters=ncolors, random_state=0).fit(trees_2d)
quantized = kmeans.predict(trees_2d)
 

d = kmeans.cluster_centers_.shape[1]
image = np.zeros((w, h, d))
index = 0
for i in range(w):
    for j in range(h):
        image[i][j] = kmeans.cluster_centers_[quantized[index]]
        index += 1

plt.imshow(image)    
plt.show()