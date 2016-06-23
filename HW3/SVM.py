#!/usr/bin/env python
#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn import cross_validation
from sklearn import linear_model
from sklearn import tree
from sklearn.cross_validation import train_test_split

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


csv1 = csv[csv[:,2] == 1]
csv0 = csv[csv[:,2] == 0]

train1_x, test1_x, train1_y, test1_y = train_test_split(csv1[:,0:2], csv1[:,2], train_size=0.6)
train0_x, test0_x, train0_y, test0_y = train_test_split(csv0[:,0:2], csv0[:,2], train_size=0.6)

train = np.concatenate((train1_x, train0_x), axis=0)
test = np.concatenate((test1_x, test0_x), axis=0)
label = np.concatenate((train1_y, train0_y), axis=0)
label_test = np.concatenate((test1_y, test0_y), axis=0)
label = np.reshape(label, label.shape[0])


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



linear_svc = svm.SVC(kernel='linear', C=1)
linear_svc.fit(train, label)
print "Linear kernel test data accuracy: %.2f%%" % (linear_svc.score(test, label_test)*100)
scores = cross_validation.cross_val_score(linear_svc, csv[:,0:2], np.reshape(csv[:,2:3], csv[:,2:3].shape[0]), cv=5)
print "Linear kernel Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
plotting(2, linear_svc, "SVM - linear kernel")


rbf_svc = svm.SVC(kernel='rbf')
rbf_svc.fit(train, label)
print "RBF kernel test data accuracy: %.2f%%" % (rbf_svc.score(test, label_test)*100)
scores = cross_validation.cross_val_score(rbf_svc, csv[:,0:2], np.reshape(csv[:,2:3], csv[:,2:3].shape[0]), cv=5)
print "RBF kernel Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
plotting(3, rbf_svc, "SVM - RBF kernel")



poly_svc = svm.SVC(kernel='poly', degree=7, C=2)
poly_svc.fit(train, label)
print "Polynomial kernel test data accuracy: %.2f%%" % (poly_svc.score(test, label_test)*100)
#scores = cross_validation.cross_val_score(poly_svc, csv[:,0:2], np.reshape(csv[:,2:3], csv[:,2:3].shape[0]), cv=5)
#print "Polynomial kernel Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
plotting(4, poly_svc, "SVM - Polynomial kernel\ndegree=7")


logreg = linear_model.LogisticRegression()
logreg.fit(train, label)
print "Logistic Regression test data accuracy: %.2f%%" % (logreg.score(test, label_test)*100)
scores = cross_validation.cross_val_score(logreg, csv[:,0:2], np.reshape(csv[:,2:3], csv[:,2:3].shape[0]), cv=5)
print "Logistic Regression Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
plotting(5, logreg, "Logistic Regression")


dtree = tree.DecisionTreeClassifier()
dtree.fit(train, label)
print "Decision tree test data accuracy: %.2f%%" % (dtree.score(test, label_test)*100)
scores = cross_validation.cross_val_score(dtree, csv[:,0:2], np.reshape(csv[:,2:3], csv[:,2:3].shape[0]), cv=5)
print "Decision Tree Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
plotting(6, dtree, "Decision Tree")


plt.show()

