import os

from src.preprocessing_classes.preprocess_helper import PreprocessHelper

class ProteinPrep(PreprocessHelper):

	def get_values(self, data_path: str, data_type: str, temp_dir: str):
		os.system(
				f"src/c_code/angle_calculation_new -d {data_path} "
				+ f"-o {temp_dir}/{data_type}_values.csv -p -f -t"
			)
		