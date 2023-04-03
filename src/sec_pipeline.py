import argparse
import os

from src.clustering_method import (
    dbscan_cluster,
    hierarchical_cluster,
    kmeans_cluster,
    mean_shift_cluster,
    predict_labels,
)
from src.utils import get_angle, labels_to_seq, list_pdb, text_to_csv
from src.preprocessing_classes.rna import RNA_Prep
from src.preprocessing_classes.protein import Protein_Prep

class Pipeline:
    def __init__(
        self,
        training_path: str,
        testing_path: str,
        temp_dir: str,
        nb_clusters: int,
        method_name: str,
        mol: str,
    ):
        """
        Initialize the different attributes
        """
        self.training_path = training_path
        self.testing_path = testing_path
        self.temp_dir = temp_dir
        self.nb_clusters = nb_clusters
        self.method_name = method_name
        self.mol = mol

    def setup_dir(self, temp_dir: str):
        """
        Create a temporary directory to store transitory files

        Args:
            :param temp_dir: the path of the temporary directory
        """
        os.makedirs(temp_dir, exist_ok=True)

    def get_angles(self, training_path: str, testing_path: str, temp_dir: str, mol: str):
        if mol == "rna":
            if training_path != None:
                train_angles = RNA_Prep(training_path, "train", temp_dir)
                train_angles.get_list(training_path, "train", temp_dir)
                train_angles.get_values(training_path, "train", temp_dir)
                train_angles.get_csv("train", temp_dir, ["ETA", "THETA"])

            if testing_path != None:
                test_angles = RNA_Prep(testing_path, "test", temp_dir)
                test_angles.get_list(testing_path, "test", temp_dir)
                test_angles.get_values(testing_path, "test", temp_dir)
                test_angles.get_csv("test", temp_dir, ["ETA", "THETA"])

        elif mol == "protein":
            if training_path != None:
                train_angles = Protein_Prep(training_path, "train", temp_dir)
                train_angles.get_list(training_path, "train", temp_dir)
                train_angles.get_values(training_path, "train", temp_dir)
                train_angles.get_csv("train", temp_dir, ["ETA", "THETA"])

            if testing_path != None:
                test_angles = Protein_Prep(testing_path, "test", temp_dir)
                test_angles.get_list(testing_path, "test", temp_dir)
                test_angles.get_values(testing_path, "test", temp_dir)
                test_angles.get_csv("test", temp_dir, ["ETA", "THETA"])

    def train_model(
        self,
        method_name: str,
        nb_clusters: int,
        temp_dir: str,
    ):
        """
        Train a model with the training values

        Args:
            :param method_name: the name of the clustering method to use
            :param nb_clusters: the number of clusters to be used by some methods
            :param temp_dir: the path of the temporary directory
        """
        x = get_angle(f"{temp_dir}/train_values.csv")

        if method_name == "dbscan":
            dbscan_cluster(x, temp_dir)
        elif method_name == "mean_shift":
            mean_shift_cluster(x, temp_dir)
        elif method_name == "kmeans":
            kmeans_cluster(x, nb_clusters, temp_dir)
        elif method_name == "hierarchical":
            hierarchical_cluster(x, temp_dir)

    def get_sequence(self, method_name: str, temp_dir: str):
        """
        Fit the testing values on the train model and get a representative sequence

        Args:
            :param method_name: the name of the clustering method used
            :param temp_dir: the path of the temporary directory
        """
        x = get_angle(f"{temp_dir}/test_values.csv")
        labels = list(predict_labels(x, method_name, temp_dir))
        seq = labels_to_seq(labels)
        print(seq)

    def main(self):

        if self.method_name == "mclust":
            self.setup_dir(self.temp_dir)
            self.get_angles(self.training_path, self.testing_path, self.temp_dir, self.mol)
            os.system(f"Rscript src/mclust.r train {self.temp_dir}")
            os.system(f"Rscript src/mclust.r test {self.temp_dir}")
        else:
            self.setup_dir(self.temp_dir)
            self.get_angles(self.training_path, self.testing_path, self.temp_dir, self.mol)
            self.train_model(self.method_name, self.nb_clusters, self.temp_dir)
            self.get_sequence(self.method_name, self.temp_dir)

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
            "--nb_clusters",
            dest="nb_clusters",
            type=int,
            choices=range(2, 8),
            default=7,
            help="The number of clusters used by some clustering method",
        )
        parser.add_argument(
            "--mol",
            dest="mol",
            type=str,
            choices=["prot", "rna"],
            help="The type of biomolecule to process, protein or RNA",
        )
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    args = Pipeline.get_arguments()
    score_cli = Pipeline(**vars(args))
    score_cli.main()
