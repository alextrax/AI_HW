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
trees_rdm = shuffle(trees_2d, random_state=0)[:1000]
kmeans = KMeans(n_clusters=ncolors, random_state=0).fit(trees_rdm)
labels = kmeans.predict(trees_2d)
#print trees.shape

def recreate_image(codebook, labels, w, h):
    """Recreate the (compressed) image from the code book & labels"""
    d = codebook.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return image

plt.figure(1)
plt.clf()
ax = plt.axes([0, 0, 1, 1])
plt.axis('off')
plt.title('Quantized image ( %d colors, K-Means)'%ncolors)
plt.imshow(recreate_image(kmeans.cluster_centers_, labels, w, h))    
plt.show()