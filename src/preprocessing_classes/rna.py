import os

from src.preprocessing_classes.preprocess_helper import Preprocess

class RNA_Prep(Preprocess):
	def __init__(
		self,
		dataset_path: str,
		data_type: str,
		temp_dir: str,
	):
		self.dataset_path = dataset_path, 
		self.data_type = data_type,
		self.temp_dir = temp_dir,
		super().__init__(dataset_path, data_type, temp_dir, ["ETA", "THETA"])
		
	def get_values(self, dataset_path: str, data_type: str, temp_dir: str):
		os.system(
				f"src/c_code/angle -d {dataset_path}/ -l {temp_dir}/{data_type}_list.txt "
				+ f"-o {temp_dir}/{data_type}_values -R -p -f -t"
			)
