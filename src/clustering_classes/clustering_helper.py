from abc import abstractmethod

class Clustering():
	def __init__(self):

		@abstractmethod
		def train_model(self):
			raise NotImplementedError
		
		@abstractmethod
		def predict_seq(self):
			raise NotImplementedError
