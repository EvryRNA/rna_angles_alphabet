import os
import pickle
from typing import Any

import numpy as np
import pandas as pd


def list_pdb(path: str, data: str, temp_dir: str):
    """
    Write the list of pdb files in a directory in a txt file
    """
    with open(f"{temp_dir}/{data}_set.txt", "w") as file:
        for filename in os.listdir(path):
            file.write(f"{filename}\n")

    return


def text_to_csv(path: str):
    """
    Extract the angle values of a file to write them in a csv
    """
    with open(path, "r") as filin, open(f"{path[:-4]}.csv", "w") as filout:
        filout.write("ETA,THETA\n")
        for line in filin:
            values = line.split()

            if values[0] != "THETA" and values[0] != "NA" and values[1] != "NA":
                filout.write(f"{float(values[1])},{float(values[0])}\n")

    return


def get_angle(path):
    """
    Extract the angle values of a csv to write them in an array
    """
    angle = []

    data = pd.read_csv(path)
    x = np.array(data.ETA.values)
    y = np.array(data.THETA.values)

    for j in range(0, len(x)):
        angle.append([x[j], y[j]])

    return np.array(angle)


def save_model(path: str, model: Any):
    """
    Save a model in pickle format
    """
    with open(path, "wb") as model_file:
        pickle.dump(model, model_file)

    return


def load_model(path):
    """
    Load a model in pickle format
    """
    with open(path, "rb") as model_file:
        loaded_model = pickle.load(model_file)

    return loaded_model


def labels_to_seq(tab: np.array):
    """
    Transform the labels of an array in a string sequence
    """
    sequence = ""
    list_structure = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

    for i in range(0, len(tab)):
        if tab[i] == -1:
            letter = "X"
        else:
            letter = list_structure[tab[i]]
        sequence += letter

    return sequence
