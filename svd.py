"""
	Assignment #2
	Project: To implement both SVD and CUR Matrix decomposition algorithms and 
	compare their efficency (in terms of space, time etc.)

	Instructor: Dr. Aruna Malapati

	Contributors: G V Sandeep 2014A7PS106H
                  Kushagra Agrawal 2014AAPS334H
                  Snehal Wadhwani 2014A7PS430H

	Course: CS F469 Information Retrieval

"""

import numpy as np
import math
import time
from numpy import linalg as LA
from common import handle_input, calc_error, print_matrix

def eigen_pairs(matrix):
	
	"""
	FINDING THE SIGNIFICANT EIGEN_VALUES AND EIGEN_VECTORS
	Input : A Matrix
	Output : A dicitonary with keys as eigen values and value as the corressponding eigen vector
	"""

	eigen_values,eigen_vectors = LA.eig(matrix)
	eigen_pairs = {}
	for i in range(0,len(eigen_values)):
		eigen_pairs[eigen_values[i]] = eigen_vectors[:,i]

	eigen_values = sorted(eigen_values)

	final_eigen_pairs = {}
	for j in eigen_values:
		final_eigen_pairs[round(j.real,2)] =  eigen_pairs[j].real

	return final_eigen_pairs


def svd(ratings):

	"""
	A function to return the three matrices of the SVD Decomposition
	Input : A matrix
	Output : Three decomposed matrices which when multiplied would approxiamte the original matrix with lowest reconstruction error
	The matrices U and V are column orthonormal. Sigma is a diagonal matrix whose diagonal elements are the square roots of the eigen values listed in descending order.
	"""
	for_U = eigen_pairs(np.dot(ratings,ratings.T))
	for_V = eigen_pairs(np.dot(ratings.T,ratings))

	eigen_values = []
	for j in for_U:
		if abs(j) !=0 :
			eigen_values.append(round(j,2))
	eigen_values = sorted(eigen_values)[::-1]

	U = np.zeros((len(for_U[eigen_values[0]]),len(eigen_values)))
	V = np.zeros((len(for_V[eigen_values[0]]),len(eigen_values)))

	for j in xrange(len(eigen_values)):
		for i in xrange(len(for_U[eigen_values[j]])):
			U[i][j] = for_U[eigen_values[j]][i]
		for i in xrange(len(for_V[eigen_values[j]])):
			V[i][j] = for_V[eigen_values[j]][i]

	V = V.T

	sigma = np.zeros((len(eigen_values),len(eigen_values)))
	for i in xrange(len(eigen_values)):
		sigma[i][i] = eigen_values[i]**0.5

	for i in xrange(len(sigma)):
		temp = np.dot(ratings,np.matrix(V[i]).T)
		temp_U = np.matrix(U[:,i]).T
		flag = False
		for j in xrange(len(temp)):
			if temp_U[j] != 0.0:
				if temp[j]/temp_U[j] < 0.0 :
					flag = True
					break
		if flag:
			for k in xrange(len(U[:,i])):
				U[k][i] = -1 * U[k][i]

	return U,sigma,V