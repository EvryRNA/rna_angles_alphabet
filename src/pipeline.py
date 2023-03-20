import argparse
import os
from typing import Optional

from src.utils import list_pdb, get_angle, text_to_csv, labels_to_seq
from src.clustering_method import dbscan_cluster, predict_labels


class Pipeline:
    def __init__(self,
                training_path: str,
                testing_path: str,
                nb_cluster: int = 6,
                model_name: Optional[str] = "dbscan",
                 ):
        """
        Initialise the different parameters
        """
        self.training_path = training_path
        self.testing_path = testing_path
        self.nb_cluster = nb_cluster
        self.model_name = model_name



    def train(self):
        list_pdb()
        print(f'{self.training_path}')
        os.system("src/c_code/angle -d data/training_set/ -l data/training_set.txt -o data/result_train -R -p -f -t")
        text_to_csv("data/result_train.txt")
        os.remove("data/training_set.txt")
        return None


    def test(self):
        print(f"{self.testing_path}")
        os.system("src/c_code/angle -d data/testing_set/ -l data/testing_set.txt -o data/result_test -R -p -f -t")
        text_to_csv("data/result_test.txt")
        os.remove("data/testing_set.txt")
        return None


    def fit_model(self, model_name: str):
        X = get_angle("data/result_train.csv")
        if model_name == "dbscan":
            dbscan_cluster(X)
        return None


    def get_sequence(self, model_name: str):
        X = get_angle("data/result_test.csv")
        labels = predict_labels(X, model_name)
        seq = labels_to_seq(labels)
        print(seq)
        return None


    def preprocess(self, input_path: str):
        """
        Call the C++
        """
        if input_path.endswith(".csv"):
            # EASY
            pass
        else:
            os.system(f"bin/c_file --input_file {input_path}")


    def main(self):
        self.train()
        self.fit_model(self.model_name)
        self.test()
        self.get_sequence(self.model_name)

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
        args = parser.parse_args()
        return args

if __name__ == "__main__":
    args = Pipeline.get_arguments()
    score_cli = Pipeline(**vars(args))
    score_cli.main()
