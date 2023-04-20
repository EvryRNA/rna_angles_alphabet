import argparse
import os
import sys
from typing import Optional
from src.plot_helper import raw_data_plot
from src.clustering_classes.clustering_helper import Clustering

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
        method_name: str,
        mol: str,
        model_path: str,
        visu_raw: bool
    ):
        """
        Initialize the different attributes
        """
        self.training_path = training_path
        self.testing_path = testing_path
        self.temp_dir = temp_dir
        self.method_name = method_name
        self.mol = mol
        self.model_path = model_path
        self.visu_raw = visu_raw

    def setup_dir(self, temp_dir: str):
        """
        Create a temporary directory to store transitory files

        Args:
            :param temp_dir: the path of the temporary directory
        """
        os.makedirs("models", exist_ok=True)
        os.makedirs("figures_clust", exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        for file in os.listdir(temp_dir):
            os.remove(f"{temp_dir}/{file}")
        

    def get_angles(self, temp_dir: str, training_path: Optional[str],
                   testing_path: Optional[str], mol: str, model_path: Optional[str]):
        """
        Get the angles values of a dataset in a csv

        Args:
            :param temp_dir: the path of the temporary directory
            :param training_path: the path of the training data
            :param testing_path: the path of the testing data
            :param mol: the type of biomolecule, protein or rna
            :param model_path: if a model is not given, process the training data
        """
        class_molecule = RNAPrep if mol == "rna" else ProteinPrep

        if model_path is None:
            if training_path is None:
                sys.exit("Error: No training nor model path given!")
            else:
                train_angles = class_molecule()
                train_angles.get_values(training_path, "train", temp_dir)

                if testing_path is not None:
                    test_angles = class_molecule()
                    test_angles.get_values(testing_path, "test", temp_dir)

        elif model_path is not None and testing_path is None:
            sys.exit("Error: No testing path given!")

        else:
            test_angles = class_molecule()
            test_angles.get_values(testing_path, "test", temp_dir)

        if self.visu_raw and training_path is not None:
            raw_data_plot(f"{temp_dir}/train_values.csv", mol)


    def initialize_clustering_model(self, method_name:  Optional[str], 
                     model_path: Optional[str]) -> Clustering:
        """
        Initialize the clustering class with either R or Sklearn model

        Args:
            :param method_name: the name of the clustering method to use
            :param model_path: if a model is not given, train a new model
        Returns:
            :return the class of the clustering model
        """
        if model_path is not None:
            if model_path.endswith(".pickle"):
                class_cluster = SklearnClust
            elif model_path.endswith(".Rds"):
                class_cluster = RClust
            else:
                sys.exit(f"FORMAT FILE NOT GOOD : \"{model_path}\", use .pickle or .Rds")

        else:
            if method_name is not None:
                class_cluster = RClust if method_name == "mclust" else SklearnClust
            else:
                sys.exit("Error: No model path nor method name given!")

        return class_cluster


    def fit_data(self, temp_dir: str, method_name:  Optional[str], mol: str, 
                     model_path: Optional[str]):
        """
        Train the model, fit the testing data and print the sequence

        Args:
            :param temp_dir: the path of the temporary directory
            :param method_name: the name of the clustering method to use
            :param mol: the type of biomolecule, protein or rna
            :param model_path: if a model is not given, train a new model
        """
        class_cluster = self.initialize_clustering_model(method_name, model_path)
        seq_process = class_cluster(temp_dir, mol)

        if model_path is None:
            params = {"method_name": method_name}
            model_path = seq_process.train_model(**params)
    
        if self.testing_path is not None:
            seq_process.predict_seq(model_path)


    def main(self):

        self.setup_dir(self.temp_dir)
        self.get_angles(self.temp_dir, self.training_path, self.testing_path,
                         self.mol, self.model_path)
        self.fit_data(self.temp_dir, self.method_name, self.mol, self.model_path)


    @staticmethod
    def get_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--training_path",
            dest="training_path",
            type=str,
            default=None,
            help="The path to the directory with the training data",
        )
        parser.add_argument(
            "--testing_path",
            dest="testing_path",
            type=str,
            default=None,
            help="The path to the directory with the testing data",
        )
        parser.add_argument(
            "--temp_dir",
            dest="temp_dir",
            type=str,
            default="tmp",
            help="The path to the directory used for temporary files",
        )
        parser.add_argument(
            "--method",
            dest="method_name",
            type=str,
            choices=["dbscan", "mean_shift", "kmeans", "hierarchical", "mclust",
                     "som", "outlier"],
            default=None,
            help="The custering method to use, kmeans needs nb_clusters",
        )
        parser.add_argument(
            "--mol",
            dest="mol",
            type=str,
            choices=["protein", "rna"],
            required=True,
            help="The type of biomolecule to process, protein or RNA",
        )
        parser.add_argument(
            "--model",
            dest="model_path",
            type=str,
            default=None,
            help="The path to an existing model in pickle or Rds format",
        )
        parser.add_argument(
            "--v",
            dest="visu_raw",
            action=argparse.BooleanOptionalAction,
            default=False,
            help="Plot the raw data, requires a training path",
        )
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    args = Pipeline.get_arguments()
    score_cli = Pipeline(**vars(args))
    score_cli.main()
