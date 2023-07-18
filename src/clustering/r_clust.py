import os

from src.clustering.clustering_helper import ClusteringHelper


class RClust(ClusteringHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def train_model(self,*args, **kwargs) -> str:
        """
        Execute a R script to train a model with the mclust package and save it

        Args:
            :param temp_dir: the path of the temporary directory
            :param mol: the type of biomolecule, protein or rna
        Returns:
            :return the path where the model is saved in Rds format
        """
        os.system(f"Rscript src/r_script/{self.method_name}.r train {self.temp_dir} {self.mol}")

        return f"models/{self.method_name}_{self.mol}_model.Rds"

    def predict_seq(self, model_path: str, file_name: str, *args, **kwargs):
        """
        Execute a R script to load a model, fit the data and print the final sequence

        Args:
            :param temp_dir: the path of the temporary directory
            :param model_path: the path to the saved model to use, in Rds format
        """
        os.system(f"Rscript src/r_script/{self.method_name}.r {file_name} {self.temp_dir} {model_path}")
        
