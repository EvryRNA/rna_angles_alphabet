from abc import ABC, abstractmethod

class Clustering(ABC):
	def __init__(self):

		@abstractmethod
		def train_model():
			pass
		
		@abstractmethod
		def predict_seq():
			pass
