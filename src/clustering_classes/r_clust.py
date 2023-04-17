import os

from src.clustering_classes.clustering_helper import Clustering

class RClust(Clustering):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def train_model(self, *args, **kwargs):
		os.system(f"Rscript src/mclust.r train {self.temp_dir} {self.mol}")

		return f"models/mclust_{self.mol}_model.Rds"
		
	def predict_seq(self, model_path: str, *args, **kwargs):
		os.system(f"Rscript src/mclust.r test {self.temp_dir} {model_path}")
