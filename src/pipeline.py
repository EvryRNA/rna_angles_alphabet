import argparse
import os

from src.utils import list_pdb, get_angle, text_to_csv, labels_to_seq
from src.clustering_method import dbscan_cluster, kmeans_cluster, hierarchical_cluster, predict_labels


class Pipeline:
    def __init__(self,
                training_path: str,
                testing_path: str,
                nb_cluster: int,
                model_name: str,
                 ):
        """
        Initialize the different parameters
        """
        self.training_path = training_path
        self.testing_path = testing_path
        self.nb_cluster = nb_cluster
        self.model_name = model_name


    def setup_dir(self):
        """
        Create a temporary directory to store transitory files
        """
        if not os.path.isdir("tmp"):
            os.mkdir("tmp")
        else:
            for file in os.listdir("tmp"):
                os.remove(f"tmp/{file}")


    def get_train_values(self):
        """
        Compute the angle values of the training dataset and store them in a csv
        """
        list_pdb(self.training_path, "training")
        os.system(f"src/c_code/angle -d {self.training_path} -l tmp/training_set.txt -o tmp/result_train -R -p -f -t")
        text_to_csv("tmp/result_train.txt")


    def get_test_values(self):
        """
        Compute the angle values of the testing dataset and store them in a csv
        """
        list_pdb(self.testing_path, "testing")
        os.system(f"src/c_code/angle -d {self.testing_path} -l tmp/testing_set.txt -o tmp/result_test -R -p -f -t")
        text_to_csv("tmp/result_test.txt")


    def train_model(self):
        """
        Train a model with the training values
        """
        x = get_angle("tmp/result_train.csv")
        if self.model_name == "dbscan":
            dbscan_cluster(x)
        elif self.model_name == "kmeans":
            kmeans_cluster(x, self.nb_cluster)
        elif self.model_name == "hierarchical":
            hierarchical_cluster(x)


    def get_sequence(self):
        """
        Fit the testing values on the train model and get a representative sequence
        """
        x = get_angle("tmp/result_test.csv")
        labels = predict_labels(x, self.model_name)
        seq = labels_to_seq(labels)
        print(seq)


    def main(self):
        self.setup_dir()
        self.get_train_values()
        self.train_model()
        self.get_test_values()
        self.get_sequence()


    @staticmethod
    def get_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--training_path",
            dest="training_path",
            type=str,
            help="",
        )
        parser.add_argument(
            "--testing_path",
            dest="testing_path",
            type=str,
             help="",
        )
        parser.add_argument(
            "--method",
            dest="model_name",
            type=str,
            choices=["dbscan", "kmeans", "hierarchical"],
            default="dbscan",
             help="",
        )
        parser.add_argument(
            "--nb_cluster",
            dest="nb_cluster",
            type=int,
            choices=range(2, 8),
            default=7,
             help="",
        )
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    args = Pipeline.get_arguments()
    score_cli = Pipeline(**vars(args))
    score_cli.main()
