#!/usr/bin/env python
#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn import cross_validation
from sklearn import linear_model
from sklearn import tree

csv = np.genfromtxt ('chessboard.csv', delimiter=",", skip_header=1)

X = csv[:, 0:2]      
y = csv[:, 2:3]
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, .02),np.arange(y_min, y_max, .02))

plt.subplot(2, 3, 1)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Set3)
plt.xlabel('A')
plt.ylabel('B')
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.xticks(())
plt.yticks(())
plt.title("Original Data")


test = np.genfromtxt ('test.csv', delimiter=",")
train = np.genfromtxt ('train.csv', delimiter=",")
label = train[:,2:3]
label = np.reshape(label, label.shape[0])


def accuracy(predict, label):
	hit = 0.0
	for i in range(len(predict)):
		if predict[i] == label[i]:
			hit += 1
	return hit/len(predict)	

def plotting(num, method, title):	
    plt.subplot(2, 3, num)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    Z = method.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.cool, alpha=0.5)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Set3)
    plt.xlabel('A')
    plt.ylabel('B')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())
    plt.title(title)



linear_svc = svm.SVC(kernel='linear')
linear_svc.fit(train[:,0:2], label)
#result = linear_svc.predict(test[:,0:2])
#acc = accuracy(result, np.reshape(test[:,2:3], test[:,2:3].shape[0]))
#print "Linear kernel accuracy: %.2f%%" % (linear_svc.score(test[:,0:2], np.reshape(test[:,2:3], test[:,2:3].shape[0]))*100)
scores = cross_validation.cross_val_score(linear_svc, csv[:,0:2], np.reshape(csv[:,2:3], csv[:,2:3].shape[0]), cv=5)
print "Linear kernel Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
plotting(2, linear_svc, "SVM - linear kernel")


rbf_svc = svm.SVC(kernel='rbf')
rbf_svc.fit(train[:,0:2], label)
#result = rbf_svc.predict(test[:,0:2])
#acc = accuracy(result, np.reshape(test[:,2:3], test[:,2:3].shape[0]))
#print "RBF kernel accuracy: %.2f%%" % (rbf_svc.score(test[:,0:2], np.reshape(test[:,2:3], test[:,2:3].shape[0])) *100)
scores = cross_validation.cross_val_score(rbf_svc, csv[:,0:2], np.reshape(csv[:,2:3], csv[:,2:3].shape[0]), cv=5)
print "RBF kernel Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
plotting(3, rbf_svc, "SVM - RBF kernel")



poly_svc = svm.SVC(kernel='poly')
poly_svc.fit(train[:,0:2], label)
#result = poly_svc.predict(test[:,0:2])
#acc = accuracy(result, np.reshape(test[:,2:3], test[:,2:3].shape[0]))
#print "Polynomial kernel accuracy: %.2f%%" % (poly_svc.score(test[:,0:2], np.reshape(test[:,2:3], test[:,2:3].shape[0]))*100)
scores = cross_validation.cross_val_score(poly_svc, csv[:,0:2], np.reshape(csv[:,2:3], csv[:,2:3].shape[0]), cv=5)
print "Polynomial kernel Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
plotting(4, poly_svc, "SVM - Polynomial kernel")



logreg = linear_model.LogisticRegression(C=1e5)
logreg.fit(train[:,0:2], label)
scores = cross_validation.cross_val_score(logreg, csv[:,0:2], np.reshape(csv[:,2:3], csv[:,2:3].shape[0]), cv=5)
print "Logistic Regression Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
plotting(5, logreg, "Logistic Regression")


dtree = tree.DecisionTreeClassifier()
dtree.fit(train[:,0:2], label)
scores = cross_validation.cross_val_score(dtree, csv[:,0:2], np.reshape(csv[:,2:3], csv[:,2:3].shape[0]), cv=5)
print "Decision Tree Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
plotting(6, dtree, "Decision Tree")


plt.show()
	
