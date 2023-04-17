from abc import abstractmethod

class Clustering():
	def __init__(self, temp_dir: str, mol: str,):
		self.temp_dir = temp_dir
		self.mol = mol


	@abstractmethod
	def train_model(self):
		raise NotImplementedError
	
	@abstractmethod
	def predict_seq(self):
		raise NotImplementedError
