import argparse
import os
from typing import Optional

from src.utils import get_angle, text_to_csv
from src.clustering_method import dbscan_cluster


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
        print(f'{self.training_path}')
        os.system("src/c_code/angle -d data/training_set/ -l data/training.txt -o data/result_train -R -p -f -t")
        text_to_csv("data/result_train.txt")
        return None

    def test(self):
        print(f"{self.testing_path}")
        os.system("src/c_code/angle -d data/testing_set/ -l data/testing.txt -o data/result_test -R -p -f -t")
        text_to_csv("data/result_test.txt")
        return None

    def fit_model(self, model_name: str):
        X = get_angle("data/result_train.csv")
        if model_name == "dbscan":
            dbscan_cluster(X)

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
