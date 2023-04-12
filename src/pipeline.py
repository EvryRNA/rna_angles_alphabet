import argparse
import os

from src.preprocessing_classes.rna_prep import RNAPrep
from src.preprocessing_classes.protein_prep import ProteinPrep
from src.clustering_classes.r_clust import RClust
from src.clustering_classes.sklearn_clust import SklearnClust

class Pipeline:
    def __init__(
        self,
        training_path: str,
        testing_path: str,
        temp_dir: str,
        init_clusters: int,
        method_name: str,
        mol: str,
    ):
        """
        Initialize the different attributes
        """
        self.training_path = training_path
        self.testing_path = testing_path
        self.temp_dir = temp_dir
        self.init_clusters = init_clusters
        self.method_name = method_name
        self.mol = mol

    def setup_dir(self, temp_dir: str):
        """
        Create a temporary directory to store transitory files

        Args:
            :param temp_dir: the path of the temporary directory
        """
        os.makedirs("models", exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        for file in os.listdir(temp_dir):
            os.remove(f"{temp_dir}/{file}")
        


    def get_angles(self, training_path: str, testing_path: str, temp_dir: str, mol: str):
        class_molecule = RNAPrep if mol == "rna" else ProteinPrep

        if training_path is not None:
            train_angles = class_molecule(training_path, "train", temp_dir)
            train_angles.get_preprocessing()

        test_angles = class_molecule(testing_path, "test", temp_dir)
        test_angles.get_preprocessing()


    def data_process(self, temp_dir: str, method_name: str, mol: str, init_clusters: int):
        if method_name == "mclust":
            seq_process = RClust(temp_dir, mol)
            seq_process.train_model(temp_dir, mol)
            seq_process.predict_seq(temp_dir, mol)

        else:
            seq_process = SklearnClust(temp_dir, method_name, init_clusters)
            seq_process.train_model(temp_dir, method_name, mol, init_clusters)
            seq_process.predict_seq(temp_dir, method_name, mol)
        

    def main(self):

        self.setup_dir(self.temp_dir)
        self.get_angles(self.training_path, self.testing_path, self.temp_dir, self.mol)
        self.data_process(self.temp_dir, self.method_name, self.mol, self.init_clusters)


    @staticmethod
    def get_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--training_path",
            dest="training_path",
            type=str,
            help="The path to the directory with the training data",
        )
        parser.add_argument(
            "--testing_path",
            dest="testing_path",
            type=str,
            help="The path to the directory with the testing data",
        )
        parser.add_argument(
            "--temp_dir",
            dest="temp_dir",
            type=str,
            default="tmp",
            help="The path to the directory used for the temporary files",
        )
        parser.add_argument(
            "--method",
            dest="method_name",
            type=str,
            choices=["dbscan", "mean_shift", "kmeans", "hierarchical", "mclust"],
            default="dbscan",
            help="The custering method to use, kmeans needs nb_clusters",
        )
        parser.add_argument(
            "--init_clusters",
            dest="init_clusters",
            type=int,
            choices=range(2, 8),
            default=7,
            help="The number of clusters required by some clustering method",
        )
        parser.add_argument(
            "--mol",
            dest="mol",
            type=str,
            choices=["protein", "rna"],
            help="The type of biomolecule to process, protein or RNA",
        )
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    args = Pipeline.get_arguments()
    score_cli = Pipeline(**vars(args))
    score_cli.main()
