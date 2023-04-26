import argparse
from typing import Any, Optional

from src.clustering.r_clust import RClust
from src.clustering.sklearn_clust import SklearnClust
from src.plot_helper import raw_data_plot
from src.preprocessing.protein_prep import ProteinPrep
from src.preprocessing.rna_prep import RNAPrep
from src.utils import setup_dir


class Pipeline:
    """
    The class used to execute all the process

    Attributes:
        training_path: The path to the directory with the training data
        testing_path: The path to the directory with the testing data
        temp_dir: The path to the directory used for temporary files
        method_name: The custering method to use
        mol: The type of biomolecule to process, protein or RNA
        model_path: The path to an existing model in pickle or Rds format
        visu_raw: Plot the raw data if True, requires a training path
    """

    def __init__(
        self,
        training_path: str,
        testing_path: str,
        temp_dir: str,
        method_name: str,
        mol: str,
        model_path: str,
        visu_raw: bool,
    ):
        self.training_path = training_path
        self.testing_path = testing_path
        self.temp_dir = temp_dir
        self.method_name = method_name
        self.mol = mol
        self.model_path = model_path
        self.visu_raw = visu_raw

    def preprocess_data(
        self,
        training_path: Optional[str] = None,
        testing_path: Optional[str] = None,
    ):
        """
        Get the angles values of a dataset in a csv

        Args:
            :param training_path: the path of the training data
            :param testing_path: the path of the testing data
        """
        training_path = self.training_path if training_path is None else training_path
        testing_path = self.testing_path if testing_path is None else testing_path

        # Setup the necessary directories
        setup_dir(self.temp_dir)

        # Initialize the class depending on the type of molecule
        class_molecule = RNAPrep if self.mol == "rna" else ProteinPrep

        if self.model_path is None:
            if training_path is None:
                raise ValueError("No training nor model path given!")
            else:
                # Get the train values
                train_angles = class_molecule()
                train_angles.get_values(training_path, "train", self.temp_dir)

                if testing_path is not None:
                    # Get the test values
                    test_angles = class_molecule()
                    test_angles.get_values(testing_path, "test", self.temp_dir)

        elif self.model_path is not None and testing_path is None:
            raise ValueError("No testing path given!")

        else:
            # Get the test values
            test_angles = class_molecule()
            test_angles.get_values(testing_path, "test", self.temp_dir)

        if self.visu_raw and training_path is not None:
            # Plot the raw data if a training path is given
            raw_data_plot(f"{self.temp_dir}/train_values.csv", self.mol)

    def initialize_clustering_model(
        self, method_name: Optional[str] = None, model_path: Optional[str] = None
    ):
        """
        Initialize the clustering class with either R or Sklearn model

        Args:
            :param method_name: the name of the clustering method to use
            :param model_path: if a model is not given, train a new model
        Returns:
            :return the class of the clustering model
        """
        class_cluster = Any

        if model_path is not None:
            # Choose the adequate class depending on the model extension
            if model_path.endswith(".pickle"):
                class_cluster = SklearnClust
            elif model_path.endswith(".Rds"):
                class_cluster = RClust
            else:
                raise ValueError("When giving a model, use a .pickle or .Rds format!")

        else:
            if method_name is not None:
                class_cluster = RClust if method_name == "mclust" else SklearnClust
            else:
                raise ValueError("No model path nor method name given!")

        return class_cluster

    def fit_data(self, method_name: Optional[str] = None, model_path: Optional[str] = None):
        """
        Train the model, fit the testing data and print the sequence

        Args:
            :param method_name: the name of the clustering method to use
            :param model_path: if a model is not given, train a new model
        """
        # Get the adequate class
        class_cluster = self.initialize_clustering_model(method_name, model_path)
        seq_process = class_cluster(self.temp_dir, self.mol)

        if model_path is None:
            # Train the model
            params = {"method_name": method_name}
            model_path = seq_process.train_model(**params)

        if self.testing_path is not None:
            # Fit the data and print the sequence
            seq_process.predict_seq(model_path)

    def main(self):
        self.preprocess_data(self.training_path, self.testing_path)
        self.fit_data(self.method_name, self.model_path)

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
            choices=["dbscan", "mean_shift", "kmeans", "hierarchical", "mclust", "outlier", "som"],
            default=None,
            help="The custering method to use",
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
            help="Plot the raw data if True, requires a training path",
        )
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    args = Pipeline.get_arguments()
    score_cli = Pipeline(**vars(args))
    score_cli.main()
