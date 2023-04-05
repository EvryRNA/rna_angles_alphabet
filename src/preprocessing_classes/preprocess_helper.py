from abc import abstractmethod

from src.utils import list_pdb, text_to_csv

class PreprocessHelper:
	def __init__(
		self,
		dataset_path: str,
		data_type: str,
		temp_dir: str,
		angle_names: list,
	):
		self.dataset_path = dataset_path 
		self.data_type = data_type
		self.temp_dir = temp_dir
		self.angle_names = angle_names

	@abstractmethod
	def get_values(self):
		raise NotImplementedError

	def get_list(self, dataset_path: str, data_type: str, temp_dir: str):
		list_pdb(dataset_path, data_type, temp_dir)

	def get_csv(self, data_type: str, temp_dir: str, angle_names: list):
		text_to_csv(f"{temp_dir}/{data_type}_values.txt", angle_names)

	def get_preprocessing(self):
		
		self.get_list(self.dataset_path, self.data_type, self.temp_dir)
		self.get_values(self.dataset_path, self.data_type, self.temp_dir)
		self.get_csv(self.data_type, self.temp_dir, self.angle_names)
		print(f"\nProcessing of the {self.data_type} data done\n")