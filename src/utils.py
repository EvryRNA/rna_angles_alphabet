import pickle
from typing import Any


def save_model(path : str, model : Any):

    pickle.dump(model, open(path, "wb"))

    return


def load_model(path):

    loaded_model = pickle.load(open(path, "rb"))
    print(loaded_model)

    return loaded_model


if __name__ == "__main__":
    save_model("src/test.pickle", None)
    load_model("src/test.pickle")