#!/usr/bin/python
# coding:utf-8
'''
Created on 2013-9-3

@author: plex
'''

import numpy as np

class LogReg():
	'''
	逻辑回归
	'''
	def __init__(self):
		self.category = 1 # 分哪一个feature
		
		self.train_data = []
		self.train_label = []
		self.test_data = []
		self.test_label = []
		
		self.weight = []
		self.alpha = 0.08
		self.max_iter = 100
		
		pass

	def load_dataset(self, trainf, testf):
		
		with open(trainf, "r") as fr:
			for line in fr.readlines():
				line_val = [float(val) for val in line.strip().split()]
				self.train_data.append([1.0] + line_val[0:-1])
				if int(line_val[-1]) == self.category:
					self.train_label.append(1)
				else:
					self.train_label.append(0)
		
		with open(trainf, "r") as fr:
			for line in fr.readlines():
				line_val = [float(val) for val in line.strip().split()]
				self.test_data.append([1.0] + line_val[0:-1])
				if int(line_val[-1]) == self.category:
					self.test_label.append(1)
				else:
					self.test_label.append(0)
		pass
	
	def train(self):
		
		x = LogReg.normalization(np.mat(self.train_data))
		y = np.mat(self.train_label).transpose()
		alpha = self.alpha
		
		self.weight = LogReg.batch_gradient_descent(x=x, y=y, alpha=alpha, maxIter=self.max_iter)
		pass
	
	@staticmethod
	def batch_gradient_descent(x, y, alpha=0.1, alpha_decay=0.99, maxIter=1000):
		w = np.zeros((x.shape[1], 1))
		
		for i in range(maxIter):
			p = LogReg.sigmoid(x * w) # p stands for predict value
			err = y - p
			w += alpha * x.transpose() * err
			alpha *= alpha_decay
			print 'batch_gradient_descent - iteration %5d with sum error %d' % (i, err.sum())
		
		return w.tolist()
	
	
	@staticmethod
	def normalization(data_mat):
		# TODO better to use (val-min)/(max-min)
# 		row_sums = data_mat.sum(axis=1)
# 		data_mat = data_mat / row_sums[:, np.newaxis]
		return data_mat
		
	@staticmethod
	def sigmoid(val):
		return 1 / (1 + np.exp(-val))
	
	def test(self):
		x = LogReg.normalization(np.mat(self.test_data))
		y = np.mat(self.test_label).transpose()
		w = np.mat(self.weight)
		
		p = LogReg.sigmoid(x * w)
		
		err_count = 0
		for err in np.abs(y-p):
			if err>0.5:
				err_count += 1
		
		print 'error rate is %s' % (err_count / x.shape[0])
		pass

if __name__ == '__main__':
	lr = LogReg()
# 	lr.load_dataset("../data/testSet.txt", "../data/testSet.txt")
	lr.load_dataset("../data/training/1698863684.tr", "../data/training/1698863684.tr")
	lr.train()
	lr.test()
	
	
	
	