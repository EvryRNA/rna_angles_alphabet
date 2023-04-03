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

    def get_train_values(self, training_path: str, temp_dir: str, angles_names: list):
        """
        Compute the angle values of the training dataset and store them in a csv

        Args:
            :param training_path: the path of the directory containing the pdb used for training
            :param temp_dir: the path of the temporary directory
            :param angles_names: names of the angles in the file, PHI-PSI for protein and
            ETA-THETA for RNA
        """
        list_pdb(training_path, "training", temp_dir)
        if angles_names[0] == "PHI":
            os.system(
                f"src/c_code/angle -d {training_path}/ -l {temp_dir}/training_set.txt -o"
                + f"{temp_dir}/result_train -p -f -t"
            )
        elif angles_names[0] == "ETA":
            os.system(
                f"src/c_code/angle -d {training_path}/ -l {temp_dir}/training_set.txt -o"
                + f"{temp_dir}/result_train -R -p -f -t"
            )
        text_to_csv(f"{temp_dir}/result_train.txt", angles_names)

    def get_test_values(self, testing_path: str, temp_dir: str, angles_names: list):
        """
        Compute the angle values of the testing dataset and store them in a csv

        Args:
            :param testing_path: the path of the directory containing the pdb to process
            :param temp_dir: the path of the temporary directory
            :param angles_names: names of the angles in the file, PHI-PSI for protein and
            ETA-THETA for RNA
        """
        list_pdb(testing_path, "testing", temp_dir)
        if angles_names[0] == "PHI":
            os.system(
                f"src/c_code/angle -d {testing_path}/ -l {temp_dir}/testing_set.txt -o"
                + f"{temp_dir}/result_test -p -f -t"
            )
        elif angles_names[0] == "ETA":
            os.system(
                f"src/c_code/angle -d {testing_path}/ -l {temp_dir}/testing_set.txt -o"
                + f"{temp_dir}/result_test -R -p -f -t"
            )
        text_to_csv(f"{temp_dir}/result_test.txt", angles_names)

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
        x = get_angle(f"{temp_dir}/result_train.csv")

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
        x = get_angle(f"{temp_dir}/result_test.csv")
        labels = list(predict_labels(x, method_name, temp_dir))
        seq = labels_to_seq(labels)
        print(seq)

    def main(self):
        if self.mol == "prot":
            angles_names = ["PHI", "PSI"]
        elif self.mol == "rna":
            angles_names = ["ETA", "THETA"]

        if self.method_name == "mclust":
            self.setup_dir(self.temp_dir)
            self.get_train_values(self.training_path, self.temp_dir, angles_names)
            os.system(f"Rscript src/mclust.r train {self.temp_dir}")
            self.get_test_values(self.testing_path, self.temp_dir, angles_names)
            os.system(f"Rscript src/mclust.r test {self.temp_dir}")
        else:
            self.setup_dir(self.temp_dir)
            self.get_train_values(self.training_path, self.temp_dir, angles_names)
            self.train_model(self.method_name, self.nb_clusters, self.temp_dir)
            self.get_test_values(self.testing_path, self.temp_dir, angles_names)
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
