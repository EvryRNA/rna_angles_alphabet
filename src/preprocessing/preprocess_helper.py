import subprocess


class PreprocessHelper:
    def __init__(self, mol: str):
        self.is_rna = mol == "rna"

    def get_values(self, data_path: str, temp_dir: str):
        """
        Execute a c++ script to compute the angle values of protein pdb (file or dataset)

        Args:
            :param data_path: the path to the data
            :param temp_dir: the path of the temporary directory

        """
        if data_path.endswith(".pdb"):
            print(f"start of preprocessing for {data_path[-8:]}")
            data_name = data_path[-8:-4]
        else:
            print("start of preprocessing for the training")
            data_name = "train"
        
        args = "-R" if self.is_rna else ""
        command = (
            f"src/cpp_script/angle_calculation -d {data_path} "
            + f"-o {temp_dir}/{data_name}_values.csv -p -f -t {args}"
        )
        subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        if data_path[-4:] == ".pdb":
            print(f"end of preprocessing for {data_path[-8:]}\n")
        else:
            print("end of preprocessing for the training\n")
