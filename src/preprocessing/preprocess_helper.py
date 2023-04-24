from abc import abstractmethod


class PreprocessHelper:
    @abstractmethod
    def get_values(self, *args, **kwargs):
        raise NotImplementedError
