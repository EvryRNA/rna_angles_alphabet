import os

from src.clustering_classes.clustering_helper import Clustering

class RClust(Clustering):
	def __init__(
		self,
		temp_dir: str,
		mol: str
	):
		self.temp_dir = temp_dir,
		self.mol = mol,
		super().__init__()
		
	def train_model(self, temp_dir: str, mol: str):
		os.system(f"Rscript src/mclust.r train {temp_dir} {mol}")
		
	def predict_seq(self, temp_dir: str, mol: str):
		os.system(f"Rscript src/mclust.r test {temp_dir} {mol}")
