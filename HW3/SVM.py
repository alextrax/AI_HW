#!/usr/bin/env python
#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn import cross_validation
from sklearn import linear_model
from sklearn import tree
from sklearn.cross_validation import train_test_split
from sklearn import grid_search

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


csv1 = csv[csv[:,2] == 1] # All samples with label == 1
csv0 = csv[csv[:,2] == 0] # All samples with label == 0

train1_x, test1_x, train1_y, test1_y = train_test_split(csv1[:,0:2], csv1[:,2], train_size=0.6)
train0_x, test0_x, train0_y, test0_y = train_test_split(csv0[:,0:2], csv0[:,2], train_size=0.6)

train = np.concatenate((train1_x, train0_x), axis=0) # x for training set
test = np.concatenate((test1_x, test0_x), axis=0)	# x for testing set
label = np.concatenate((train1_y, train0_y), axis=0) # y for training set
label_test = np.concatenate((test1_y, test0_y), axis=0) # y for testing set
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



def parameter_search(svr, x, y, parameters): # Use GridSearchCV to search best parameters based on cross-validation score
	clf = grid_search.GridSearchCV(estimator=svr, param_grid=parameters, cv=5, verbose=2, n_jobs=1, 
                       refit=True)
	clf.fit(x, y)
	print("Best parameters :")
	print(clf.best_params_)
	print("Best score :")
	print(clf.best_score_)
	print("Grid scores on development set:")
	for params, mean_score, scores in clf.grid_scores_:
		print("%0.3f (+/-%0.03f) for %r"% (mean_score, scores.std() * 2, params))

def search_all(): # Auto select best parameters
	search_paras = [{ 'C': [0.001, 0.1, 1, 5, 10, 20, 50, 100], 'gamma':['auto',5, 4, 3, 2, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]}				]
	#svr = svm.SVC(kernel='poly')	
	#svr = svm.SVC(kernel='rbf')
	svr = svm.SVC(kernel='linear')
	parameter_search(svr, train, label, search_paras)

def run_all(): # Use test set to get all result and plotting
	linear_svc = svm.SVC(kernel='linear', C=0.001)
	linear_svc.fit(train, label)
	print "Linear kernel test data accuracy: %.2f%%" % (linear_svc.score(test, label_test)*100)
	scores = cross_validation.cross_val_score(linear_svc, train, label, cv=5)
	print "Linear kernel Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
	plotting(2, linear_svc, "SVM - linear kernel")


	rbf_svc = svm.SVC(kernel='rbf', C=20, gamma=2)
	rbf_svc.fit(train, label)
	print "RBF kernel test data accuracy: %.2f%%" % (rbf_svc.score(test, label_test)*100)
	scores = cross_validation.cross_val_score(rbf_svc, train, label, cv=5)
	print "RBF kernel Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
	plotting(3, rbf_svc, "SVM - RBF kernel")
	
	
	poly_svc = svm.SVC(kernel='poly', degree=5, C=0.1, gamma=1)
	poly_svc.fit(train, label)
	print "Polynomial kernel test data accuracy: %.2f%%" % (poly_svc.score(test, label_test)*100)
	scores = cross_validation.cross_val_score(poly_svc, train, label, cv=5)
	print "Polynomial kernel Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
	plotting(4, poly_svc, "SVM - Polynomial kernel")


	logreg = linear_model.LogisticRegression()
	logreg.fit(train, label)
	print "Logistic Regression test data accuracy: %.2f%%" % (logreg.score(test, label_test)*100)
	scores = cross_validation.cross_val_score(logreg, train, label, cv=5)
	print "Logistic Regression Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
	plotting(5, logreg, "Logistic Regression")


	dtree = tree.DecisionTreeClassifier()
	dtree.fit(train, label)
	print "Decision tree test data accuracy: %.2f%%" % (dtree.score(test, label_test)*100)
	scores = cross_validation.cross_val_score(dtree, train, label, cv=5)
	print "Decision Tree Cross-Validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
	plotting(6, dtree, "Decision Tree")
	

	plt.show()

run_all()
#search_all()


