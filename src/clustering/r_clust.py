import os

from src.clustering.clustering_helper import ClusteringHelper


class RClust(ClusteringHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def train_model(self, *args, **kwargs) -> str:
        """
        Execute a R script to train a model with the mclust package and save it

        Args:
        Returns:
            :return the path where the model is saved in Rds format
        """
        path_script = f"src/r_script/{self.method_name}.r"
        ign = ">/dev/null 2>&1"  # Use to ignore the script output in terminal

        os.system(f"Rscript {path_script} train {self.temp_dir} {self.mol} {ign}")

        return f"models/{self.method_name}_{self.mol}_model.Rds"

    def predict_seq(self, model_path: str, file_name: str, *args, **kwargs):
        """
        Execute a R script to load a model, fit the data and print the final sequence

        Args:
            :param model_path: the path to the saved model to use, in Rds format
            :file_name: the name of the pdb that will be treated
        """
        path_script = f"src/r_script/{self.method_name}.r"
        ign = ">/dev/null 2>&1"  # Use to ignore the script output in terminal

        os.system(
            f"Rscript {path_script} {file_name} {self.temp_dir} {self.mol} {model_path} {ign}"
        )
