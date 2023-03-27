import argparse
import os

from src.utils import list_pdb, get_angle, text_to_csv, labels_to_seq
from src.clustering_method import dbscan_cluster, kmeans_cluster, hierarchical_cluster, predict_labels

# CONVERTER_NAME_TO_CLUSTER_MODEL = {
#     "dbscan": ClusterSklearn,
# }

class Pipeline:
    def __init__(self,
                training_path: str,
                testing_path: str,
                temp_dir: str,
                nb_cluster: int,
                method_name: str,
                 ):
        """
        Initialize the different parameters
        """
        self.training_path = training_path
        self.testing_path = testing_path
        self.temp_dir = temp_dir
        self.nb_cluster = nb_cluster
        self.method_name = method_name


    def setup_dir(self, temp_dir: str):
        """
        Create a temporary directory to store transitory files
        """
        if not os.path.isdir(temp_dir):
            os.mkdir(temp_dir)
        else:
            for file in os.listdir(temp_dir):
                os.remove(f"{temp_dir}/{file}")


    def get_train_values(self, training_path: str, temp_dir: str):
        """
        Compute the angle values of the training dataset and store them in a csv
        """
        list_pdb(training_path, "training", temp_dir)
        os.system(f"src/c_code/angle -d {training_path} -l {temp_dir}/training_set.txt -o {temp_dir}/result_train -R -p -f -t")
        text_to_csv(f"{temp_dir}/result_train.txt")


    def get_test_values(self, testing_path: str, temp_dir: str):
        """
        Compute the angle values of the testing dataset and store them in a csv
        """
        list_pdb(testing_path, "testing", temp_dir)
        os.system(f"src/c_code/angle -d {testing_path} -l {temp_dir}/testing_set.txt -o {temp_dir}/result_test -R -p -f -t")
        text_to_csv(f"{temp_dir}/result_test.txt")


    def train_model(self, method_name: str, nb_cluster: int, temp_dir: str):
        """
        Train a model with the training values
        """
        x = get_angle(f"{temp_dir}/result_train.csv")

        # cluster_helper = CONVERTER_NAME_TO_CLUSTER_MODEL.get(method_name)(nb_cluster,  )
        # return cluster_helper.predict()
        if method_name == "dbscan":
            dbscan_cluster(x, temp_dir)
        elif method_name == "kmeans":
            kmeans_cluster(x, nb_cluster, temp_dir)
        elif method_name == "hierarchical":
            hierarchical_cluster(x, temp_dir)


    def get_sequence(self, method_name: str, temp_dir: str):
        """
        Fit the testing values on the train model and get a representative sequence
        """
        x = get_angle(f"{temp_dir}/result_test.csv")
        labels = predict_labels(x, method_name, temp_dir)
        seq = labels_to_seq(labels)
        print(seq)


    def main(self):
        self.setup_dir(self.temp_dir)
        self.get_train_values(self.training_path, self.temp_dir)
        self.train_model(self.method_name, self.nb_cluster, self.temp_dir)
        self.get_test_values(self.testing_path, self.temp_dir)
        self.get_sequence(self.method_name, self.temp_dir)


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
            "--temp_dir",
            dest="temp_dir",
            type=str,
            default="tmp",
             help="",
        )
        parser.add_argument(
            "--method",
            dest="method_name",
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
