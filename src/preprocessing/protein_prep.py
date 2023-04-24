import os

from src.preprocessing.preprocess_helper import PreprocessHelper


class ProteinPrep(PreprocessHelper):
    def get_values(self, data_path: str, data_type: str, temp_dir: str):
        """
        Execute a c++ script to compute the angle values of protein pdb (file or dataset)

        Args:
            :param data_path: the path to the data
                        :param data_type: either train or test, used to save the result
                        :param temp_dir: the path of the temporary directory

        """
        os.system(
            f"src/cpp_script/angle_calculation -d {data_path} "
            + f"-o {temp_dir}/{data_type}_values.csv -p -f -t"
        )
