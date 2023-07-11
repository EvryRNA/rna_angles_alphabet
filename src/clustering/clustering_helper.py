from abc import abstractmethod


class ClusteringHelper:
    def __init__(
        self,
        temp_dir: str,
        mol: str,
        method_name: str,
    ):
        self.temp_dir = temp_dir
        self.mol = mol
        self.method_name = method_name

    @abstractmethod
    def train_model(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def predict_seq(self, *args, **kwargs):
        raise NotImplementedError
