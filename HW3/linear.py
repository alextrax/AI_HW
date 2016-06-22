#!/usr/bin/env python
#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt


ALPHA = 1

# read csv and transform it into numpy float arrays
ages = np.array(np.loadtxt('girls_age_weight_height_2_8.csv',dtype=str,delimiter=',',usecols=(0,))).astype(np.float)
weights = np.array(np.loadtxt('girls_age_weight_height_2_8.csv',dtype=str,delimiter=',',usecols=(1,))).astype(np.float)
heights = np.array(np.loadtxt('girls_age_weight_height_2_8.csv',dtype=str,delimiter=',',usecols=(2,))).astype(np.float)

std_age = np.std(ages)
std_weight = np.std(weights)
mean_age = np.mean(ages)
mean_weight = np.mean(weights)
print "Std dev of age:", std_age, "\nStd dev of weight:", std_weight
print "Mean of age:", mean_age, "\nMean of weight:", mean_weight

ages_scaled = np.empty_like(ages)
weight_scaled = np.empty_like(weights)

for i in range(ages_scaled.shape[0]):
	ages_scaled[i] = (ages[i] - mean_age)/std_age 

for i in range(weight_scaled.shape[0]):
	weight_scaled[i] = (weights[i] - mean_weight)/std_weight


def gradient_decent(x, y, times):
	theta = np.zeros(x.shape[1])
	for i in xrange(times):
		estimate = np.dot(x, theta)
		loss = estimate - y
		gradient = np.dot(x.T, loss) / x.shape[0]
		#print gradient, x.shape[0], x.shape[1]
		theta = theta - ALPHA * gradient    
		print "# %d , loss = %f" % (i, np.sum(abs(loss)))

	return theta	


def predicted(age, weight, theta):
	a = (age - mean_age)/std_age 
	w = (weight - mean_weight)/std_weight
	return np.dot(np.array([1,a,w]).T, theta)


one_array = np.ones(ages.shape[0])
x = np.array([one_array, ages_scaled, weight_scaled]).T
theta = gradient_decent(x, heights, 50)	
print theta
print predicted(5, 20, theta)






