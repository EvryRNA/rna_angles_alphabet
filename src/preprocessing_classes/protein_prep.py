import os

from src.preprocessing_classes.preprocess_helper import PreprocessHelper

class ProteinPrep(PreprocessHelper):
	def __init__(
		self,
		dataset_path: str, 
		data_type: str, 
		temp_dir: str,
	):
		super().__init__(dataset_path, data_type, temp_dir, ["PHI", "PSI"])
				
	def get_values(self, dataset_path: str, data_type: str, temp_dir: str):
		os.system(
                f"src/c_code/angle -d {dataset_path}/ -l {temp_dir}/{data_type}_list.txt "
                + f"-o {temp_dir}/{data_type}_values -p -f -t"
            )
		