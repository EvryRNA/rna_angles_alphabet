import argparse
import os
from typing import Optional

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
        return None

    def test(self):
        print(f"{self.testing_path}")
        return None

    def fit_model(self, model_name: str):
        if model_name == "dbscan":
            dbscan_cluster()

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
