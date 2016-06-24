#!/usr/bin/env python
#coding:utf-8

from sklearn.utils import shuffle
from sklearn.cluster import spectral_clustering
from sklearn.cluster import SpectralClustering
from sklearn.feature_extraction import image
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
import matplotlib as mpl
ncolors = 4


trees = misc.imread("linkedin.png")
trees = np.array(trees, dtype=np.float64)
trees = misc.imresize(trees, 0.8) / 255.
print trees.shape

w, h, d = tuple(trees.shape)
mask = trees.astype(bool)
trees_2d = np.reshape(trees, (w * h, d))

quantized = SpectralClustering(n_clusters=ncolors, eigen_solver='arpack').fit_predict(trees_2d)

cmap = mpl.cm.cool
norm = mpl.colors.Normalize(vmin=0, vmax=ncolors)
print quantized.shape#

image = np.reshape(quantized, (w , h))

plt.imshow(image, vmin=0, vmax=ncolors)    
plt.show()